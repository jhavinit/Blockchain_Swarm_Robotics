
      
        #include <stdio.h>
    	#include <fcntl.h>   /* File Control Definitions           */
    	#include <termios.h> /* POSIX Terminal Control Definitions */
    	#include <unistd.h>  /* UNIX Standard Definitions 	   */ 
    	#include <errno.h>   /* ERROR Number Definitions           */

      char* fun(void)
               {
               int rd;
                
        	rd = open("/dev/pts/20",O_RDWR | O_NOCTTY);						
        	if(rd == -1)	
            	   printf("\n  Error! in Opening /dev/pts/20 ");
        	else
            	   printf("\n  ttyUSB0 Opened Successfully ");
		struct termios SerialPortSettings;	
		tcgetattr(rd, &SerialPortSettings);	
		cfsetispeed(&SerialPortSettings,B9600); 
		cfsetospeed(&SerialPortSettings,B9600); 
		SerialPortSettings.c_cflag &= ~PARENB; 
		SerialPortSettings.c_cflag &= ~CSTOPB;   
		SerialPortSettings.c_cflag &= ~CSIZE;	
		SerialPortSettings.c_cflag |=  CS8;   
		SerialPortSettings.c_cflag &= ~CRTSCTS;       
		SerialPortSettings.c_cflag |= CREAD | CLOCAL; 
		SerialPortSettings.c_iflag &= ~(IXON | IXOFF | IXANY);          
		SerialPortSettings.c_iflag &= ~(ICANON | ECHO | ECHOE | ISIG); 
		SerialPortSettings.c_oflag &= ~OPOST;
		SerialPortSettings.c_cc[VMIN] = 1; 
		SerialPortSettings.c_cc[VTIME] = 0; 
		if((tcsetattr(rd,TCSANOW,&SerialPortSettings)) != 0) 
		    printf("\n  ERROR ! in Setting attributes");
		else
                    printf("\n  BaudRate = 9600 \n  StopBits = 1 \n  Parity   = none");
                
                                   
                tcflush(rd, TCIFLUSH);
                char read_buffer[100];
                char *sread;   /* Buffer to store the data received              */
		int  bytes_read = 0;    /* Number of bytes read by the read() system call */
 		int i = 0;

		bytes_read = read(rd,&read_buffer,100); /* Read the data                   */
	        sread=read_buffer;
		for(i=0;i<bytes_read;i++)	 /*printing only the received characters*/
		    printf("%c",read_buffer[i]);
	
		printf("\n +----------------------------------+\n\n\n");

		close(rd); /* Close the serial port */
       
                return sread;


                }  










       int main(void)
            {
             
                int wd;          
       	        wd = open("/dev/pts/21",O_RDWR |O_NOCTTY);						
        	if(wd == -1)	
            	   printf("\n  Error! in Opening /dev/pts/20 ");
        	else
            	   printf("\n  ttyUSB0 Opened Successfully ");
		struct termios SerialPortSettings;	
		tcgetattr(wd, &SerialPortSettings);	
		cfsetispeed(&SerialPortSettings,B9600); 
		cfsetospeed(&SerialPortSettings,B9600); 
		SerialPortSettings.c_cflag &= ~PARENB; 
		SerialPortSettings.c_cflag &= ~CSTOPB;   
		SerialPortSettings.c_cflag &= ~CSIZE;	
		SerialPortSettings.c_cflag |=  CS8;   
		SerialPortSettings.c_cflag &= ~CRTSCTS;       
		SerialPortSettings.c_cflag |= CREAD | CLOCAL; 
		SerialPortSettings.c_iflag &= ~(IXON | IXOFF | IXANY);          
		SerialPortSettings.c_iflag &= ~(ICANON | ECHO | ECHOE | ISIG); 
		SerialPortSettings.c_oflag &= ~OPOST;
		SerialPortSettings.c_cc[VMIN] = 1; 
		SerialPortSettings.c_cc[VTIME] = 0; 
		if((tcsetattr(wd,TCSANOW,&SerialPortSettings)) != 0) 
		    printf("\n  ERROR ! in Setting attributes");
		else
                    printf("\n  BaudRate = 9600 \n  StopBits = 1 \n  Parity   = none");
	       write(wd, "hello!\n", 7);

              

               
             }


       
	
	

