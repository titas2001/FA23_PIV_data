# -*- coding: utf-8 -*-
"""
Created on Mar 22 11:48:00 2023
@author: lasickas
"""

import os
import numpy as np
import scipy.io
from scipy import signal
import glob

#%% Set paths
globalFolderPath = '~GlobalDataFolderPath~' # eg.: C:\PIV\Gas\InsideFlow
folderPath = '~specificDataFolderPath~'     # eg.: \Test013\PreProc_Up\out_PaIRS
path = globalFolderPath+folderPath          # Full path
filePaths = path+"\*.mat" 
""" for ploting:
case = 'open'                               # set case open/closed
diameterTH = '4mm'                          # set case diameter 4mm / 6mm / 8mm / 10mm 
window = 'Upstream'                         # observation window Upstream / Downstream
"""
files = glob.glob(filePaths)                # find all the files with .mat extension in the folder
NN=len(files)-2                             # Number of files
#%% Calibrate and initialise arrays
pixelScaling = 56.111111111  # pixels/mm
Fs = 15569  # Hz
dt = 1/Fs
T = 1/Fs


mat = scipy.io.loadmat(path + '\out_00003.mat') # use single data point to set the array size
utO = mat["U"]
vtO = mat["V"]
xt = mat["X"]
yt = mat["Y"]
J,I = utO.shape

# Set 
xl = xt[0,:]/pixelScaling
yl = yt[:,0]/pixelScaling
Xl = xt/pixelScaling
Yl = yt/pixelScaling

#%% Load Data

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
    
"""
    Now you have horizontal (ui) and vertical (vi) velocity arrays, with them you can do your processing
    For aligning the data on x-axis some shifting of data is needed:
            downstream x for plotting: 
                    4 mm:   xl[2:-2]-17.74+10.33+157
                    6 mm:   xl[2:-2]-19.42+10.33+157
                    8 mm:   xl[2:-2]-19.2+10.33+157
                    10 mm:  xl[2:-2]-19.02+10.33+157
                    157 mm is the distance from centre of the TH to the open end
                    10.33 mm is the distance from the centre of TH to the 0mm mark
            upstream x for plotting: 
                    4 mm:   xl-10.4769
                    6 mm:   xl-13.66
                    8 mm:   xl-13.7797
                    10 mm:  xl-13.0769
"""
    