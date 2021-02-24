for i in `seq 1 20` ; do grompp -v -f NPT.mdp -c out2.gro ;  mdrun -v -c out2.gro -nt 4; rm \#*; done
