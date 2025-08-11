/*
 * UAT_Ver_3.h
 *
 * Created: 2020-04-13 오후 3:41:11
 *  Author: NI
 */ 


#ifndef UAT_VER_3_H_
#define UAT_VER_3_H_


/*#define F_CPU 14745600UL*/
#define F_CPU 14745600UL
#define TERMINATOR '\r'


/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                 
                음향태그 V3.0 헤더파일                

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

#include <stdio.h>
#include <avr/io.h>
#include <util/delay.h>
#include <string.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <avr/wdt.h>
#include <avr/sfr_defs.h>
#include <math.h>

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                 
                TX모드: SPI통신을 위한 핀 정의                

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

#define SPI_SS				PORTA6
#define SPI_MOSI			PORTA4		//마스터 -> 슬레이브(데이터)
#define SPI_SCK				PORTA5
#define SPI_Select()			PORTA &= ~( 1 << SPI_SS)		// Low
#define SPI_DeSelect()			PORTA |= ( 1 << SPI_SS)			// High


/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                 
                음향태그 V3.0 global 변수                

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

extern char state;
extern char Sleep_Time;
extern char RXSA;
extern unsigned int datah;
extern unsigned int delay_data;
extern unsigned int dataL;
extern unsigned int mindataL;
extern volatile unsigned int Delay_Flag[5];
extern unsigned char Buffer_INDEX;
extern volatile unsigned int Buffer[60];
extern volatile unsigned int RX_Buffer[26];
extern volatile unsigned int RX_ID[26];
extern unsigned char RX_Buffer_INDEX;
extern unsigned char RX_ID_INDEX;
extern unsigned char Signalcheck_Flag;
extern unsigned char IDCHECK_Flag;
extern unsigned char Start_index;
extern unsigned char END_index;
extern volatile unsigned int UAT_ID[26];
extern unsigned char TXON;
extern unsigned char TX_INDEX;
extern unsigned char TX_count;


/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                 
                전원관리모드 함수               

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/

extern void PORT_INIT(void);
extern void TXMD(void);
extern void RXMD(void);
extern void WDMD(void);

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                 
               디버깅: UART통신함수               

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
extern void UART_init(void);
extern void UART_transmit( char data);
extern unsigned char UART_receive(void);
extern void UART_print_string(char *str);
extern void UART_print_1_byte_number( uint8_t n);
void DCM250B_UartProc(uint8_t* ReceiveData);
int read_ADC(void);
void ADC_init(unsigned char channel);
void ADC_EN(void);
void ADC_OFF(void);
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                 
             Sleep Mode: 워치독 관리 함수               

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
extern void WDT_ON(void);
extern void WDT_OFF(void);

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                 
    RX모드: 타이머, 수신신호처리, 버퍼 초기화 함수               

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
extern void timer0_init(void);
extern void timer0_off(void);
extern void timer0_on(void);
extern void RX_MODE(void);
extern void Buffer_zeros(void);

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                 
      TX모드: SPI관리, 신호생성, 신호초기화 함수               

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
extern void SPI_INIT(void);
extern void SPI_change_2_Byte( unsigned int byte);
extern void TX_frequency_control(long frequency, char cont_freq);
extern void UP_chirp_32ms(char index);
extern void DOWN_chirp_32ms(char index);
extern void TX_set(char TX_ON, char period);
extern void SPI_off(void);
extern void TX_FREQ0_write( long frequency, unsigned char first_phase);


#endif /* UAT_VER_3_H_ */