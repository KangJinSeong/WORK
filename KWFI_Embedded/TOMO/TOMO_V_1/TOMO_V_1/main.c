/*
 * TOMO_V_2c
 * Title: TRC_Controller_V2.0
 * Created: 2023-6-22
 * Author : Kangjinseong
 */ 

#include <stdio.h>
#include <avr/io.h>
#include "UAT_Ver_3.h"
#include <util/delay.h>

FILE OUTPUT = FDEV_SETUP_STREAM(UART_transmit, NULL, _FDEV_SETUP_WRITE);
//FILE INPUt = FDEV_SETUP_STREAM(NULL,UART_receive, _FDEV_SETUP_READ);

int read_ADC(void)
{

	while(!(ADCSRA & ( 1 << ADIF)));

	return ADC;

}

void PWM_init(void)
{
	TCCR1D |= (1<< OC1AU);
	TCCR1A |= (1 << COM1A1) | (1 << WGM11);
	TCCR1B |=  (1 << WGM13) | (1 << WGM12);
	TCCR1B |= (1 << CS11);
	ICR1 = 275;
	//OCR1A = 85 * 0.06;
	
}
void PWM_close(void)
{
	TCCR1D &= ~(1<< OC1AU);
}
void PWM_Open(void)
{
	TCCR1D |= (1<< OC1AU);
}
void ADC_init(unsigned char channel)
{
	ADMUX &= ~( 1 << AREFEN);
	ADCSRA |= (1 << ADPS2) | (1 << ADPS0)| (1 << ADPS0);
	ADCSRA |= ( 1 << ADEN);
	ADCSRA |= ( 1 << ADSC);
	ADCSRA |= ( 1 << ADATE);
	ADMUX = ((ADMUX & 0xE0) | channel);
}

void ADC_EN(void)
{
	ADCSRA |= ( 1 << ADSC);
}

void ADC_OFF(void)
{
	ADCSRA &= ~( 1 << ADSC);
}

float move_average(void)
{
	float result = 0;
	int read_data;
	for (int i = 0; i<10; i++)
	{
		read_data = read_ADC();
		_delay_ms(300);
		result += (read_data*5.11)/1023;
	}
	result = (result / 10);
	return result;
}

int main(void)
{
	DDRB = 0x03;	// PWM 출력 단자
	//DDRA = 0x04;	// DC-DC 컨버터 Enable 단자
	PORTB = 0x01;
	stdout = &OUTPUT;
	
	float V;
	int read;
	int top = 275;
	PWM_init();
	PWM_close();
	UART_init();									//디버깅 UART 제어 초기설정
	ADC_init(6);	//0B01100      AVcc/4 0B01101
	printf("init_supply START\r\n");

	char sss = 1;
	int tun = 10.061;			//10.216
    /* Replace with your application code */
    while (1) 
    {

		while(sss == 1)
		{	
			printf("충전모드\r\n");
			V = move_average();
			printf("Read Volt = %f\r\nDone\r\n", V*tun);
			if (V*tun < 6.9)
			{
				PWM_Open();
				printf("PWM out Duty: 0.11\r\n");
				OCR1A = top * 0.11;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 6.9) && ( V*tun < 13.5 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.12\r\n");
				OCR1A = top * 0.12;
				PORTB = 0x03;
				//_delay_ms(30000);				
			}
			if ((V*tun >= 13.5) && ( V*tun < 19.7 ))	//19.7 -> 19.4V 0.3V 튜닝
			{
				PWM_Open();
				printf("PWM out Duty: 0.13\r\n");
				OCR1A = top * 0.13;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 19.7) && ( V*tun < 22.3 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.14\r\n");
				OCR1A = top * 0.14;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 22.3) && ( V*tun < 25.1 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.15\r\n");
				OCR1A = top * 0.15;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 25.1) && ( V*tun < 27.8 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.16\r\n");
				OCR1A = top * 0.16;
				PORTB = 0x03;
				//_delay_ms(30000);
			}			
			if ((V*tun >= 27.8) && ( V*tun < 30.3 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.18\r\n");
				OCR1A = top * 0.18;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 30.3) && ( V*tun < 32.9 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.20\r\n");
				OCR1A = top * 0.20;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 32.9) && ( V*tun < 35.4 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.24\r\n");
				OCR1A = top * 0.24;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 35.4) && ( V*tun < 37.8 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.30\r\n");
				OCR1A = top * 0.30;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 37.8) && ( V*tun < 40.2 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.40\r\n");
				OCR1A = top * 0.40;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 40.2) && ( V*tun < 42.4 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.60\r\n");
				OCR1A = top * 0.60;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 42.4) && ( V*tun < 44.4 ))
			{
				PWM_Open();
				printf("PWM out Duty: 100\r\n");
				OCR1A = top * 1;
				PORTB = 0x03;
				//_delay_ms(30000);
			}
			if ((V*tun >= 44.4) && ( V*tun < 46 ))
			{
				PWM_Open();
				printf("PWM out Duty: 100\r\n");
				OCR1A = top * 1;
				PORTB = 0x03;
				//_delay_ms(30000);
			}			
									
			if ( V*tun >= 46 )		//0.3V 튜닝
			{
				PWM_close();
				//PORTA = 0x00;
				PORTB = 0x01;
				sss = 0;
			}
		}
		printf("방전모드\r\n");
		V = move_average();
		printf("Read Volt = %f\r\nDone\r\n", V*tun);
		if ( V*tun <= 45)
		{
			sss = 1;
		}
	}
	return 0;
}

/*
			if ((V*tun >= 40.2) && ( V*tun < 42.4 ))
			{
				PWM_Open();
				printf("PWM out Duty: 0.60\r\n");
				PORTA = 0x04;
				OCR1A = top * 0.60;
				_delay_ms(30000);
			}
			if ((V*tun >= 42.4) && ( V*tun < 47 ))// 0.3V 튜닝(47 -> 46.7)
			{
				PWM_close();
				PORTB = 0xFF;
				printf("PWM out Duty: 1\r\n");
				PORTA = 0x04;
				_delay_ms(30000);
			}
			if ( V*tun >= 47 )		//0.3V 튜닝
			{
				PORTB = 0x00;
				PORTA = 0x00;
				sss = 0;
			}
*/