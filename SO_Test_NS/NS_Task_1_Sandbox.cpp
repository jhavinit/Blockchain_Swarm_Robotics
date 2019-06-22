#include "NS_Task_1_Sandbox.h"
#include "serialread.h"
#include "string.h"









void forward_wls(unsigned char node)
{       int d;
        int flag=0;
	unsigned char leftSensor, rightSensor, midSensor;
	int nodeReached = 0, i = 0;
	while (1)
	{
		leftSensor = ADC_Conversion(1);
		midSensor = ADC_Conversion(2);
		rightSensor = ADC_Conversion(3);
                
                
        d=getProxSensorDistance();
        if((d>0)&&(d<90))
          {
          stop();
          flag=1;
          }
        
	else if (leftSensor < 200 && midSensor >= 200 && rightSensor < 200 && !flag)
		{       
                        printf("f\n");
			forward();
			_delay_ms(1);
			stop();
		}
		
		else if ((leftSensor >= 200 && midSensor >= 200 && rightSensor < 200 && !flag) || (leftSensor >= 200 && midSensor < 200 && rightSensor < 200 && !flag))
		{        
                        printf("sl\n");
			soft_left();
			_delay_ms(1);
			stop();
		}
		
		else if ((leftSensor < 200 && midSensor >= 200 && rightSensor >= 200 && !flag) || (leftSensor < 200 && midSensor < 200 && rightSensor >= 200 && !flag))
		{       
                        printf("sr\n");
			soft_right();
			_delay_ms(1);
			stop();
		}
		
		else if (leftSensor >= 200 && midSensor >= 200 && rightSensor >= 200 && !flag)
		{       
                        
			nodeReached++;
			if (nodeReached == node)
			{       printf("nodedetected\n");
				stop();
				break;
			}
		}
                else if(d==0)
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
* Function Name: Square
* Input: void
* Output: void
* Logic: Use this function to make the robot trace a square path on the arena
* Example Call: Square();
*/
void Square(void)
{
}

/*
*
* Function Name: Task_1_1
* Input: void
* Output: void
* Logic: Use this function to encapsulate your Task 1.1 logic
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
			_delay_ms(1);
			break;
		case 'l':
                        printf("left\n");
			left_turn_wls();
			_delay_ms(1);
			break;
		case 'r':
                        printf("right\n");
			right_turn_wls();
			_delay_ms(1);
			break;
                case 'g':
                        printf("pick\n");
                        pick();
                        _delay_ms(50);
                        break;
                case 'p':
                        printf("place\n");
                        place();
                        _delay_ms(50);
                        break;
		case 'q':
                        printf("finish\n");
			stop();
                        write_wd();
                        _delay_ms(50);
	                
			break;
		default:
			break;
		}
                 
                
              
	}
}


