% Doppler Frequency Simulation
%clear all

%Water_Tx1ms_1
%Water_1m_0527_1
%Water1m_1ms_140531_4
%Water_1m_1ms_140605_2
%Water_1m_1ms_140605_1_3
%Water_1m_1ms_140605_2_3
%Water_1m_1ms_140605_4_1
%Water_1m_1ms_140609_MotorOff
%Water_1m_1ms_140609_MotorOn
%Water_1m_1ms_140609_Moving
%lake_3m_Tx_2ms_2
%Simulator_Test3
%lake_3m_Tx_2ms_SW140609_1
%lake_3m_Tx_2ms_SW140609_2
%lake_3m_Tx_2ms_1
%lake_3m_Tx_2ms_2
%lake_3p1m_Tx_3ms_2
%lake_3p1m_Tx_4ms_3
%lake_3p1m_Tx_5ms_1
%lake_4m_Tx_3ms_1
%lake_4m_Tx_3ms_2	% ????
%lake_4m_Tx_4ms_2
%lake_4m_Tx_5ms_2	% ????
%lake_4m_Tx_5ms_3
soyang_0611sw
%soyang_0612sw_1
%soyang_0612sw_2

Fs = 160000;
Fc = 40000;
Channel_N = 4;
Simul_Channel_N = 2;
Sample_N = 8192;

Decimation_N1 = 625;
Decimation_factor = 6;
Fft_factor = 6/Decimation_factor;
Df_resol = 20000/(3072);


bm_coef = blackman(4096*Fft_factor);

LPF_TAP_N = 64;
LPF_TAP_N2 = LPF_TAP_N/2;
lpf_tap = fir1(LPF_TAP_N-1, 0.10);
lpf_tap_r1 = lpf_tap(2:2:LPF_TAP_N);
lpf_tap_i1 = lpf_tap(1:2:LPF_TAP_N);

if 1
for i=1:32
	lpf_tap_r(i) = lpf_tap_r1(33-i);
	lpf_tap_i(i) = lpf_tap_i1(33-i);
end
end

clear rssi rssi1

%RSSI_SUM_N = 64;
RSSI_SUM_N = 16;
RSSI_OFFSET = 0;

cnt = 0;
start_flag = 0;
max_rssi = 0;

for i=1:Sample_N
	rssi(i) = sum(data(8*i-7:8*i-4))/4;
end

%figure(10),plot(rssi);

%load ('rssi1.mat','rssi1');
%rssi = 300*rssi1;

rssi_mean = mean(rssi);
%rssi_mean = mean(rssi(1:2048));
%rssi_sum = 0;
cnt = 0;
start_flag = 0;
max_rssi = 0;

rssi_sum = sum(rssi(1+RSSI_OFFSET:RSSI_SUM_N+RSSI_OFFSET));

max_rssi_sum = 0;
for i=(1+RSSI_OFFSET):(Sample_N-RSSI_SUM_N)
    rssi_sum = rssi_sum + rssi(i+RSSI_SUM_N)-rssi(i);
	rssi1(i) = rssi_sum / RSSI_SUM_N;
	if (rssi_sum > max_rssi_sum)
		max_rssi_sum = rssi_sum;
		ch_sum_max_index = i;
	end
end
if 0
max_rssi = max_rssi_sum / RSSI_SUM_N;
for i=max_index:-1:1
	%if (rssi1(i) < (rssi_mean+100))
	if (rssi1(i) < (max_rssi-100))
		%start_pos = i+20
        break;
	end
end
start_pos = i+25
%start_pos = i+50
for i=max_index:(Sample_N-RSSI_SUM_N)
	if (rssi1(i) < (max_rssi-100))
		%end_pos = i+10
        break;
	end
end
if (i >= (Sample_N-RSSI_SUM_N-10))
	end_pos = Sample_N-RSSI_SUM_N
else
	%end_pos = i+10
	end_pos = i-10
end
    
start_pos = 260
end_pos = 360
end
START_TH = 500;
END_TH = 500;

