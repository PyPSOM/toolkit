%reset -f
import numpy as np
import matplotlib.pyplot as plt

from sympy import *
from sympy.series import fourier
from IPython.display import display, Math, Latex
import seaborn as sns
import pandas as pd
from cmocean import cm

from mpl_toolkits import mplot3d
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('png', 'pdf')

plt.ion()

######################################################
# Defining funtions

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

    # g = a*E**((-(z-b)**2)/(2*c**2))+d
    g = amplitude*E**((-(z-center)**2)/(2*std**2))+shelf_extention

    #  h = Max_depth + ((topo_func-np.min(topo_func))*(Min_depth-Max_depth))/(np.max(topo_func)-np.min(topo_func)) feature scaling
    # ky = {'b':0.75*Ly,'c':0.1*Ly,'a':0.3*Lx,'d':0.2*Lx,'z':y}
    # kx = {'b':g.subs(ky),'c':0.02*np.abs(Max_depth-Min_depth),'a':np.abs(Max_depth-Min_depth),'d':Max_depth,'z':x}

    ky = {'center':ky_param[1]*Ly,'std':ky_param[2]*Ly,'amplitude':ky_param[0]*Lx,'shelf_extention':ky_param[3]*Lx,'z':y}
    kx = {'center':g.subs(ky),'std':slope*np.abs(Max_depth-Min_depth),'amplitude':np.abs(Max_depth-Min_depth),'shelf_extention':Max_depth,'z':x}

    p = Piecewise(
        (Min_depth,(x<g.subs(ky))),
        (g.subs(kx),(x>=g.subs(ky))))

    D = lambdify((x,y),p)(xi,yi) # D antigo topo_func
    Ddx = (lambdify((x,y),diff(p,x))(xi,yi))
    Ddy = (lambdify((x,y),diff(p,y))(xi,yi))

    return D,Ddx,Ddy,xi,yi
def psom_grid_shelfbreak_seamount(Lx, Ly, Max_depth, Min_depth, res, slope , ky, ktx, kty):

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

    ky = {'center':ky_param[1]*Ly,'std':ky_param[2]*Ly,'amplitude':ky_param[0]*Lx,'shelf_extention':ky_param[3]*Lx,'z':y}
    kx = {'center':g.subs(ky),'std':slope*np.abs(Max_depth-Min_depth),'amplitude':np.abs(Max_depth-Min_depth),'shelf_extention':Max_depth,'z':x}

    kty = {'amplitude':kty_param[0]*Lx,'center':kty_param[1]*Ly,'std':kty_param[2]*Ly,'shelf_extention':kty_param[3]*Lx,'z':y}
    ktx = {'amplitude':ktx_param[0],'center':ktx_param[1]*Lx,'std':ktx_param[2]*Lx,'shelf_extention':ktx_param[3],'z':x}
    # ktx = {'amplitude':np.abs(Max_depth-Min_depth),'center':g.subs(kty),'std':slope*np.abs(Max_depth-Min_depth),'shelf_extention':Max_depth,'z':x}


    p = Piecewise(
        (1,(x<g.subs(ky))),
        (g.subs(kx),(x>=g.subs(ky)))
    )+g.subs(ktx)*g.subs(kty)
    # p = g.subs(kx)+g.subs(ktx)*g.subs(kty)

    D = lambdify((x,y),p)(xi,yi) # D antigo topo_func
    Ddx = (lambdify((x,y),diff(p,x))(xi,yi))
    Ddy = (lambdify((x,y),diff(p,y))(xi,yi))

    return D,Ddx,Ddy,xi,yi

# def psom_grid_shelfbreak_2seamount(Lx, Ly, Max_depth, Min_depth, res, slope , ky, ktx, kty, ktx1, kty1):

#     xi,yi = np.meshgrid(np.arange(0,Lx+res,res),
#                         np.arange(0,Ly+res,res))

#     x = Symbol('x')
#     y = Symbol('y')
#     z = Symbol('z')

#     amplitude = Symbol('amplitude')                 # a
#     center = Symbol('center')                       # b
#     std = Symbol('std')                             # c
#     shelf_extention = Symbol('shelf_extention')     # d

#     g = amplitude*E**((-(z-center)**2)/(2*std**2))+shelf_extention

