function [mout] = mseq2(stg, taps, inidata, n)

% M-sequence Generator
% By Kibae Lee

% stg: LFSR(Linear Feedback Shift Resister) �� ��
% taps: Register feedback ��ġ
% inidata: �ʱⰪ
% n: ��� ������ ���� (��������)
% mout: M-sequence ���

if nargin < 4 % nargin: �Լ��� �Է� ���� ����
    n = 1;
end

mout = zeros(n, 2^stg-1);
fpos = zeros(stg, 1);

fpos(taps) = 1;

inidata0 = bi2de(inidata,'left-msb');
for ii = 1:2^stg-1
    mout(1,ii) = inidata0; % ��� ������ ���� ����
    num = mod(inidata*fpos,2); % �ǵ�� ������ ���
    inidata(2:stg) = inidata(1:stg-1); % �������� �̵�
    inidata(1) = num; % �ǵ�� ������ ��ȯ
    inidata0 = bi2de(inidata,'left-msb');
end

if n > 1
    for ii = 2:n
        mout(ii,:) = shift(mout(ii-1,:), 1, 0);
    end
end