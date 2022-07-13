function [TSig0] = FHSS_SIGGEN(Tx_code, Freq0, Freq1, Tc, t0)
% M-seqeunce generation (PN-code) for FHSS
% 2020.04.09. KLEE

TSig0 = [];
for i = 1:size(Tx_code, 1)
    TSigs = [];
    phi = 0;
    for ii = 1:size(Tx_code, 2)
        if Tx_code(i,ii) < 1 % bit 0
            for k = 1:size(Freq0, 2)
                if ii < 2 && k < 2
                    TSig = sin(2*pi*Freq0(i,k)*t0 + phi);
                    phi = 2*pi*Freq0(i,k)*Tc + phi;
                else
                    TSig = sin(2*pi*Freq0(i,k)*t0(2:end) + phi);
                    phi = 2*pi*Freq0(i,k)*Tc + phi;
                end
                TSigs = [TSigs TSig];
            end
        else
            for k = 1:size(Freq1, 2) % bit 1
                if ii < 2 && k < 2
                    TSig = sin(2*pi*Freq0(i,k)*t0 + phi);
                    phi = 2*pi*Freq0(i,k)*Tc + phi;
                else
                    TSig = sin(2*pi*Freq0(i,k)*t0(2:end) + phi);
                    phi = 2*pi*Freq1(i,k)*Tc + phi;
                end
                TSigs = [TSigs TSig];
            end
        end
    end
    TSig0 = [TSig0; TSigs];
end