#     ky = {'center':ky_param[1]*Ly,'std':ky_param[2]*Ly,'amplitude':ky_param[0]*Lx,'shelf_extention':ky_param[3]*Lx,'z':y}
#     kx = {'center':g.subs(ky),'std':slope*np.abs(Max_depth-Min_depth),'amplitude':np.abs(Max_depth-Min_depth),'shelf_extention':Max_depth,'z':x}

#     kty = {'amplitude':kty_param[0]*Lx,'center':kty_param[1]*Ly,'std':kty_param[2]*Ly,'shelf_extention':kty_param[3]*Lx,'z':y}
#     ktx = {'amplitude':ktx_param[0],'center':ktx_param[1]*Lx,'std':ktx_param[2]*Lx,'shelf_extention':ktx_param[3],'z':x}
#     # ktx = {'amplitude':np.abs(Max_depth-Min_depth),'center':g.subs(kty),'std':slope*np.abs(Max_depth-Min_depth),'shelf_extention':Max_depth,'z':x}
#     kty1 = {'amplitude':kty_param[0]*Lx,'center':kty_param[1]*Ly,'std':kty_param[2]*Ly,'shelf_extention':kty_param[3]*Lx,'z':y}
#     ktx1 = {'amplitude':ktx_param[0],'center':ktx_param[1]*Lx,'std':ktx_param[2]*Lx,'shelf_extention':ktx_param[3],'z':x}


#     p = Piecewise(
#         (1,(x<g.subs(ky))),
#         (g.subs(kx),(x>=g.subs(ky)))
#     )+g.subs(ktx)*g.subs(kty)+g.subs(ktx1)*g.subs(kty1)
    
#     # g.subs(ktx1)*g.subs(kty1)
#     # p = g.subs(kx)+g.subs(ktx)*g.subs(kty)

#     D = lambdify((x,y),p)(xi,yi) # D antigo topo_func
#     Ddx = (lambdify((x,y),diff(p,x))(xi,yi))
#     Ddy = (lambdify((x,y),diff(p,y))(xi,yi))

#     return D,Ddx,Ddy,xi,yi

def psom_grid_seamount(Lx, Ly, Max_depth, Min_depth, res, ktx1, kty1):
# nao ta funcinando
#********************************************************************************
# Grid_dimensions

Lx = 300                    # Length of the domain in y direction: units 'km'
Ly = 800                    # Length of the domain in y direction: units 'km'
Max_depth = -1200           # Maximum value of depth: should be <0 : units 'm'
Min_depth = -50             # Minimum value of depth: should be <0 : units 'm'
res = 2                     # Spatial resolution: units 'km'
#********************************************************************************

a = 0.8  # ampli
b = 0.5 # center
c = 0.01 # std
d = 0 # 

xi,yi = np.meshgrid(np.arange(0,Lx+res,res),
                    np.arange(0,Ly+res,res))

term1 = (xi-b)**2/2*c**2
term2 = (yi-b)**2/2*c**2

g = (a*np.exp(-(term1+term2)))+d

plt.figure(),plt.pcolormesh(xi,yi,g)
plt.axis('scaled')
_=plt.colorbar()

D = lambdify((x,y),p)(xi,yi) # D antigo topo_func
Ddx = (lambdify((x,y),diff(p,x))(xi,yi))
Ddy = (lambdify((x,y),diff(p,y))(xi,yi))

# return D,Ddx,Ddy,xi,yi


##############################################################################################
# seamomunt

# #********************************************************************************
# # Grid_dimensions

# Lx = 300                    # Length of the domain in y direction: units 'km'
# Ly = 800                    # Length of the domain in y direction: units 'km'
# Max_depth = -1200           # Maximum value of depth: should be <0 : units 'm'
# Min_depth = -50             # Minimum value of depth: should be <0 : units 'm'
# res = 2                     # Spatial resolution: units 'km'
# #********************************************************************************

# ktx1_param = [7.5,0.6,0.05,0.] 
# kty1_param = [0.5,0.55,0.03,0.] 

# slope = 0.02

# D,Ddx,Ddy,xi,yi = psom_grid_shelfbreak_2seamount(Lx, Ly, Max_depth, Min_depth, res, slope , ky_param, ktx_param, kty_param, ktx1_param, kty1_param)

# plot ****************************************
plt.figure()
plt.subplot(131)
plt.contourf(xi,yi,D,20)
plt.axis('scaled')
_=plt.colorbar()

plt.subplot(132)
plt.contourf(xi,yi,Ddy,20)
plt.axis('scaled')
_=plt.colorbar()

