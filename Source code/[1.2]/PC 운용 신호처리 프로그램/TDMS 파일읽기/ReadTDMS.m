% TDMS File Reader
% K.Lee (Kyungwon)

clc; clear all; close all

Fs = 400e3; % Sampling frequency (Hz)

FileName = ['CSS_52dB_120m_4']; % 파일명
ReadFileName = strcat(FileName,'.tdms'); % TDMS 확장자 자동설정

cd('C:\...') % 파일위치
tempData = convertTDMS(0,ReadFileName); % 데이터 읽기

RawData = tempData.Data.MeasuredData(1,3).Data; % 수신신호 [r(t)]
bit0 = tempData.Data.MeasuredData(1,4).Data; % Up-Chirp에 대한 정합필터 출력 [y_u(t)]
bit1 = tempData.Data.MeasuredData(1,5).Data; % Down-Chirp에 대한 정합필터 출력 [y_d(t)]
OUT = tempData.Data.MeasuredData(1,6).Data; % 신호처리 최종출력 [u(t)]