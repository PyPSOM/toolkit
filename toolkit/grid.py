############################################################################
# #
#  Further Information:
#  link git hub
#
#  PSOM_pytools is free toolbox written in python to provide
#  an easely visualization and dynamical analysis from PSOM output
#
#  PSOM_pytools is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# #  e-mail:cauezlazaneo@usp.br
################################################################################
# -*- coding: utf-8 -*-
%reset -f
################################################################################
# Importing packages ###########################################################

import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from sympy.series import fourier
from IPython.display import display, Math, Latex
import seaborn as sns
import pandas as pd
from cmocean import cm
from mpl_toolkits import mplot3d

################################################################################
# Defining funtions ############################################################

def psom_grid_shelfbreak(Lx, Ly, Max_depth, Min_depth, res, slope, ky):

    '''   example: ky_param = [ampy_value=0, centery_value=0.75, stdy_value=0.1, shelf_ext_value=0.2] '''

    xi,yi = np.meshgrid(np.arange(0,Lx+res,res),
                        np.arange(0,Ly+res,res))

    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    amplitude = Symbol('amplitude')
    center = Symbol('center')
    std = Symbol('std')
    shelf_extention = Symbol('shelf_extention')

    g = amplitude*E**((-(z-center)**2)/(2*std**2))+shelf_extention

    ky = {'center':ky_param[1]*Ly,'std':ky_param[2]*Ly,'amplitude':ky_param[0]*Lx,'shelf_extention':ky_param[3]*Lx,'z':y}
    kx = {'center':g.subs(ky),'std':slope*np.abs(Max_depth-Min_depth),'amplitude':np.abs(Max_depth-Min_depth),'shelf_extention':Max_depth,'z':x}

    p = Piecewise(
        (Min_depth,(x<g.subs(ky))),
        (g.subs(kx),(x>=g.subs(ky))))

    display(Math(latex(Eq(Symbol('f(x,y)'),p))))

    D = lambdify((x,y),p)(xi,yi) # D antigo topo_func
    Ddx = (lambdify((x,y),diff(p,x))(xi,yi))
    Ddy = (lambdify((x,y),diff(p,y))(xi,yi))
    D = D*1e3

    return D,Ddx,Ddy,xi,yi
def psom_grid_seamount(Lx, Ly, Max_depth, Min_depth, res, ktx_param, kty_param):

    xi,yi = np.meshgrid(np.arange(0,Lx+res,res),
                        np.arange(0,Ly+res,res))

    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    amplitude = Symbol('amplitude')                 # a
    center = Symbol('center')                       # b
    std = Symbol('std')                             # c
    shelf_extention = Symbol('shelf_extention')     # d

    g = amplitude*E**((-(z-center)**2)/(2*std**2))+shelf_extention
    dz = np.abs(Max_depth-Min_depth)

    fg = []
    if len(kty_param)==len(ktx_param):
        for i in range(len(kty_param)):
            kty = {'amplitude':kty_param[i][0],'center':kty_param[i][1]*Ly,'std':kty_param[i][2]*Ly,'shelf_extention':kty_param[i][3],'z':y}
            ktx = {'amplitude':ktx_param[i][0],'center':ktx_param[i][1]*Lx,'std':ktx_param[i][2]*Lx,'shelf_extention':ktx_param[i][3],'z':x}

            fg.append(g.subs(kty)*g.subs(ktx)*dz)

        f_sum = np.sum(np.array(np.array(fg)))

        f = f_sum -(dz-Min_depth)

        D = lambdify((x,y),f)(xi,yi) # D antigo topo_func
        Ddx = (lambdify((x,y),diff(f,x))(xi,yi))
        Ddy = (lambdify((x,y),diff(f,y))(xi,yi))
        D = D*1e3

    else:
        print('ERROR')

    return D,Ddx,Ddy,xi,yi
def psom_grid_shelfbreak_seamount(Lx, Ly, Max_depth, Min_depth, res, slope, ky_param, ktx_param, kty_param):

    xi,yi = np.meshgrid(np.arange(0,Lx+res,res),
                        np.arange(0,Ly+res,res))

    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    amplitude = Symbol('amplitude')
    center = Symbol('center')
    std = Symbol('std')
    shelf_extention = Symbol('shelf_extention')

    g = amplitude*E**((-(z-center)**2)/(2*std**2))+shelf_extention

    ky = {'center':ky_param[1]*Ly,'std':ky_param[2]*Ly,'amplitude':ky_param[0]*Lx,'shelf_extention':ky_param[3]*Lx,'z':y}
    kx = {'center':g.subs(ky),'std':slope*np.abs(Max_depth-Min_depth),'amplitude':np.abs(Max_depth-Min_depth),'shelf_extention':Max_depth,'z':x}

    p = Piecewise(
        (Min_depth,(x<g.subs(ky))),
        (g.subs(kx),(x>=g.subs(ky))))

    dz = np.abs(Max_depth-Min_depth)
    fg = []
    if len(kty_param)==len(ktx_param):
        for i in range(len(kty_param)):
            kty = {'amplitude':kty_param[i][0],'center':kty_param[i][1]*Ly,'std':kty_param[i][2]*Ly,'shelf_extention':kty_param[i][3],'z':y}
            ktx = {'amplitude':ktx_param[i][0],'center':ktx_param[i][1]*Lx,'std':ktx_param[i][2]*Lx,'shelf_extention':ktx_param[i][3],'z':x}

            fg.append(g.subs(kty)*g.subs(ktx)*dz)

        f_sum = np.sum(np.array(np.array(fg)))

        fseamouts = f_sum #-(dz-Min_depth)

    f = p + fseamouts

    display(Math(latex(Eq(Symbol('f(x,y)'),f))))

    D = lambdify((x,y),f)(xi,yi) # D antigo topo_func
    Ddx = (lambdify((x,y),diff(f,x))(xi,yi))
    Ddy = (lambdify((x,y),diff(f,y))(xi,yi))
    D = D*1e3

    return D,Ddx,Ddy,xi,yi

