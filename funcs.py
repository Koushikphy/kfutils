import numpy as np
from scipy.interpolate import splev, splrep, RectBivariateSpline
from scipy.interpolate import interp2d as inter
from scipy.interpolate import griddata
from scipy.interpolate import InterpolatedUnivariateSpline as spl





def mirror(data, tc=0, pc=1, rad=False):


    #remove other half
    if rad:
        data = data[data[:,pc]<=3.14159266]  #be carefule about this value
        new_ph = np.deg2rad(np.arange(0,363,3))
    else:
        data = data[data[:,pc]<=180]
        new_ph = np.arange(0,363,3)



    def Int(i,th):
        if i==tc:
            return np.full(new_ph.shape[0],th)
        if i==pc:
            return new_ph
        else:
            line = block[:,i]
            return np.append(line,np.flip(line[:-1]))


    # print data.shape
    res = np.array([], dtype=np.float64).reshape(0,data.shape[1])
    for th in np.unique(data[:,tc]) :
        block = data[data[:,tc]==th]
        rest = np.column_stack([Int(i,th) for i in range(data.shape[1])])
        res = np.vstack((res, rest))

    return res



def rectGridInt(data, grid1Col, grid2Col, newGrid1, newGrid2):
    '''This script interpolates only on a rectangular grid
    Can be used to make the grid more densed or vice versa

    Parameters
    ----------
    iFile : name of the input file  
    grid1Col : Column number to be used as grid 1  
    grid2Col : Column number to be used as grid2  
    newGrid1 : new number of grid for grid1  
    newGrid2 :  new number of grid for grid2  
    '''


    g1 = np.unique(data[:,grid1Col])
    g2 = np.unique(data[:,grid2Col])

    ng1 = np.linspace(g1.min(),g1.max(),newGrid1)
    ng2 = np.linspace(g2.min(),g2.max(),newGrid2)

    c1 = g1.shape[0]
    c2 = g2.shape[0]

    funcs = []
    for i in range(data.shape[1]):
        if i not in [grid1Col, grid2Col]:
            funcs.append(RectBivariateSpline(g1,g2,data[:,i].reshape(c1,c2)))
        else: 
            funcs.append(None)

    def Int(i,g1V):
        if i==grid1Col: 
            return np.full(ng2.shape,g1V) 
        elif i==grid2Col: 
            return ng2 
        else:
            return funcs[i](g1V,ng2)[0]


    res = []
    for g1V in ng1:
        res1 = np.column_stack([Int(i,g1V) for i in range(data.shape[1])])
        res.append(res1)
    return np.vstack(res)



def rectGridInt1(data, grid1Col, grid2Col, newGrid1, newGrid2):
    '''This script interpolates only on a rectangular grid
    Can be used to make the grid more densed or vice versa

    Parameters
    ----------
    iFile : name of the input file  
    grid1Col : Column number to be used as grid 1  
    grid2Col : Column number to be used as grid2  
    newGrid1 : new number of grid for grid1  
    newGrid2 :  new number of grid for grid2  
    '''

    g1 = np.unique(data[:,grid1Col])
    g2 = np.unique(data[:,grid2Col])
    c1 = g1.shape[0]
    c2 = g2.shape[0]


    ng1 = np.linspace(g1.min(),g1.max(),newGrid1)
    ng2 = np.linspace(g2.min(),g2.max(),newGrid2)
    ng1m, ng2m =np.meshgrid(ng1, ng2)


    result = []
    for i in range(data.shape[1]):
        if i==grid1Col:
            res = ng1m.reshape(-1)
        elif i==grid2Col:
            res = ng2m.reshape(-1)
        else:
            res = RectBivariateSpline(g1,g2,data[:,i].reshape(c1,c2))(ng1, ng2).reshape(-1)
        result.append(res)
    return np.column_stack(result)







def writeFile(data, file, fc=0):
    #writes data as fc column wise
    tp_list = np.unique(data[:,fc])
    file = open(file,"wb")
    for tp in tp_list:
        dat = data[data[:,fc]==tp]
        np.savetxt( file, dat ,delimiter="\t", fmt="%.8f")
        file.write("\n")
    file.close()

