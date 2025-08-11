/*
 * UAT_Ver_3.c
 *
 * Created: 2020-04-13 오후 3:28:51
 *  Author: NI
 */ 
#include "UAT_Ver_3.h"



/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                 
               디버깅: UART통신함수               

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
void UART_init(void)
{
	LINCR |= ( 1 << LENA ); //  UART mode on //8비트 데이터 패리티 없음, 1비트 정지 비트 모드 디폴트
	LINBRRH = 0x00;
	LINBRRL = 0x03;
	//LINBTR |= ( 1 << LDISR);
	LINCR |= ( 1 << LCMD1) | ( 1 << LCMD2) | ( 1 << LCMD0);  //송신 가능   송수신가능 ( 1 << LCMD1) | ( 1 << LCMD2) | ( 1 << LCMD0)
	//LINENIR |= (1<<LENTXOK) | (1<<LENRXOK);
}

void UART_transmit( char data)
{
	LINDAT = data;	//송신 가능 대기
	while( (LINSIR & ( 1 << LBUSY ) ) );
}

unsigned char UART_receive(void)
{
	
	while( !(LINSIR & ( 1 << LRXOK ) ) );
	while( (LINERR & ( 1 << LTOERR ) ) );
	return LINDAT;
}

void UART_print_string(char *str)
{
	for (int i = 0; str[i]; i++)
	{
		UART_transmit(str[i]);
	}
}

void UART_print_1_byte_number( uint8_t n)
{
	char numString[4] = "0";
	int i, index = 0;
	
	if (n > 0)
	{
		for (i = 0; n != 0; i++)
		{
			numString[i] = n % 10 + '0';
			n = n /10;
		}
		numString[i] = '\0';
		index =  i - 1;
	}
	for (i = index; i >= 0; i--)
	{
		UART_transmit(numString[i]);
	}
}

int read_ADC(void)
{

	while(!(ADCSRA & ( 1 << ADIF)));
	

	return ADC;

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



uint8_t Pitch[10]={0x00,};                        // Pitch Data Buffer Initialize
uint8_t Roll[10]={0x00,};                         // Roll Data Buffer Initialize
uint8_t Heading[10]={0x00,};                      // Heading Data Buffer Initialize
uint8_t Step=0;

void DCM250B_UartProc(uint8_t* ReceiveData)
{
	switch(Step){
		case 0x00:
		if(ReceiveData[0]==0x68)                  // Confirm Receive Data "0x68"
		Step = 0x01;
		else break;
		case 0x01:
		if(ReceiveData[1]==0x0D)                  // Confirm Receive Data "0x0D"
		Step = 0x02;
		else break;
		case 0x02:
		if(ReceiveData[2]==0x00)                   // Confirm Receive Data "0x03"
		Step = 0x03;
		else break;
		case 0x03:
		if(ReceiveData[3]==0x84)                   // Confirm Receive Data "0x84"
		Step = 0x04;
		else break;
		case 0x04:
		Pitch[0] = '>';
		Pitch[1] = 'P';
		Pitch[2] = '=';

		if(((ReceiveData[4]&0xF0)>>4)==0x01)      // ReciveData[4]의 상위 word 값이 1이면 Pitch의 부호는 '-', 0이면 '+'
		{
			Pitch[3] = '-';
		}
		else
		{
			Pitch[3] = '+';
		}
		Pitch[4] = (ReceiveData[4]&0x0F)+0x30;                    // Pitch 100단위
		Pitch[5] = ((ReceiveData[5]&0xF0)>>4)+0x30;               // pitch 10단위
		Pitch[6] = (ReceiveData[5]&0x0F)+0x30;                    // pitch 1단위
		Pitch[7] = '.';                                           // 소수점
		Step = 0x05;
		case 0x05:
		Pitch[8] = ((ReceiveData[6]&0xF0)>>4)+0x30;               // pitch 1/10단위
		Pitch[9] = ((ReceiveData[6]&0x0F)>>4)+0x30;               // pitch 1/100단위
		Step = 0x06;
		case 0x06:
		Roll[0] = '>';
		Roll[1] = 'R';
		Roll[2] = '=';
		if(((ReceiveData[7]&0xF0)>>4)==0x01)                      //  ReciveData[7]의 상위 word 값이 1이면 Roll의 부호는 '-', 0이면 '+'
		{
			Roll[3] = '-';
		}
		else
		{
			Roll[3] = '+';
		}
		Roll[4] = (ReceiveData[7]&0x0F)+0x30;                      // Roll 100단위
		Roll[5] = ((ReceiveData[8]&0xF0)>>4)+0x30;                 // Roll 10단위
		Roll[6] = (ReceiveData[8]&0x0F)+0x30;                      // Roll 1단위
		Roll[7] = '.';                                             // 소수점
		Step = 0x07;
		case 0x07:
		Roll[8] = ((ReceiveData[9]&0xF0)>>4)+0x30;                 // Roll 1/10 단위
		Roll[9] = (ReceiveData[9]&0x0F)+0x30;                      // Roll 1/100 단위
		Step = 0x08;
		case 0x08:
		Heading[0] = '>';
		Heading[1] = 'H';
		Heading[2] = '=';
		if(((ReceiveData[10]&0xF0)>>4)==0x01)                      //  ReciveData[10]의 상위 word 값이 1이면 Heading의 부호는 '-', 0이면 '+'
		{
			Heading[3] = '-';
		}
		else
		{
			Heading[3] = '+';
		}
		Heading[4] = (ReceiveData[10]&0x0F)+0x30;                  // Heading 100단위
		Heading[5] = ((ReceiveData[11]&0xF0)>>4)+0x30;             // Heading 10단위
		Heading[6] = (ReceiveData[11]&0x0F)+0x30;                  // Heading 1단위
		Heading[7] = '.';                                          // 소수점
		Step = 0x09;
		case 0x09:
		Heading[8] = ((ReceiveData[12]&0xF0)>>4)+0x30;             // Heading 1/10단위
		Heading[9] = (ReceiveData[12]&0x0F)+0x30;                  // Heading 1/100단위
		Step = 0x0A;
		case 0x0A:
		for(int i=0; i<10; i++)
		{
			printf("%c", *(Pitch+i));                                // Pitch  RS485  Transmission
		}
		printf("\r\n");


		for(int i=0; i<10; i++)
		{
			printf("%c", *(Roll+i));                                 // Roll RS485 Transmission
		}
		printf("\r\n");


		for(int i=0; i<10; i++)
		{
			printf("%c", *(Heading+i));                              // Heading RS485 Transmission
		}
		printf("\r\n");
		Step = 0x00;
		break;
		default: break;
	}
}