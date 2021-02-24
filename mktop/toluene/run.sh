perl ../mktop.pl -i toluene.pdb -o topology.top -ff opls -conect no
mv topology.top topol.top
bash ../fixCharges.sh topol.top
cp ../NPT.mdp .
python ../pdb2gmx.py toluene.pdb topol.top

