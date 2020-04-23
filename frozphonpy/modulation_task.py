#!/usr/bin/env python

import os
import numpy as np
import phonopy
from BGWpy import Structure, QeScfTask, Workflow
from os.path import join as pjoin


class ModulationTask:

    def __init__(self, phonopy_yaml, nmode, amplitude_list, dft_params):

        self.phonopy_yaml = phonopy_yaml
        self.nmode = nmode
        self.amplitude_list = amplitude_list
        self.num_of_modulations = len(amplitude_list)
        self.dirname = 'nmode-{:03d}'.format(self.nmode)
        self.kwargs = dft_params

        self.generate_modulations()
        self.generate_calculations()

    def generate_modulations(self):
        '''Generate the modulations.'''

        print 'Generating modulated structures...'

        phonon = phonopy.load(self.phonopy_yaml)

        Na = 3
        print 'WARNING Na is hard coded'

        # [q-point, band index (int), amplitude (float), phase (float)]
        qpt = [0., 0., 0.] # Note: fix qpt
        A_list = np.asarray(self.amplitude_list) * np.sqrt(Na)
        phonon_modes = [[qpt, self.nmode - 1, A, 0.0] for A in A_list]

        dim = [1,1,1]
        phonon.set_modulations(dim, phonon_modes)
        phonon.write_yaml_modulations()
        phonon.write_modulations()

        # Go into MPOSCAR and correct header and mode to relevant directories...
        os.system('mkdir {}'.format(self.dirname))
        os.system('mkdir {}/structures'.format(self.dirname))
        os.system('sed -i "s/   1.0/    0.529177/g" MPOSCAR*')
        os.system('mv modulation.yaml {}/structures'.format(self.dirname))
        for i in range(self.num_of_modulations):
            os.system('mv MPOSCAR-{:03d} {}/structures/POSCAR-{:03d}'.format(i+1, self.dirname, i+1))
        os.system('mv MPOSCAR* {}/structures'.format(self.dirname))


    def generate_calculations(self):
        ''' Generates calculations.'''   

        workflow = Workflow(dirname='{}/dft'.format(self.dirname))

        for i in range(self.num_of_modulations):
             
            scftask = QeScfTask(
                dirname = pjoin(workflow.dirname, 'struct-{:03d}'.format(i+1)),
                structure = Structure.from_file('{}/structures/POSCAR-{:03d}'.format(self.dirname,i+1)),
                **self.kwargs)

            workflow.add_tasks([scftask])

        # Execution
        workflow.write()
        workflow.report()
