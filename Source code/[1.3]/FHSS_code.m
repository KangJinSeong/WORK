clc; clear; close all;

% FHSS(Frequency Hopping Spread Spectrum)
% Signal Processing code
% By Kibae Lee (Kyungwon)
% 2020.10.08

%% FHSS Signal Gen.
Fs = 160e3; % Sampling Frequency

% == Modulation parameter == %
Rc = 1/(0.128e-3); % Chip rate
n = 8; % Number of LFSR for M-sequence

[Tc, BW, m, Ts] = ModSET(Rc, n); % ModSET(Rc(ChipRate), n(#.LFSR))
% Tc : Chip duration [sec]
% m : m-seqeunce length
% Ts : Symbol duration [sec]

% PN-code Init data
inidata0 = [1 0 0 0 0 0 0 0];
inidata1 = [0 0 0 1 0 0 0 0];

f_min = 30e3; % Mnimum Frequency
fs = 16; % Freqeuency resolution
BW = fs*m; % Spread Spectrum Bandwidth
Tx_code = [0 1]; % Transmit code

% == Modulation == %
Tx_SIG = BitSeqGen(Tx_code, Fs*Ts); % Tx.code sequence generation
t0 = 0:1/Fs:Tc; % Chip time
taps0 = [8 7 6 1]; % Taps for bit0
taps1 = [8 5 3 1]; % Taps for bit1
[M_Seq0, M_Seq1] = MseqGen2(taps0, taps1, inidata0, inidata1, 1, n); % M-sequence Gen.
Freq0 = f_min+((M_Seq0-1)*fs); Freq1 = f_min+((M_Seq1-1)*fs); % Freqeuncy Array

TSig0 = FHSS_SIGGEN(Tx_code, Freq0, Freq1, Tc, t0);

%% FHSS Signal Processing.
Sr = TSig0; % Received signal

% == Source signal generation == %
Source0 = FHSS_SIGGEN(0, Freq0, Freq1, Tc, t0); % Source signal for bit 0
Source1 = FHSS_SIGGEN(1, Freq0, Freq1, Tc, t0); % Source signal for bit 1

% == Filter Coefficient == %
Num0 = Source0(end:-1:1); Num1 = Source1(end:-1:1);
Out0 = filter(Num0,1,Sr); Out1 = filter(Num1,1,Sr);