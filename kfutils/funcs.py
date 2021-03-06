__all__ = ['smoothen', 'getShape', 'writeShapedFile', 'writeFile']



import numpy as np 
from scipy.interpolate import RectBivariateSpline
import os,shutil,subprocess,sys
from csaps import csaps





def smoothen(data, shape, tc, pc, cols, sm=0.95):
    data.shape = shape

    grid = [data[:,0,tc], data[0,:, pc]]

    res = np.copy(data)

    for c in cols:
        res[...,c] = csaps(grid, data[...,c], grid, smooth=sm)
    return res




def getShape(data):
    for i in range(data.shape[1]):
        print(np.unique(data[:,i]).shape)



def writeShapedFile(file,data,fmt='%.8f'):
    assert len(data.shape)==3, "A 3D data is required for this function"
    with open(file, 'w') as f:
        for i in data:
            np.savetxt(f,i,delimiter='\t', fmt=fmt)
            f.write('\n')
    


def writeFile(file,dat,tc=0,fmt='%.8f'):
    with open(file,'w') as f:
        for i in np.unique(dat[:,tc]):
            np.savetxt(f,dat[dat[:,tc]==i],delimiter='\t', fmt=fmt)
            f.write('\n')

