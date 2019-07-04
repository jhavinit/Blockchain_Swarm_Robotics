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
      
	signal(SIGTERM, signalHandler);
	init();
	std::thread t_1(threadCalls);	
        stop();
       

        while(1)
        {	
          Task_1_1();
        }	

	threadStop();
	t_1.join();
       

	cleanUp();
}
