function [Seq] = BitSeqGen(Code, T0)
% Generating the bit sequence
% 2020.03.26. KLEE

for j = 1:size(Code, 1)
    q=1;
    for jj = 1:size(Code, 2)
        for jjj = 1:T0
            Seq(j,q) = Code(j,jj);
            q = q+1;
        end
    end
end