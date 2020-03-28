#source /global/common/software/m3035/conda-activate.sh 3.7
#bcast-pip mpl_aea
#bcast-pip mpsort

import healpy as hp
import bigfile
#from scipy import *
import numpy as np
from emcee.utils import MPIPool 
import sys
import os

folder='/global/cscratch1/sd/jialiu/fastpm/CorrelatedSims/'
def gen_comp(zs):
    f = bigfile.File(folder+'wlen_jliu/WL-%.2f-N4096'%(zs))

    nside = f['kappa'].attrs['nside'][0] 
    zmin  = f['kappa'].attrs['zlmin'][0] 
    zmax  = f['kappa'].attrs['zlmax'][0] 
    #zstep = f['kappa'].attrs['zstep'][0] 
    zs    = f['kappa'].attrs['zs'][0] 

    print('nside = ', nside)
    print('redshifts = ', zs)

    lmax = min([5000,nside])#5000
    ell_sim = np.arange(lmax+1)
    print (f['kappa'][:].shape)
    fn_cl=folder+'/clkk/kappa_cl_z%.2f.npz'%(zs)
    if not os.path.isfile(fn_cl):
        cl=hp.anafast(f['kappa'][:], lmax=lmax)
        np.savez(fn_cl, ell=ell_sim, cl = cl) 

zs=np.arange(0.1, 2.21, 0.1)
##### MPIPool
pool=MPIPool()
if not pool.is_master():
    pool.wait()
    sys.exit(0)

out=pool.map(gen_comp, zs)
pool.close()
