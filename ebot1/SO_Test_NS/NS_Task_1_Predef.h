#include <stdio.h>
#include <iostream>
#include <chrono>
#include <thread>

//using namespace std;

extern "C"{
	#include "extApi.h"
}

#define LIN_MAX 5
#define FRONT_IR_ADC_CHANNEL 4
#define VIS_SEN_INIT_VAL 1000


int initial(void);
void threadCalls(void);
void forward(void);
void back(void);
void left(void);
void right(void);
void soft_left(void);
void soft_right(void);
void stop(void);
void velocity(int, int);
unsigned char ADC_Conversion(unsigned char);
void initSensors(void);
void _delay_ms(unsigned int);
void filter_red(void);
void filter_blue(void);
void filter_green(void);
void filter_clear(void);
void pick(void);
void place(void);
void init(void);
void cleanUp(void);
void threadStop(void);
unsigned int getProxSensorDistance(int);
