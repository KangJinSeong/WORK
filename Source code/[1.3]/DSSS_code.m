clc; clear; close all

% DSSS(Direct Sequence Spread Spectrum)
% Signal Processing code
% By Kibae Lee (Kyungwon)
% 2020.10.08

%% DSSS Signal Gen.
Fs = 1e6; % Sampling Frequency

% == Modulation parameter == %
Rc = 1/(0.125e-3); % Chip rate
n = 8; % Number of LFSR for M-sequence

[Tc, BW, m, Ts] = ModSET(Rc, 8); % ModSET(Rc(ChipRate), n(#.LFSR))
% Tc : Chip duration [sec]
% BW : Bandwidth of PN-code [Hz]
% m : m-seqeunce length
% Ts : Symbol duration [sec]

% PN-code Init data
inidata0 = [1 0 0 0 0 0 0 0];
inidata1 = [0 0 0 1 0 0 0 0];

fc = Rc*4; % Carrier frequency
Modi = 5; % Modulation index
Tx_code = [0 1]; % Transmit code

% == Modulation == %
Tx_SIG = BitSeqGen(Tx_code, Fs*Ts); % Tx.code sequence generation
t0 = 0:1/Fs:(size(Tx_SIG,2)-1)/Fs; % Tx. time
taps0 = [8 7 6 1]; % Taps for bit0
taps1 = [8 5 3 1]; % Taps for bit1
[M_Seq0, M_Seq1] = MseqGen(taps0, taps1, inidata0, inidata1, 1, n); % M-sequence Gen.
[CODE_SIG, bit_sample] = CodeSigGen(Fs, Rc, Tx_code, Tx_SIG, M_Seq0, M_Seq1); % Code signal
Sc = Modi*sin(2*pi*fc*t0); % Carrier signal
TSig0 = CODE_SIG.*Sc; % Trasmit signal

%% DSSS Signal Processing.
Sr = TSig0; % Received signal

% == Source signal generation == %
S_M_Seq0 = BitSeqGen(M_Seq0, bit_sample); % Sequence Gen. for bit 0
S_M_Seq1 = BitSeqGen(M_Seq1, bit_sample); % Sequence Gen. for bit 1
ts = 0:1/Fs:(size(S_M_Seq0,2)-1)/Fs; % Symbol time
Sc0 = Modi*sin(2*pi*fc*ts); % Carrier signal
Source0 = ones(1, length(S_M_Seq0)).*S_M_Seq0.*Sc0; % Source signal for bit 0
Source1 = ones(1, length(S_M_Seq1)).*S_M_Seq1.*Sc0; % Source signal for bit 1

% == Filter Coefficient == %
Num0 = Source0(end:-1:1); Num1 = Source1(end:-1:1);
Out0 = filter(Num0,1,Sr); Out1 = filter(Num1,1,Sr);