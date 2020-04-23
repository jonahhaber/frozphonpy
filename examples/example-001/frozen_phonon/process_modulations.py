#!/usr/bin/env python

from frozphonpy import FrozPhon

# Create frozen phonon object
frozphon = FrozPhon(prefix='WSe2', dirname='nmode-008')

# Compute phonon frequency and diagonal couplings for this mode
frozphon.compute_frequency()
frozphon.compute_diagonal_coupling()

# Write to file
frozphon.write_results()

#amps = frozphon.amplitudes
#eig = frozphon.eigenvalues[:,0,0]
#
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pylab as plt
#
#for ib in range(frozphon.nbnd):
#    plt.plot(amps, frozphon.eigenvalues[:,ib,0]- frozphon.eigenvalues[0,ib,0], '-o')
#
#plt.savefig('test.pdf')
