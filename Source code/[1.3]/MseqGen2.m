function [M_Seq0, M_Seq1] = MseqGen2(taps0, taps1, inidata0, inidata1, Nt, n)
% M-seqeunce generation (PN-code) for FHSS
% 2020.04.09. KLEE

% == Input == %
% taps0 : Taps for bit0
% taps1 : Taps for bit1
% inidata : initial data
% Nt : Number of transmitter
% n : Number of LFSR

% == Output ==%
% M_Seq0 : M-sequence for bit0
% M_Seq1 : M-sequence for bit1

M_Seq0 = []; M_Seq1 = [];
for i  = 1:Nt
    M_Seq0 = [M_Seq0; mseq2(n, taps0(i,:), inidata0(i,:), 1)];
    M_Seq1 = [M_Seq1; mseq2(n, taps1(i,:), inidata1(i,:), 1)];
end