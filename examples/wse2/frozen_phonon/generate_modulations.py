#!/usr/bin/env python

import numpy as np
from frozphonpy import ModulationTask


modulation = ModulationTask(

    phonopy_yaml = 'phonopy_params.yaml', 
    nmode = 8,
    amplitude_list = np.arange(0.0, 0.02, 0.01),

    dft_params = dict(

    # System info
    prefix = 'WSe2',
    pseudo_dir = './pseudos',
    pseudos = ['W.upf', 'Se.upf'],
    ngkpt = [6,6,1],                                  # k-points grid
    ecutwfc = 80.0,                                   # Wavefunctions cutoff energy
    variables = {'system' : {'nosym_evc' : True},
                 'k_points' : ['automatic', [6, 6, 1, 0, 0, 0]]},

    # Parallelization info
    mpirun = 'ibrun -n 64',
    PWFLAGS='-nk 4'
    )

)