for n = 1:Channel_N
	clear rx 
	rx = data(n+Channel_N:8:Sample_N*Channel_N*2);
	rssi = data(n:8:Sample_N*Channel_N*2);

	% RSSI Detection
	rssi_mean = mean(rssi);
	%rssi_mean = mean(rssi(1:2048));
	%rssi_sum = 0;
	cnt = 0;
	start_flag = 0;
	max_rssi = 0;
	
	rssi_sum = sum(rssi(1+RSSI_OFFSET:RSSI_SUM_N+RSSI_OFFSET));
	
	max_rssi_sum = 0;
	for i=(1+RSSI_OFFSET):(Sample_N-RSSI_SUM_N)
	    rssi_sum = rssi_sum + rssi(i+RSSI_SUM_N)-rssi(i);
		rssi1(i) = rssi_sum / RSSI_SUM_N;
		if (rssi_sum > max_rssi_sum && i > 20)
			max_rssi_sum = rssi_sum;
			max_index = i;
		end
	end
	max_rssi = max_rssi_sum / RSSI_SUM_N;

	cnt = 0;
	for i=max_index:-1:1
		%if (rssi1(i) < (rssi_mean+100))
		%if (rssi1(i) < (max_rssi-400))
		if ((rssi1(i) < (max_rssi-START_TH)) || ((i > 16) && (rssi1(i) < (max_rssi-100)) && rssi1(i-16) > rssi1(i)))
			%start_pos = i+20
	        break;
		end
	end
	%start_pos = i+25
	start_pos = i+30
	cnt = 0;
	for i=max_index:(Sample_N-RSSI_SUM_N)
		if ((rssi1(i) < (max_rssi-END_TH)) || ((rssi1(i) < (max_rssi-100)) && rssi1(i+16) > rssi1(i)))
			%end_pos = i+10
	        break;
		end
	end
	if (i >= (Sample_N-RSSI_SUM_N-10))
		end_pos = Sample_N-RSSI_SUM_N
	else
		end_pos = i-15
		%end_pos = i-10
    end
if 0    
    echo_len = end_pos - start_pos;
    fill_len = (88-echo_len);
    if (echo_len < 84 && echo_len > 48)
        %start_pos = start_pos-fill_len;
        end_pos = end_pos+fill_len;
    end
end
	if (end_pos - start_pos < 84)
		if (rssi1(max_index)-rssi1(max_index+50) < 500) 
			max_index1 = max_index + 50;
			max_rssi1 = rssi1(max_index1);
			
			for i=max_index1:-1:1
				%if (rssi1(i) < (rssi_mean+100))
				%if (rssi1(i) < (max_rssi-400))
				if ((rssi1(i) < (max_rssi1-START_TH)) || ((i > 16) && (rssi1(i) < (max_rssi1-100)) && rssi1(i-16) > rssi1(i)))
					%start_pos = i+20
			        break;
				end
			end
			%start_pos = i+25
			start_pos = i+30
			
			for i=max_index1:(Sample_N-RSSI_SUM_N)
				if ((rssi1(i) < (max_rssi1-END_TH)) || ((rssi1(i) < (max_rssi1-100)) && rssi1(i+16) > rssi1(i)))
					%end_pos = i+10
			        break;
				end
			end
			if (i >= (Sample_N-RSSI_SUM_N-10))
				end_pos = Sample_N-RSSI_SUM_N
			else
				end_pos = i-15
				%end_pos = i-10
		    end
	    end
	end

	if (end_pos - start_pos < 84 && max_index > 50)
		if (rssi1(max_index)-rssi1(max_index-50) < 500) 
			max_index2 = max_index - 50;
			max_rssi2 = rssi1(max_index2);
			
			for i=max_index2:-1:1
				%if (rssi1(i) < (rssi_mean+100))
				%if (rssi1(i) < (max_rssi-400))
				if ((rssi1(i) < (max_rssi2-START_TH)) || ((i > 16) && (rssi1(i) < (max_rssi2-100)) && rssi1(i-16) > rssi1(i)))
					%start_pos = i+20
			        break;
				end
			end
			%start_pos = i+25
			start_pos = i+30
			
			for i=max_index2:(Sample_N-RSSI_SUM_N)
				if ((rssi1(i) < (max_rssi2-END_TH)) || ((rssi1(i) < (max_rssi2-100)) && rssi1(i+16) > rssi1(i)))
					%end_pos = i+10
			        break;
				end
			end
			if (i >= (Sample_N-RSSI_SUM_N-10))
				end_pos = Sample_N-RSSI_SUM_N
			else
				end_pos = i-15
				%end_pos = i-10
		    end
	    end
	end
    
    %start_pos = 500;
    %end_pos = 700;
	echo_sig = rx(start_pos:end_pos);
	%echo_sig = rx;
if 0
    b_rx_r = zeros(1,fix(length(echo_sig)/2)+LPF_TAP_N);
	b_rx_i = zeros(1,fix(length(echo_sig)/2)+LPF_TAP_N);
