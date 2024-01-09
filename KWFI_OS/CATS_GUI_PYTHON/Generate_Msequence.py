'''
Date: 2024.01.9
Title: Msequence 생성 코드
By: Kang Jin seong
''' 

import numpy as np
from pylfsr import LFSR
import matplotlib.pyplot as plt
from scipy.signal import upfirdn
from scipy.fftpack import fft, ifft, fftshift, ifftshift
from scipy import signal
from matplotlib import font_manager, rc

def Mseq_GEN(order, index, taps):
        inidata = np.zeros(order)
        inidata[index] = 1
        inidata = list(inidata)
        mseq = LFSR(initstate=inidata, fpoly= taps)
        cyc = 2**(order)
        tempseq = mseq.runKCycle(cyc)
        return tempseq