################################################################################
# Case 1: Uniform shelf break ##################################################

#*******************************************************************************
# Grid_dimensions
Lx = 300                    # Length of the domain in y direction: units 'km'
Ly = 800                    # Length of the domain in y direction: units 'km'
Max_depth = -1.200              # Maximum value of depth: should be <0 : units 'm'
Min_depth = -0.050                # Minimum value of depth: should be <0 : units 'm'
res = 1                        # Spatial resolution: units 'km'
ky_param = [0.,0.,0.,0.2]
#********************************************************************************

D,Ddx,Ddy,xi,yi = psom_grid_shelfbreak(Lx, Ly, Max_depth, Min_depth, res, 20, ky_param)

# plot ****************************************
f, axes = plt.subplots(1, 2, sharex=True,sharey=True, figsize=(9.5, 6.5))
cf = axes[0].contourf(xi,yi,D,20)
axes[0].axis('scaled')
cbar = f.colorbar(cf,ax=axes[0])#,extend='both')
axes[0].set_xlabel('x [km]')
axes[0].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'h [m]',fontsize=12)

cf = axes[1].contourf(xi,yi,Ddx,20)
axes[1].axis('scaled')
cbar = f.colorbar(cf,ax=axes[1])#,extend='both')
axes[1].set_xlabel('x [km]')
axes[1].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'$\frac{\partial h}{\partial x}$',fontsize=12)

plt.figure()
for i in range(int(Ly/res)):
    plt.plot(xi[i,:],D[i,:])

##############################################################################################
# Case 2: shelf break - non-uniforme
#********************************************************************************
# Grid_dimensions

Lx = 300                    # Length of the domain in y direction: units 'km'
Ly = 800                    # Length of the domain in y direction: units 'km'
Max_depth = -1.200           # Maximum value of depth: should be <0 : units 'km'
Min_depth = -0.050             # Minimum value of depth: should be <0 : units 'km'
res = 1                     # Spatial resolution: units 'km'
ky_param = [0.3,0.75,0.1,0.3]
#********************************************************************************

D,Ddx,Ddy,xi,yi = psom_grid_shelfbreak(Lx, Ly, Max_depth, Min_depth, res, 25, ky_param)

# plot ****************************************
f, axes = plt.subplots(1, 3, sharex=True,sharey=True, figsize=(12, 6.5))
cf = axes[0].contourf(xi,yi,D,20)
axes[0].axis('scaled')
cbar = f.colorbar(cf,ax=axes[0])#,extend='both')
axes[0].set_xlabel('x [km]')
axes[0].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'h [m]',fontsize=8)

cf = axes[1].contourf(xi,yi,Ddy,20)
axes[1].axis('scaled')
cbar = f.colorbar(cf,ax=axes[1])#,extend='both')
axes[1].set_xlabel('x [km]')
axes[1].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'$\frac{\partial h}{\partial y}$',fontsize=8)

cf = axes[2].contourf(xi,yi,Ddx,20)
axes[2].axis('scaled')
cbar = f.colorbar(cf,ax=axes[2])#,extend='both')
axes[2].set_xlabel('x [km]')
axes[2].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'$\frac{\partial h}{\partial x}$',fontsize=8)

plt.figure()
for i in range(int(Ly/res)):
    plt.plot(xi[i,:],D[i,:])

##############################################################################################
# Case 3: a) single seamount
#********************************************************************************

Lx = 300                    # Length of the domain in y direction: units 'km'
Ly = 800                    # Length of the domain in y direction: units 'km'
Max_depth = -1.200           # Maximum value of depth: should be <0 : units 'm'
Min_depth = -0.050             # Minimum value of depth: should be <0 : units 'm'
res = 1                     # Spatial resolution: units 'km'

kty_param = [[1,0.8,0.02,0]]
ktx_param = [[1,0.8,0.02,0]]


