This is the directory where finite displacement calculations are set
up and run. Begin by linking the scf.in and prefix.fc file from the 
dfpt directory to this directory:

ln -s ../dfpt/scf.in .
ln -s ../dfpt/WSe2.fc .

The first step is to create the phonopy_params.yaml file. To do this
please use the command line utility script `create_phonopy_yaml.py`.

It is run in line with the folloing arguments:

create_phonopy_yaml.py scf.in prefix.fc nqx1 nqx2 nqx3

where nqx1-3 is the qgird on which the dfpt calculation
was run. In this case:

create_phonopy_yaml.py scf.in WSe2.fc 1 1 1

This should create a file phonopy_params.yaml which is 
human readable and used by Phonopy to generate modulaitons.

The next step is to run `generate_modulations.py`, please a have
look inside this file, paramters should be self explanitory. This
will generate a directory 'nmode-008/dft' which contains a number
of finite displacement calcaultions to be run by the user. Please
modify the various runscripts, 'run.sh' and run the calculation.

After the scf calculations have been run, the final step is to 
run `process_modulations.py`, which will parse the xml files from
the scf calculatons and write a file: 'diagonal_couplings_nmode-008.dat'
which the diagnoal couplings computed from finite difference.
