#!/bin/bash


MPIRUN='ibrun -n 64'
PW='pw.x'
PH='ph.x'
Q2R='q2r.x'
MATDYN='matdyn.x'
PWFLAGS='-nk 4'

$MPIRUN $PW $PWFLAGS -in scf.in &> scf.out
$MPIRUN $PH $PWFLAGS -in ph.in &> ph.out
$MPIRUN $Q2R $PWFLAGS -in q2r.in &> q2r.out

