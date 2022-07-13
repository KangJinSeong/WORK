% TDMS File Reader
% K.Lee (Kyungwon)

clc; clear all; close all

Fs = 400e3; % Sampling frequency (Hz)

FileName = ['CSS_52dB_120m_4']; % ���ϸ�
ReadFileName = strcat(FileName,'.tdms'); % TDMS Ȯ���� �ڵ�����

cd('C:\...') % ������ġ
tempData = convertTDMS(0,ReadFileName); % ������ �б�

RawData = tempData.Data.MeasuredData(1,3).Data; % ���Ž�ȣ [r(t)]
bit0 = tempData.Data.MeasuredData(1,4).Data; % Up-Chirp�� ���� �������� ��� [y_u(t)]
bit1 = tempData.Data.MeasuredData(1,5).Data; % Down-Chirp�� ���� �������� ��� [y_d(t)]
OUT = tempData.Data.MeasuredData(1,6).Data; % ��ȣó�� ������� [u(t)]