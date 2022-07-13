function [CODE_SIG, bit_sample] = CodeSigGen(Fs, Rc, Tx_code, Tx_SIG, M_Seq0, M_Seq1)
% Code Signal Generation with PN-code
% 2020.10.08. KLEE

bit_sample = round(Fs*(1/Rc));
PNCODE0 = []; PNCODE1 = [];
for k = 1:size(Tx_code, 2)
    PNCODE0 = [PNCODE0 M_Seq0];
    PNCODE1 = [PNCODE1 M_Seq1];
end
PN_SIG0 = BitSeqGen(PNCODE0, bit_sample);
PN_SIG1 = BitSeqGen(PNCODE1, bit_sample);
CODE_SIG = ((((-Tx_SIG+1).*PN_SIG0)+(Tx_SIG.*PN_SIG1))*2-1);