plt.subplot(133)
plt.contourf(xi,yi,Ddx,20)
plt.axis('scaled')
_=plt.colorbar()

plt.figure(),plt.plot(xi[220,:],D[220,:])






##############################################################################################
# shelf break--non-uniforme-- + 2 seamomunt

#********************************************************************************
# Grid_dimensions

Lx = 300                    # Length of the domain in y direction: units 'km'
Ly = 800                    # Length of the domain in y direction: units 'km'
Max_depth = -1200           # Maximum value of depth: should be <0 : units 'm'
Min_depth = -50             # Minimum value of depth: should be <0 : units 'm'
res = 2                     # Spatial resolution: units 'km'
#********************************************************************************

ky_param = [0.3,0.75,0.1,0.2]
ktx_param = [7.5,0.6,0.05,0.] 
kty_param = [0.5,0.55,0.03,0.] 
ktx1_param = [7.5,0.99,0.05,0.] 
kty1_param = [0.5,0.2,0.2,0.02] 

slope = 0.02

D,Ddx,Ddy,xi,yi = psom_grid_shelfbreak_2seamount(Lx, Ly, Max_depth, Min_depth, res, slope , ky_param, ktx_param, kty_param, ktx1_param, kty1_param)

# plot ****************************************
plt.figure()
plt.subplot(131)
plt.contourf(xi,yi,D,20)
plt.axis('scaled')
_=plt.colorbar()

plt.subplot(132)
plt.contourf(xi,yi,Ddy,20)
plt.axis('scaled')
_=plt.colorbar()

plt.subplot(133)
plt.contourf(xi,yi,Ddx,20)
plt.axis('scaled')
_=plt.colorbar()

plt.figure(),plt.plot(xi[220,:],D[220,:])

A PARTIR DAQUI TA OK, vale a pena apenas criar um filtro pra forcar nao ter plataforma, ou seja valores igual a zero serao min depth

##############################################################################################
# shelf break--non-uniforme-- + 1 seamomunt

#********************************************************************************
# Grid_dimensions

Lx = 300                    # Length of the domain in y direction: units 'km'
Ly = 800                    # Length of the domain in y direction: units 'km'
Max_depth = -1200           # Maximum value of depth: should be <0 : units 'm'
Min_depth = -50             # Minimum value of depth: should be <0 : units 'm'
res = 2                     # Spatial resolution: units 'km'
#********************************************************************************

ky_param = [0.3,0.75,0.1,0.2]
ktx_param = [7.5,0.6,0.05,0.] 
kty_param = [0.5,0.55,0.03,0.] 
slope = 0.02

D,Ddx,Ddy,xi,yi = psom_grid_shelfbreak_seamount(Lx, Ly, Max_depth, Min_depth, res, slope , ky_param, ktx_param, kty_param)

# plot ****************************************
plt.figure()
plt.subplot(131)
plt.contourf(xi,yi,D,20)
plt.axis('scaled')
_=plt.colorbar()

plt.subplot(132)
plt.contourf(xi,yi,Ddy,20)
plt.axis('scaled')
_=plt.colorbar()

plt.subplot(133)
plt.contourf(xi,yi,Ddx,20)
plt.axis('scaled')
_=plt.colorbar()

plt.figure(),plt.plot(xi[220,:],D[220,:])

##############################################################################################
# shelf break - uniforme (ampy_value shoulb be 0)

#********************************************************************************
# Grid_dimensions

Lx = 300                    # Length of the domain in y direction: units 'km'
Ly = 800                    # Length of the domain in y direction: units 'km'
Max_depth = -1200           # Maximum value of depth: should be <0 : units 'm'
Min_depth = -50             # Minimum value of depth: should be <0 : units 'm'
res = 2                     # Spatial resolution: units 'km'
#********************************************************************************

ky_param = [0.,0.75,0.1,0.2]
D,Ddx,Ddy,xi,yi = psom_grid_shelfbreak(Lx, Ly, Max_depth, Min_depth, res, 0.02, [ky_param])

# plot ****************************************
plt.figure()
plt.subplot(121)
plt.contourf(xi,yi,D,20)
plt.axis('scaled')
_=plt.colorbar()

plt.subplot(122)
plt.contourf(xi,yi,Ddx,20)
plt.axis('scaled')
_=plt.colorbar()

##############################################################################################
# shelf break - non-uniforme

#********************************************************************************
# Grid_dimensions

