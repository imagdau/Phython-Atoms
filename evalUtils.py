import ase.io
from ase import Atoms
import os

def eval_gap_quip(inxyz_file, outxyz_file, gap_file, init_args=None):
    quipcmd = "atoms_filename="+inxyz_file
    if init_args is not None:
        quipcmd += " init_args=\""+init_args+"\""
    quipcmd += " param_filename="+gap_file+" E=True F=True V=True"
    os.system("quip "+quipcmd+" | grep AT | sed 's/AT//' > "+outxyz_file+"_temp.xyz")
    db = ase.io.read(outxyz_file+'_temp.xyz',':')
    for at in db:
        at.calc.reset()
        at.arrays['forces'] = at.arrays.pop('force')
        del at.arrays['map_shift']
        del at.arrays['n_neighb']
        at.info['stress'] = -at.info['virial']/at.get_volume()
        del at.info['nneightol']
        del at.info['cutoff']
    ase.io.write(outxyz_file, db)
    os.system('rm -rfv '+outxyz_file+'_temp.xyz')
