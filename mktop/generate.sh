#### $1 is your pdb file
#### add this file to your folder with a single pdb file as a subdirectory here

perl ../mktop.pl -i $1 -o topology.top -ff opls -conect no
mv topology.top topol.top
bash ../fixCharges.sh topol.top
cp ../NPT.mdp ../EQM.mdp .
python ../pdb2gmx.py $1 topol.top
