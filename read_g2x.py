#!/usr/bin/env python
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
sys.modules[__name__].__dict__.clear()
import os
os.system('clear')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
__author__ = "Antoine Lucas"
__copyright__ = "Copyright 2016, Antoine Lucas"
__license__ = "GPL"
__version__ = "0.0.1"
__status__ = "Prototype"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import csv
import numpy
import matplotlib
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_g2xfield(filename,field,refine):

    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        data = list(reader)
    label = data[1]
    label = label[field]
    label=label.decode("utf-8")
    #print label
    data=data[2:]
    row_count = len(data[0])
    line_count = len(data)
    grid = numpy.empty((line_count,row_count))
    grid[:] = numpy.NAN
    ii=0
    while not 'Node' in data[ii]:
        grid[ii,:] = data[ii]
        ii=ii+1;

    grid=grid[0:ii,:]


    while not 'Element' in data[ii]:
        ii=ii+1

    kk=0

    triangle = numpy.zeros((len(data)-ii-1,3))
    ii=ii+1
    while  ii < len(data):
        tmp=data[ii]
        triangle[kk,:] = tmp[1:]
        kk=kk+1
        ii=ii+1

    triangle = triangle.astype(int)-1
    triang = tri.Triangulation(grid[:,1], grid[:,2],triangle)
    if refine:
        refiner = tri.TriRefiner(triang)
        triang, z = refiner.refine_field(z, subdiv=refine)

    z=grid[:,field]
    return z, triang,label




filename="7_Slope_Stability_-_Short_Term_Strains.csv"
filename2="7_Slope_Stability_-_Short_Term_Displacements.csv"

pngfile=filename + ".png"
pdffile=filename + ".pdf"

field=3
refine=0;

[exx,triang,label]=get_g2xfield(filename,field,refine)


[ux,triang,labelux]=get_g2xfield(filename2,3,refine)
[uy,triang,labeluy]=get_g2xfield(filename2,4,refine)
[u,triang,labelu]=get_g2xfield(filename2,5,refine)


# field we want to plot later on:
z=exx
#vecx=ux/u;
#vecy=uy/u;
dlev=(max(z)-min(z))/256


# Display options:
plotvec=True  # Display vector field
plotgrid=True  # Display grid
plottri=True   # Display tri
plotcont=False  # Display contour
usetex=False    # Use TeX
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Plot the triangulation and the high-res iso-contours
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

levels = np.arange(min(z), max(z), dlev)
#levels = np.arange(-0.5,1,1./256)
#print levels
print min(z), max(z)
cmap = cm.get_cmap(name='magma', lut=None)


fig=plt.figure(figsize=(20,8))
ax=plt.gca()
plt.gca().set_xlim([5, 25])

if usetex:
    plt.rc('text', usetex=True)
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

plt.gca().set_aspect('equal')
plt.title("Slope stability on the short term for Vesta Landsliding")



if plotgrid:
    if plottri:
        plt.triplot(triang, lw=0.2, color='0.1',zorder=90)
    else:
        plt.triplot(triang, lw=0.2, color='0.1',zorder=90)


print min(u), max(u),numpy.mean(u)
if plotvec:
    vecx=ux ##/u;
    vecy=uy ##/u;
    plt.quiver(triang.x, triang.y, vecx, vecy,color='cyan',zorder=100)


    #           scale=100,headlength=30,headwidth=30)
           #units='xy', scale=1000, zorder=1, color='blue',
           #width=1, headwidth=0.1, headlength=0.1)


if plotcont:
    plt.tricontour(triang, z, levels=[0.25],
            #colors=['0.25', '0.5', '0.5', '0.5', '0.5'],
            cmap=cmap,
            linewidths=[1.0],zorder=50)


if plottri:
    aa=1.0
    im=plt.tricontourf(triang,z, levels=levels, cmap=cmap,alpha=aa)
    divider = make_axes_locatable(ax)

    cax = divider.append_axes("right", size="5%", pad=0.15)
    plt.colorbar(im, cax=cax)
    plt.title(label)


fig.savefig(pngfile)
fig.savefig(pdffile)

plt.show()
