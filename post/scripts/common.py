#!/bin/python
import numpy as np
import get_namelist as nml

myblue=[51./255, 105./255, 169./255]
myred=[200./255, 90./255, 90./255]
fs = 12
xdir = 0
ydir = 1
zdir = 2

# Get decorrelation length
def get_lscale(y,Lvv):
    Ny = np.size(Lvv)
    i1 = np.argmin(abs(Lvv[:Ny/2]-thresh))
    i2 = np.argmin(abs(Lvv[Ny/2:]-thresh)) + Ny/2 
    L_int = abs(y[i1]-y[i2])
    return L_int

# Get 99% thickness
def get_L99(y,utilde):
    du = abs(utilde[0]-utilde[-1])
    utop = 0.99*du/2
    ubot = -0.99*du/2
    Ny = np.size(utilde)
    
    itop = np.argmin(abs(utilde[:Ny/2]-ubot))
    ibot = np.argmin(abs(utilde[Ny/2:]-utop)) + Ny/2
    L99 = (y[itop]-y[ibot])
    return L99, itop, ibot

# Thickness and growth rates
def get_dtheta(directory,time):
    filename_prefix = directory+'/shearlayer_'
    tlist,dtheta,rate = growth_rates(filename_prefix)
    idx = np.argmin(abs(tlist-time))
    return dtheta[idx]

def growth_rates(filename_prefix):
    fname = filename_prefix+'growth.dat'
    dat = np.fromfile(fname,dtype=float, count=-1, sep=' ')
    n = np.size(dat)
    nstats=3
    dat = np.reshape(dat,[n/nstats,nstats])
    time = dat[:,0]
    dtheta = dat[:,1]
    rate = dat[:,2]
    return time,dtheta,rate

def which_tID(tvec,t):
    tID = np.argmin(np.abs(tvec-t))
    return tID

# get centerline from Reynolds stresses (vector)
def get_centerline(directory,y,tID):
    nmodes = 10
    dat = np.fromfile( directory + 'shearlayer_Rij_%04d'%(tID)+'.dat',dtype=float, count=-1, sep=' ')
    n = np.size(dat)
    nstats=6
    dat = np.reshape(dat,[n/nstats,nstats]) 
    yc = 0
    for i in [0,1]:
        ic = np.argmax(smooth_modes(abs(dat[:,i]),nmodes))
        yc += y[ic]
    yc /= 2.    
    ic = np.argmin(abs(y-yc))
    return ic,y[ic]

def smooth_modes(f,nmodes):
    fhat = np.fft.fft(f)
    fhat[nmodes+1:-(nmodes+1):] = 0
    f = np.fft.ifft(fhat)
    return f
