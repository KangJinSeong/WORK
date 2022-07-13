function [mout] = mseq(stg, taps, inidata, n)

% M-sequence Generator
% By Kibae Lee

% stg: LFSR(Linear Feedback Shift Resister) 단 수
% taps: Register feedback 위치
% inidata: 초기값
% n: 출력 시퀀스 개수 (생략가능)
% mout: M-sequence 출력

if nargin < 4 % nargin: 함수의 입력 인자 개수
    n = 1;
end

mout = zeros(n, 2^stg-1);
fpos = zeros(stg, 1);

fpos(taps) = 1;

for ii = 1:2^stg-1
    mout(1,ii) = inidata(stg); % 출력 데이터 저장 공간
    num = mod(inidata*fpos,2); % 피드백 데이터 계산
    inidata(2:stg) = inidata(1:stg-1); % 레지스터 이동
    inidata(1) = num; % 피드백 데이터 반환
end

if n > 1
    for ii = 2:n
        mout(ii,:) = shift(mout(ii-1,:), 1, 0);
    end
end