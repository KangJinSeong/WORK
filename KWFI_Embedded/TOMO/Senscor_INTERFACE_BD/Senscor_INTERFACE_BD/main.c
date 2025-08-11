/*
 Date: 2024.08.21
 Title: 센서 인터페이스 보드 V1.0
 Rev: Rev1
 By: Kang Jin seong
*/

#include <stdio.h>
#include <avr/io.h>
#include "UAT_Ver_3.h"
#include <util/delay.h>

/*
 자세센서 데이터 관련 변수 설정
*/
uint8_t ReadData[5] = {0x68, 0x04, 0x00, 0x04, 0x08};                // Angle Read Command
uint8_t ReceiveData[14] = {0x00,};                                   // Angle Receive Buffer Initialization

/*
 UART 통신 관련 출력 설정
*/
FILE OUTPUT = FDEV_SETUP_STREAM(UART_transmit, NULL, _FDEV_SETUP_WRITE);
FILE INPUT = FDEV_SETUP_STREAM(NULL, UART_receive, _FDEV_SETUP_READ);

int main(void)
{

	UART_init();
	/*
	 I/O Port 설정
	  1) TRX_CON1: 자세 센서 및 Coastal TMC Set 통신 관련 스위치 포트(PB3)
	  2) TRX_CON2: Coastal TMC Set 통신 관련 트렌시버 IC 제어 포트
	  3) RS232EN: 자세센서 통신 관련 트렌시버 IC 제어 포트
	*/
	DDRB |= 0x49;
	PORTB |= 0x01;
	/*
	 UART 출력 설정
	*/
	stdout = &OUTPUT;
	stdin = &INPUT;
	/*
	 변수 설정
	  1) V_rth: 온도센서로부터 읽은 전압 변수 값
	  2) V_pa: 압력센서로부터 읽은 전압 변수 값
	  3) k: V_rth 값을 저항 값으로 변경하기 위한 온도 센서 상수 K의 값
	*/
	float V_rth, V_pa;
	float Rth = 0;
	float k;
	float pa = 0;
	ADC_init(6);
	_delay_ms(3000);



	/* Replace with your application code */
	while (1)
	{	

		PORTB = 0x00;
		
		for(int i=0; i<5; i++) 
		{
			UART_transmit(ReadData[i]);                                          // Read Angle command
		}


		PORTB = 0x00;
		LINDAT = 0;
		LINSIR &= ~( 1 << LRXOK);
		for(int j=0; j<14; j++)
		{
			ReceiveData[j] = UART_receive(); 
		}

		_delay_ms(100);
		ADC_EN();
		_delay_ms(100);
		ADMUX = ((ADMUX & 0xE0) | 0x06);
		_delay_ms(100);
		V_rth = (read_ADC()*5.22)/1023;
		k = V_rth/5.11;
		Rth = (k/(1-k)) * 10000;

		_delay_ms(100);
		ADMUX = ((ADMUX & 0xE0) | 0x03);
		_delay_ms(100);
		V_pa = (read_ADC()*5.22)/1023;
		pa = V_pa;
		
		ADC_OFF();
		_delay_ms(300);
 		PORTB = 0x48;
		_delay_ms(300);
		printf("START");
		printf("\r\n");
		for(int p=0; p<14; p++)
		{-
			printf("%d", ReceiveData[p]);
		}
		printf("\r\n");
		DCM250B_UartProc(ReceiveData);
		printf(">RTH=%f\r\n", Rth);
		printf(">pa=%f\r\n", pa);
		

		_delay_ms(400);
	
	}
}
