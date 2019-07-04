/*
File to call the Task_1_1()
Which makes a blocking call to the serial port so that it waits for the path.
  */
#include "NS_Task_1_Sandbox.h"

#include <csignal>


void signalHandler(int param)
{
		threadStop();
		_delay_ms(50);
		cleanUp();
		printf("Signal Received");
}





int main(int argc, char* argv[])
{       
      
	signal(SIGTERM, signalHandler);  //looks for keyboard interrupts
	init();                          //makes connection with vrep server over the port mentioned in predef.cpp
	std::thread t_1(threadCalls);	 //creates various threads
        stop();
       

        while(1)
        {	
          Task_1_1();                        
        }	

	threadStop();
	t_1.join();
       

	cleanUp();
}
