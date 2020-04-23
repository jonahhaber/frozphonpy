#!/usr/bin/env python

import sys
import os
import numpy as np
from phonopy.interface.qe import read_pwscf, PH_Q2R
from phonopy.phonon.band_structure import get_band_qpoints_and_path_connections
from phonopy.units import THzToEv
import phonopy


def main(scf_name, fc_name, grid):
    primcell_filename = scf_name
    q2r_filename = fc_name
    cell, _ = read_pwscf(primcell_filename)
    q2r = PH_Q2R(q2r_filename)
    q2r.run(cell)
    q2r.write_force_constants()
    
    phonon = phonopy.load(supercell_matrix=grid,
                          calculator='qe',
                          unitcell=cell,
                          force_constants_filename="force_constants.hdf5")
    
    phonon.save(settings={'force_constants': True})

    freq, evec = phonon.get_frequencies_with_eigenvectors([0.,0.,0.])


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('scf_name')
    parser.add_argument('fc_name')
    parser.add_argument('grid', nargs=3, type=int) 
    args = parser.parse_args()

    main(**vars(args))


