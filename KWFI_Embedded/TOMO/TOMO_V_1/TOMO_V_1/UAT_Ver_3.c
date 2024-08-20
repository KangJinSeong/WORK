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
	LINBRRL = 0x33;
	LINCR |= ( 1 << LCMD1) | ( 1 << LCMD2) | ( 1 << LCMD0);  //송신 가능   송수신가능 ( 1 << LCMD1) | ( 1 << LCMD2) | ( 1 << LCMD0)
	//LINCR &= ~(1 << LCMD1);
}
void UART_transmit( char data)
{

	LINDAT = data;	//송신 가능 대기
	while( (LINSIR & ( 1 << LBUSY ) ) );

}
unsigned char UART_receive(void)
{
	while( ! (LINSIR & ( 1 << LRXOK) ) );
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