else
    b_rx_r = zeros(1,fix(length(echo_sig)/2));
	b_rx_i = zeros(1,fix(length(echo_sig)/2));    
end
if 0	
	for i = 1:fix(length(echo_sig)/4)
		b_rx_r(LPF_TAP_N/2+2*i-1) =  echo_sig(4*i-3);
		b_rx_i(LPF_TAP_N/2+2*i-1) = -echo_sig(4*i-2);
		b_rx_r(LPF_TAP_N/2+2*i-0) = -echo_sig(4*i-1);
		b_rx_i(LPF_TAP_N/2+2*i-0) =  echo_sig(4*i-0);
	end
else
	for i = 1:fix(length(echo_sig)/4)
		b_rx_r(2*i-1) =  echo_sig(4*i-3);
		b_rx_i(2*i-1) = -echo_sig(4*i-2);
		b_rx_r(2*i-0) = -echo_sig(4*i-1);
		b_rx_i(2*i-0) =  echo_sig(4*i-0);
    end    
end
	clear lpf_b_rx_r lpf_b_rx_i
	%for i=1:fix((length(b_rx_r)-LPF_TAP_N2)/3)-18
    if (fix((length(b_rx_r)-LPF_TAP_N2)/3 > 2))
        for i=1:fix((length(b_rx_r)-LPF_TAP_N2)/3)
            lpf_b_rx_r(i) = lpf_tap_r * b_rx_r(3*i-2:3*i-2+(LPF_TAP_N2-1))';
            lpf_b_rx_i(i) = lpf_tap_i * b_rx_i(3*i-2:3*i-2+(LPF_TAP_N2-1))';	 
            %lpf_b_rx_r(i) = lpf_tap_r * b_rx_r(3*(i+10)-2:3*(i+10)-2+(LPF_TAP_N2-1))';
            %lpf_b_rx_i(i) = lpf_tap_i * b_rx_i(3*(i+10)-2:3*(i+10)-2+(LPF_TAP_N2-1))';	 
        end
            lpf_b_rx = lpf_b_rx_r + j*lpf_b_rx_i;
    else
            lpf_b_rx_r = 0;
            lpf_b_rx_i = 0;
            lpf_b_rx = lpf_b_rx_r + j*lpf_b_rx_i;            
    end
            downsample6_out = conj(lpf_b_rx)';
        
	if length(downsample6_out) < 4096
		zero_pad_len = 4096-length(downsample6_out);
		if zero_pad_len > 100
			downsample6_out = [zeros(1,100) downsample6_out' zeros(1,4096-length(downsample6_out)-100)];
		else
			downsample6_out = [downsample6_out' zeros(1,4096-length(downsample6_out))];	
		end
		downsample6_out = downsample6_out';
	end
		windowing_out = downsample6_out .* bm_coef;
	
	fft_rx=abs(fft(rx,4096*Fft_factor));
	fft_out=abs(fft(windowing_out,4096*Fft_factor));
	temp_alg_out = [fft_out((4096*Fft_factor-1536)+1:4096*Fft_factor)' fft_out(1:1536)'];
	alg_out = temp_alg_out';
	
	rssi_buf = 10*ones(1,Sample_N);
	rssi_buf(start_pos:end_pos) = 10000*ones(1,end_pos-start_pos+1); 
	x_axis=([0:3072-1]*Df_resol+30000)';
	[val, idx] = max(alg_out);
	Df = (idx-1)*Df_resol+30000
	Int_Df = round(Df);
	if Df >= 40000.0
		figure(n)
		subplot(2,1,1)
		plot(rx), hold on, plot(rssi,'r'), plot(rssi_buf,'c'), title('Rx Sample & RSSI'), hold off
		subplot(2,1,2) 
		plot(x_axis, alg_out), hold on, plot(x_axis, alg_out, 'r.') 
		title(['CH',num2str(n),' Freq']), text(Df-4000,val-val*0.1,['Df=',num2str(Int_Df),'Hz']), hold off 
	else
		figure(n)
		subplot(2,1,1)
		plot(rx), hold on, plot(rssi,'r'), plot(rssi_buf,'c'), title('Rx Sample & RSSI'), hold off
		subplot(2,1,2)
		plot(x_axis, alg_out), hold on, plot(x_axis, alg_out, 'r.')
		title(['CH',num2str(n),' Freq']), text(Df+1000,val-val*0.1,['Df=',num2str(Int_Df),'Hz']), hold off 	
	end
end %for n = 0:Channel_N