Lx = 300                    # Length of the domain in y direction: units 'km'
Ly = 800                    # Length of the domain in y direction: units 'km'
Max_depth = -1200           # Maximum value of depth: should be <0 : units 'm'
Min_depth = -50             # Minimum value of depth: should be <0 : units 'm'
res = 2                     # Spatial resolution: units 'km'
#********************************************************************************

ky_param = [0.3,0.75,0.1,0.2]
D,Ddx,Ddy,xi,yi = psom_grid_shelfbreak(Lx, Ly, Max_depth, Min_depth, res, 0.02, [ky_param])

# plot ****************************************
plt.figure()
plt.subplot(131)
plt.contourf(xi,yi,D,20)
plt.axis('scaled')
_=plt.colorbar()

plt.subplot(132)
plt.contourf(xi,yi,Ddy,20)
plt.axis('scaled')
_=plt.colorbar()

plt.subplot(133)
plt.contourf(xi,yi,Ddx,20)
plt.axis('scaled')
_=plt.colorbar()

############################################################################################################################################





























###########################################################################################################################################################
######################################################
# 1D 

a = 0.8
b = 0.5
c = 0.1
x = np.linspace(0,1,100)
g = a*np.exp(-(x-b)**2/(2*c)**2)

plt.figure(),plt.plot(x,g)



######################################################
# 2D Seamount - topography

a = 0.8
b = 0.5
c = 0.01
d = 10
x = np.linspace(0,1,100)
y = np.linspace(0,1,100)
xx,yy = np.meshgrid(x,y)

term1 = (xx-b)**2/2*c**2
term2 = (yy-b)**2/2*c**2

g = (a*np.exp(-(term1+term2)))+d

plt.figure(),plt.pcolormesh(xx,yy,g)
plt.axis('scaled')
_=plt.colorbar()


######################################################
# errado - parece que tem um seamount longo em y (barreira) 

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')

g = a*E**((-(z-b)**2)/(2*c**2))+d

ky = {
'b':0.6,
'c':0.1,
'a':0.2,
'd':0.1,
'z':y
}

kx = {
'b':0.6,
'c':0.1,
'a':0.2,
'd':0.1,
'z':x
}

p = Piecewise(
    (1,(x<g.subs(ky))),
    (g.subs(kx),(x>=g.subs(ky))))


xi,yi = np.meshgrid(np.linspace(0,1,100),
                    np.linspace(0,1,100))

plt.figure()
plt.contourf(xi,yi*2,lambdify((x,y),p)(xi,yi),20)
plt.axis('scaled')
_=plt.colorbar()

######################################################
# shelf break
# b de ky desloca o banco meridionalmente
ky = {
'b':1.8,
'c':0.1,
'a':0.2,
'd':0.1,
'z':y
}

kx = {
'b':g.subs(ky),
'c':0.1,
'a':1,
'd':0,
'z':x
}

p = Piecewise(
    (1,(x<g.subs(ky))),
    (g.subs(kx),(x>=g.subs(ky))))

xi,yi = np.meshgrid(np.linspace(0,1,100),
                    np.linspace(0,1,100))


plt.figure()
plt.contourf(xi,yi*2,lambdify((x,y),p)(xi,yi),20)
plt.axis('scaled')
_=plt.colorbar()



######################################################
# Shelf-break + 1 seamount

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')


g = a*E**((-(z-b)**2)/(2*c**2))+d


ky = {
'b':0.6,
'c':0.1,
'a':0.2,
'd':0.1,
'z':y
}

kx = {
'b':g.subs(ky),
'c':0.1,
'a':1,
'd':0,
'z':x
}

ktx = {
'b':0.6,
'c':0.05,
'a':0.5,
'd':0,
'z':x
}

kty = {
'b':0.2,
'c':0.03,
'a':0.5,
'd':0,
'z':y
}

p = Piecewise(
    (1,(x<g.subs(ky))),
    (g.subs(kx),(x>=g.subs(ky)))
)+g.subs(ktx)*g.subs(kty)
# p = g.subs(kx)+g.subs(ktx)*g.subs(kty)

# p2 = g.subs()


display(Math(latex(Eq(Symbol('f(x,y)'),p))))


# g.subs(ky)

xi,yi = np.meshgrid(np.linspace(0,1,100),
                    np.linspace(0,1,100))


plt.contourf(xi,yi*2,lambdify((x,y),p)(xi,yi),20)
plt.axis('scaled')
_=plt.colorbar()

