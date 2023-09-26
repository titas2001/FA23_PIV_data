# -*- coding: utf-8 -*-
"""
Created on Mar 22 11:48:00 2023
@author: lasickas
"""

import os
import numpy as np
import scipy.io
from scipy import signal


#%% Set paths
globalFolderPath = '~GlobalDataFolderPath~' # eg.: C:\PIV\Gas\InsideFlow
folderPath = '~specificDataFolderPath~'     # eg.: \Test013\PreProc_Up\out_PaIRS
path = globalFolderPath+folderPath          # full path
filePaths = path+"\*.mat" 
case = 'open'                               # set case open/closed
diameterTH = '4mm'                          # set case diameter 4mm / 6mm / 8mm / 10mm 
window = 'Upstream'                         # observation window Upstream / Downstream

files = glob.glob(filePaths)
NN=len(files)-2
#%% Calibrate and initialise arrays
calibration = 56.111111111  
Fs = 15569  # Hz
dt = 1/Fs
T = 1/Fs


mat = scipy.io.loadmat(path + '\out_00003.mat') # use single data point to set the array size
utO = mat["U"]
vtO = mat["V"]
xt = mat["X"]
yt = mat["Y"]
J,I = utO.shape

xl = xt[0,:]/calibration
yl = yt[:,0]/calibration
Xl = xt/calibration
Yl = yt/calibration

mhu = 1.8100e-05
dx = (Xl[0,1]-Xl[0,0])/1000 # mm -> m
#%% Load Data
fi = np.zeros((J, I, NN))
ui = np.zeros((J, I, NN))
vi = np.zeros((J, I, NN))
for pp in range(NN):
    # print(pp)
    name = str(pp).rjust(5, '0')
    mat = scipy.io.loadmat(path+"\out_"+name+".mat")
    ut = mat["U"]
    vt = mat["V"]
    xt = mat["X"]
    yt = mat["Y"]
    ut = signal.convolve2d(ut, np.ones((4, 4))/16, mode='same', boundary='symm')
    vt = signal.convolve2d(vt, np.ones((4, 4))/16, mode='same', boundary='symm')
    ui[:, :, pp] = ut
    vi[:, :, pp] = vt
    