D,Ddx,Ddy,xi,yi = psom_grid_seamount(Lx, Ly, Max_depth, Min_depth, res, kty_param, kty_param)

# plot ****************************************
f, axes = plt.subplots(1, 3, sharex=True,sharey=True, figsize=(12, 6.5))
cf = axes[0].contourf(xi,yi,D,20)
axes[0].axis('scaled')
cbar = f.colorbar(cf,ax=axes[0])#,extend='both')
axes[0].set_xlabel('x [km]')
axes[0].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'h [m]',fontsize=8)

cf = axes[1].contourf(xi,yi,Ddy,20)
axes[1].axis('scaled')
cbar = f.colorbar(cf,ax=axes[1])#,extend='both')
axes[1].set_xlabel('x [km]')
axes[1].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'$\frac{\partial h}{\partial y}$',fontsize=8)

cf = axes[2].contourf(xi,yi,Ddx,20)
axes[2].axis('scaled')
cbar = f.colorbar(cf,ax=axes[2])#,extend='both')
axes[2].set_xlabel('x [km]')
axes[2].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'$\frac{\partial h}{\partial x}$',fontsize=8)

plt.figure()
for i in range(int(Ly/res)):
    plt.plot(xi[i,:],D[i,:])


# Case 3: a) multiple seamount
#********************************************************************************

kty_param = [[1,0.8,0.02,0],[1,0.5,0.02,0]]
ktx_param = [[1,0.8,0.02,0],[1,0.5,0.02,0]]

D,Ddx,Ddy,xi,yi = psom_grid_seamount(Lx, Ly, Max_depth, Min_depth, res, kty_param, kty_param)

# plot ****************************************
f, axes = plt.subplots(1, 3, sharex=True,sharey=True, figsize=(12, 6.5))
cf = axes[0].contourf(xi,yi,D,20)
axes[0].axis('scaled')
cbar = f.colorbar(cf,ax=axes[0])#,extend='both')
axes[0].set_xlabel('x [km]')
axes[0].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'h [m]',fontsize=8)

cf = axes[1].contourf(xi,yi,Ddy,20)
axes[1].axis('scaled')
cbar = f.colorbar(cf,ax=axes[1])#,extend='both')
axes[1].set_xlabel('x [km]')
axes[1].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'$\frac{\partial h}{\partial y}$',fontsize=8)

cf = axes[2].contourf(xi,yi,Ddx,20)
axes[2].axis('scaled')
cbar = f.colorbar(cf,ax=axes[2])#,extend='both')
axes[2].set_xlabel('x [km]')
axes[2].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'$\frac{\partial h}{\partial x}$',fontsize=8)

plt.figure()
for i in range(int(Ly/res)):
    plt.plot(xi[i,:],D[i,:])

##############################################################################################
# Case 4: a) un-uniform shelf break with multiples seamouts
#********************************************************************************
Lx = 300                    # Length of the domain in y direction: units 'km'
Ly = 800                    # Length of the domain in y direction: units 'km'
Max_depth = -1.200           # Maximum value of depth: should be <0 : units 'm'
Min_depth = -0.050             # Minimum value of depth: should be <0 : units 'm'
res = 1                     # Spatial resolution: units 'km'
slope = 20

# kty_param = [[1,0.8,0.02,0]]
# ktx_param = [[1,0.8,0.02,0]]

kty_param = [[0.5,0.5,0.02,0],[1,0.5,0.02,0]]
ktx_param = [[0.5,0.45,0.02,0],[1,0.8,0.02,0]]

ky_param = [0.3,0.75,0.1,0.3]

D,Ddx,Ddy,xi,yi = psom_grid_shelfbreak_seamount(Lx, Ly, Max_depth, Min_depth, res, slope, ky_param, ktx_param, kty_param)

# plot ****************************************
f, axes = plt.subplots(1, 3, sharex=True,sharey=True, figsize=(12, 6.5))
cf = axes[0].contourf(xi,yi,D,20)
axes[0].axis('scaled')
cbar = f.colorbar(cf,ax=axes[0])#,extend='both')
axes[0].set_xlabel('x [km]')
axes[0].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'h [m]',fontsize=8)

cf = axes[1].contourf(xi,yi,Ddy,20)
axes[1].axis('scaled')
cbar = f.colorbar(cf,ax=axes[1])#,extend='both')
axes[1].set_xlabel('x [km]')
axes[1].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'$\frac{\partial h}{\partial y}$',fontsize=8)

cf = axes[2].contourf(xi,yi,Ddx,20)
axes[2].axis('scaled')
cbar = f.colorbar(cf,ax=axes[2])#,extend='both')
axes[2].set_xlabel('x [km]')
axes[2].set_ylabel('y [km]')
cbar.ax.set_ylabel(r'$\frac{\partial h}{\partial x}$',fontsize=8)

plt.figure()
for i in range(int(Ly/res)):
    plt.plot(xi[i,:],D[i,:])

plt.figure()
plt.plot(D[400,:])
