function [Tc BW m Ts] = ModSET(Rc, n)
% Modulation parmeter setup
% DSSS(Direct Sequence Spread Spectrum)
% 2020.03.20. KLEE

% == Variable == %
% Tc : Chip duration [sec]
% BW : Bandwidth of PN-code [Hz]
% m : m-seqeunce length
% Ts : Symbol duration [sec]

Tc = 1/Rc;
BW = Rc/2;
m = (2^n)-1;
Ts = m*Tc;
end