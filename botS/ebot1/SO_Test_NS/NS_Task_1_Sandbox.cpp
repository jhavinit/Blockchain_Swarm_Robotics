#include "NS_Task_1_Sandbox.h"
#include "serialread.h"
#include "string.h"



/*
*
* Function Name:  forward_wls()
* Input: numberof nodes
* Output: void
* Logic: To make the bot go forward the number specified by the input parameters and also looks for obstacles before it moves forward  
* Example Call: forward_wls(1)
*/

void forward_wls(unsigned char node)
{       int d,dl,dr;
        int flag=0;
	unsigned char leftSensor, rightSensor, midSensor;
	int nodeReached = 0, i = 0;
	while (1)
	{
		leftSensor = ADC_Conversion(1);
		midSensor = ADC_Conversion(2);
		rightSensor = ADC_Conversion(3);
                
        
        d=getProxSensorDistance(1);                   //3 proximity sensors in the front to look for obstacles
        dl=getProxSensorDistance(2);
        dr=getProxSensorDistance(3);
        if(((d>0)&&(d<100))|((dl>0)&&(dl<100))|((dr>0)&&(dr<100)))
          {
          stop();
          
          flag=1;                                    // flag bit to look for if the obstacles has gone or not
          }
        
	else if (leftSensor < 200 && midSensor >= 200 && rightSensor < 200 && !flag)
		{       
                       
			forward();
			_delay_ms(1);
			stop();
		}
		
		else if ((leftSensor >= 200 && midSensor >= 200 && rightSensor < 200 && !flag) || (leftSensor >= 200 && midSensor < 200 && rightSensor < 200 && !flag))
		{        
                       
			soft_left();
			_delay_ms(1);
			stop();
		}
		
		else if ((leftSensor < 200 && midSensor >= 200 && rightSensor >= 200 && !flag) || (leftSensor < 200 && midSensor < 200 && rightSensor >= 200 && !flag))
		{       
                      
			soft_right();
			_delay_ms(1);
			stop();
		}
		
		else if (leftSensor >= 255 && midSensor >= 255 && rightSensor >= 255 && !flag)
		{       
                        
			nodeReached++;
			if (nodeReached == node)
			{       printf("nodedetected\n");
				stop();
				break;
			}
		}
                else if((d==0)&&(dl==0)&&(dr==0))
                 {
                 if(flag)
                  flag=0;
                 }  
             
	}
	while (leftSensor >= 200 && midSensor >= 200 && rightSensor >= 200)
	{
		forward();
		_delay_ms(1);
                
		leftSensor = ADC_Conversion(1);
		midSensor = ADC_Conversion(2);
		rightSensor = ADC_Conversion(3);
	}
	forward();
	_delay_ms(330);
	stop();
}
/*
*
* Function Name: left_turn_wls
* Input: void
* Output: void
* Logic: Uses white line sensors to turn left until black line is encountered
* Example Call: left_turn_wls(); //Turns right until black line is encountered
*
*/
void left_turn_wls(void)
{
	unsigned char leftSensor, rightSensor, midSensor;
	int nodeReached = 0;
	leftSensor = ADC_Conversion(1);
	midSensor = ADC_Conversion(2);
	rightSensor = ADC_Conversion(3);
	while (midSensor >= 200 || leftSensor >= 200)
	{
		left();
		_delay_ms(1);

		leftSensor = ADC_Conversion(1);
		midSensor = ADC_Conversion(2);
		rightSensor = ADC_Conversion(3);
	}
	while (midSensor < 200)
	{
		left();
		_delay_ms(1);

		leftSensor = ADC_Conversion(1);
		midSensor = ADC_Conversion(2);
		rightSensor = ADC_Conversion(3);
	}
	stop();
}

/*
*
* Function Name: right_turn_wls
* Input: void
* Output: void
* Logic: Uses white line sensors to turn right until black line is encountered
* Example Call: right_turn_wls(); //Turns right until black line is encountered
*/
void right_turn_wls(void)
{
	unsigned char leftSensor, rightSensor, midSensor;
	int nodeReached = 0;
	leftSensor = ADC_Conversion(1);
	midSensor = ADC_Conversion(2);
	rightSensor = ADC_Conversion(3);
	while (midSensor >= 200 || rightSensor >= 200)
	{
		right();
		_delay_ms(1);

		leftSensor = ADC_Conversion(1);
		midSensor = ADC_Conversion(2);
		rightSensor = ADC_Conversion(3);
	}
	while (midSensor < 200)
	{
		right();
		_delay_ms(1);

		leftSensor = ADC_Conversion(1);
		midSensor = ADC_Conversion(2);
		rightSensor = ADC_Conversion(3);
	}
	stop();
}

/*
*
* Function Name: Task_1_1
* Input: void
* Output: void
* Logic: To follow the simple commands given by the serial port to be followed and sends a acknowledgement bit 'h' after completion
* Example Call: Task_1_1();
*/
void Task_1_1()
{       
        
        char p[50];
	
        strcpy(p,fun());
        printf("%s",p);
	
	for (int i=0;  p[i]!= 'y'; ++i)
	
	{       
		switch (p[i])
		{
		case 'f':
                        printf("forward\n");
			forward_wls(1);
			_delay_ms(1000);
			break;
		case 'l':
                        printf("left\n");
			left_turn_wls();
			_delay_ms(1000);
			break;
		case 'r':
                        printf("right\n");
			right_turn_wls();
			_delay_ms(1000);
			break;
                case 'g':
                        printf("pick\n");
                        pick();
                        _delay_ms(1000);
                        break;
                case 'p':
                        printf("place\n");
                        place();
                        _delay_ms(1000);
                        break;
		case 'q':
                        printf("finish\n");
			stop();
                        write_wd();                                                         //over task so send 'h'
                        _delay_ms(1000);
	                
			break;
		default:
			break;
		}
                 
                
              
	}
}


