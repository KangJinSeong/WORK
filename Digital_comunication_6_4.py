'''
Date: 2021.11.24
Title: 누적분포 함수 예제 풀기
By: Kang Jin Seong
'''

from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def stepseq(n0,n1,n2):  #단위계단함수
    N = n2-n1+1 #데이터수
    n = np.arange(N)    #순서 시퀀스
    xn = np.zeros(N)    #데이터 어레이 설정
    for i in range(N): #단위계단시퀀스 생성
        if (i+n1) >= n0:
            xn[i] = 1
    return xn


t = [i for i in range(7)]
y = np.ones(len(t))/6
for i in range(len(y)):
    y[i] = y[i] * i
print(t)
print(y)

plt.figure()
plt.plot(t,y)
plt.show()