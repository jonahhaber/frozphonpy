# Frozphonpy
Simple package for setting up frozen-phonon calculations.

# Documetation
Before beginning, it is assumed you have performed a DFPT calculation in QE and generated a `prefix.fc` with `q2r.x`.
Then there a three steps:
1. Run the inline command utility `create_phonopy_yaml.py`
2. Generate modulated strctures and set up scf calcs with `modulation_task.py`
3. Extract and process data with `postproc.py`

For additional details please see the readme in ~frozphonpy/examples/wse2/.

# Requirements
The following software and modules are required to use BGWpy.
1. python 2.7 required (Python 3 not supported at the moment)
1. BGWpy (https://github.com/BerkeleyGW/BGWpy)
3. Phonopy (https://github.com/BerkeleyGW/BGWpy)

# Installing
Once you have satisfied the requirements, install the package with

python setup.py install
