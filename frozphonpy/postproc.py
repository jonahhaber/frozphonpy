
import os
import numpy as np
import yaml
from os.path import join as pjoin
from BGWpy.external import xmltodict


class FrozPhon:

    def __init__(self, prefix, dirname):

        # Set up directory info
        self.dirname = dirname
        self.prefix = prefix
        self.modulations_yaml = pjoin(dirname, 'structures/modulation.yaml')

        # Set up data containers
        self.na = None
        self.num_of_modulations = None
        self.amplitudes = list()
        self.nbnd = None
        self.nk = None
        self.total_energies = None
        self.eigenvalues = None
        self.kpts = None
        self.frequency = None
        self.imode = None

        # Collect data from finite disp, TODO: check that claculations finished?
        self.collect_data()

        
    def get_xml_path(self, i):
        return pjoin(self.dirname, 'dft', 'struct-{:03d}'.format(i+1), self.prefix + '.xml')


    def parse_xml(self, xml_file):
        '''Parses an xml file to find total energy and eigenvalues.'''

        with open(xml_file, 'r') as f:
            datafile = xmltodict.parse(f)

        etot = float(datafile['qes:espresso']['output']['total_energy']['etot'])
        
        nk = int(datafile['qes:espresso']['output']['band_structure']['nks'])
        nbnd = int(datafile['qes:espresso']['output']['band_structure']['nbnd'])
        self.nk = nk
        self.nbnd = nbnd

        kpts = np.zeros((nk, 3))
        eigs = np.zeros((nbnd, nk))

        ks_energies = datafile['qes:espresso']['output']['band_structure']['ks_energies']

        for ik in range(nk):

            kpts[ik, :] = np.array(map(float, ks_energies[ik]['k_point']['#text'].split()))
            eigs[:, ik] = np.array(map(float, ks_energies[ik]['eigenvalues']['#text'].split()))

        return etot, eigs, kpts

    
    def parse_modulation_yaml(self):
        '''Parse modulations.'''

        with open(self.modulations_yaml, 'r') as file:
            mod_list = yaml.load(file, Loader=yaml.FullLoader)

        # Read in Na, number of atoms in cell
        self.na = len(mod_list['supercell']['atom_info'])
        self.imode = mod_list['modulations'][0]['band']

        # Read in amplitudes and number of displaced structures
        eof = False
        i = 0
        while eof is False:
            try:
                self.amplitudes.append(mod_list['modulations'][i]['amplitude'] / np.sqrt(self.na))
                i += 1
            except IndexError:
                eof = True

        self.num_of_modulations = int(i)
        

    def collect_data(self):
        '''Collects data from finite displacement calculation.'''

        # First collect phonon data
        self.parse_modulation_yaml() 

        # Then collect electron data
        self.parse_xml(self.get_xml_path(0))
        self.total_energies = np.zeros(self.num_of_modulations)
        self.eigenvalues = np.zeros((self.num_of_modulations, self.nbnd, self.nk))

        for i in range(self.num_of_modulations):
            etot, eigs, kpts = self.parse_xml(self.get_xml_path(i))
            self.total_energies[i] = etot
            self.eigenvalues[i,:,:] = eigs

        self.kpts = kpts
             

    def compute_frequency(self):
        '''Computes the frequency from a finite difference calculation.'''

        # TODO: work in atomic units
        HBAR = 6.62607015e-34
        HAR2J = 4.35974e-18
        BORH2M = 5.29177e-11
        AMU = 1.6726219e-27
        
        amplitudes = np.array(self.amplitudes) * BORH2M
        total_energies = self.total_energies * HAR2J
        
        # Compute phonon frequecny in THz
        f = np.polyfit(amplitudes, total_energies, 2)
        a_coeff = f[0]
        ang_freq = np.sqrt( 2 * a_coeff / AMU)
        freq = ang_freq / 1.e12 / (2 * np.pi) 
        self.frequency = freq

        print 'Finite difference phonon frequency: {} THz'.format(freq)

    def compute_diagonal_coupling(self):
        '''The diagonal part of the electron-phonon coupling is given by:'''

        # TODO: work in atomic units
        HBAR = 1.054571817e-34
        HAR2J = 4.35974e-18
        HAR2MEV = 27.2114 * 1000
        BORH2M = 5.29177e-11
        AMU = 1.6726219e-27

        amplitudes = np.array(self.amplitudes) * BORH2M  # Amplitudes in meters
        eigenvalues = self.eigenvalues * HAR2MEV  # eigenvalues in meV

        self.compute_frequency()
        prefactor = np.sqrt(HBAR / (2. * AMU * self.frequency * 1e12 * 2 * np.pi))

        # Get number of bands and loop through
        diag_coupling = np.zeros((self.nbnd, self.nk))
        for ib in range(self.nbnd):
            for ik in range(self.nk):
                eigs = eigenvalues[:,ib,ik]
                f = np.polyfit(amplitudes, eigs, 1)
                diag_coupling[ib,ik] = prefactor * f[0]

        self.diag_coupling = np.abs(diag_coupling)

        return


    def write_results(self):
        '''Writes the diagonal couplings to a file'''

        with open('diagonal_couplings_nmode-{:03d}.dat'.format(self.imode), 'w') as f:
            for ik, k in enumerate(self.kpts):
                f.write('xk = {k[0]:8.4f} {k[1]:8.4f} {k[2]:8.4f}\n'.format(k=k))
                f.write('{:>6} {:>6} {:>14} {:>14} {:>14}\n'.format('ibnd', 'imode', 'eig_i (eV)', 'omega_nu (meV)', '|g| (meV)'))
                for ib in range(self.nbnd):
                    f.write('{:6d} {:6d} {:14.4f} {:14.4f} {:14.4f}\n'.format(ib+1, self.imode, self.frequency, self.eigenvalues[0, ib, ik],  self.diag_coupling[ib,ik]))

        return


