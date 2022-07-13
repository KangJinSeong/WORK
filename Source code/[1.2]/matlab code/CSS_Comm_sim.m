% Underwater Communication Matlab code
% CSS (Chirp Spread Spectrum)
% 2020.06.29 _ K.LEE (Kyungwon Industry)

clc; clear; close all;
%% Chirp signal gen.
Fs = 96e3; % Sampling Frequency (Hz)
t0 = 0:1/Fs:128e-3; % Symbol duration (128ms)
source0 = chirp(t0,30e3,128e-3,34e3); % Source signal for bit 0 (up-chirp)
source1 = chirp(t0,34e3,128e-3,30e3); % Source signal for bit 1 (down-chirp)
r_t = [source0, source1]; % received signal : message [0 1]

%% Signal Processing
% Cross-Correlation for bit 0 (Up-chirp)
Coeff0 = source0(end:-1:1); % Reverse 1D array for bit 0
u0 = filter(Coeff0,1,r_t); % Cross-Correlation for bit0

% Cross-Correlation for bit 1 (Down-chirp)
Coeff1 = source1(end:-1:1); % Reverse 1D array for bit 1
u1 = filter(Coeff1,1,r_t); % Cross-Correlation for bit1

y0 = (abs(hilbert(u0))).^2 - (abs(hilbert(u1))).^2; % Hilbert envlope ^2, Whitenning
y = (-1) + (((y0 - min(y0)) * 2) / (max(y0) - min(y0))); % Normalization (Scailing -1 to 1)

% Peak & Valley detection
Thres = 0.7; distance = round(length(t0)/20);
[Pks, Psmp] = findpeaks(y,'MinPeakHeight',Thres,'MinPeakDistance',distance); % Peak detection
[Vls, Vsmp] = findpeaks(-y,'MinPeakHeight',Thres,'MinPeakDistance',distance); % Valley detection

Val0 = [Pks -Vls]; Smp0 = [Psmp Vsmp];
[~, ind] = sort(Smp0);
Values = Val0(ind); Samples = Smp0(ind); % Output : Peak & Valley value & sample number

%% Source save
% cd('C:\Users\kibae\OneDrive\바탕 화면\이기배\기가DSP\matlab code')
% dlmwrite('source0.txt', source0); dlmwrite('source1.txt', source1);
% dlmwrite('Coeff0.txt', Coeff0); dlmwrite('Coeff1.txt', Coeff1);