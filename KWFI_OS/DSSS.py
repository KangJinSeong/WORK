'''
Date: 2022.11.18
Title: DSSS(Direct Sequence Spread Spectrum)
By: Kang Jin Seong
'''

import numpy as np
from pylfsr import LFSR
import matplotlib.pyplot as plt

class DSSS:
    def __init__(self):
        self.Fs = 1e6
        self.RC = 1/(125e-6)    # Chirp rate
        self.fc = self.RC * 4
        self.order = 8  # Numbere of LFSR for M-sequence
        self.inidata0 = [1,0,0,0,0,0,0,0]
        self.inidata1 = [0,0,0,1,0,0,0,0]
        self.taps0 = [8,7,6,1]
        self.taps1 = [8,5,3,1]
        self.TX_code = [0,1]
    
    def ModSET(self,Rc,order):
        Tc = 1/Rc   # Chirp duration[sec]
        BW = Rc/2   # Bandwidth of PN-code [Hz]
        m = (2**order)   # m-sequence length
        Ts = m* Tc  # Symbol duration[sec]
        return Tc,BW,m,Ts

    def BitSeqGen(self,Code,NS):    # NS: Number of sampling
        y = Code
        NS = int(NS)
        seq = []
        for i in y:
            seq += [i] * NS
        return seq 

    def mseq(self,taps,inidata,order):
        L = LFSR(initstate=inidata, fpoly= taps)
        tempseq = L.runKCycle(order)
        return tempseq

    def Mseqgen(self,taps0,taps1,inidata0,inidata1,m):
        M_seq0 = self.mseq(taps0, inidata0, m)
        M_seq1 = self.mseq(taps1, inidata1, m)
        return M_seq0, M_seq1

    def CodeSigGen(self,Fs, Tc, TX_code,TX_SIG, M_seq0, M_seq1):
        bit_sample = round(Fs *Tc)
        PNCODE0 = []
        PNCODE1 = []
        for i in range(len(TX_code)):
            PNCODE0.extend(M_seq0)
            PNCODE1.extend(M_seq1)
        PN_SIG0 = self.BitSeqGen(PNCODE0, bit_sample)
        PN_SIG1 = self.BitSeqGen(PNCODE1, bit_sample)
        PN_CODE = self.BitSeqGen(M_seq0, bit_sample)+self.BitSeqGen(M_seq1, bit_sample)
        PN_SIG0 = np.array(PN_SIG0)
        PN_SIG1 = np.array(PN_SIG1)
        TX_SIG = np.array(TX_SIG)

        CODE_SIG = (((TX_SIG*(-1)+1)*PN_SIG0) +(TX_SIG*PN_SIG1))*2-1
        return CODE_SIG, bit_sample, PN_SIG0, PN_CODE

    def main(self):
        a = self.mseq(self.taps0, self.inidata0, self.order)
        print(a, len(a))
        # Tc,BW,m,Ts = self.ModSET(self.RC,self.order)
        
        # TX_SIG = self.BitSeqGen(self.TX_code, self.Fs * Ts)
        # t = np.arange(start= 0, stop= len(TX_SIG)/self.Fs, step = 1/self.Fs)
        # M_seq0, M_seq1 = self.Mseqgen(self.taps0, self.taps1, self.inidata0, self.inidata1, m)
        # Code_sig, bit_sample, PN_SIG0 , PN_CODE = self.CodeSigGen(self.Fs, Tc, self.TX_code,TX_SIG, M_seq0, M_seq1)
        # # print(Code_sig.shape, t.shape)
        # sc = 5*np.sin(2*np.pi*self.fc*t[:-1])
        # TSIG = Code_sig * sc
        # print(BW, self.fc, Tc)
        # plt.figure()
        # plt.plot(t[:-1], TSIG, label = 'Modulation signal')
        # # plt.plot(t[:-1],TX_SIG,'r--', legend = 'TX_CODE')
        # plt.plot(t[:-1],PN_SIG0,'g-', label = 'PNCODE')
        # plt.xlabel('Time(sec)');plt.ylabel('Amplitude')
        # plt.legend()

        # plt.figure()
        # plt.plot(t[:-1],TX_SIG, 'r--',label = 'TX_CODE')
        # plt.plot(t[:-1],PN_CODE, label = 'PN_CODE')
        # plt.xlabel('Time(sec)');plt.ylabel('Amplitude')
        # plt.legend()
        # plt.tight_layout()



if __name__ == "__main__":
    print('START')
    A = DSSS()
    A.main()
    plt.show()