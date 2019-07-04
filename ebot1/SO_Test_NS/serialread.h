               /* c++ serial read library for reading and writing into a serial port 
               global variables:None
               functions:write_wd(),fun()*/
        
    	        #include <stdio.h>
    	        #include <fcntl.h>   /* File Control Definitions           */
    	        #include <termios.h> /* POSIX Terminal Control Definitions */
    	        #include <unistd.h>  /* UNIX Standard Definitions 	   */ 
    	        #include <errno.h>   /* ERROR Number Definitions           */
                
        
               /*function name:write_wd().
                 input:none.
                 output:none.
                 logic:writes a character h into the serial port.
                 call:write_wd()*/
                 

              int write_wd()
                {
                int wd;          
       	        wd = open("/dev/pts/26",O_RDWR |O_NOCTTY);                 /*create a virtual port and give the value here*/                            						
        	if(wd == -1)	
            	   printf("\n  Error! in Opening /dev/pts/26");                   
        	else
            	   printf("\n  ttyUSB0 Opened Successfully ");
		struct termios SerialPortSettings;	                   /*various ports setting like baud rate,partiy bits,stopbits,nonblocking call,and cannonical form with  \n only the stream ends*/ 
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
	        write(wd, "h\n", 2);
                close(wd);
                }

               /*function name:fun().
                 input:none.
                 output:stream of commands to be followed  .
                 logic:reads a data from the serial port.
                 call:fun() */

               char* fun(void)
               {
               int rd;
                
        	rd = open("/dev/pts/22",O_RDWR | O_NOCTTY);	                       /*create a virtual port and give the value here*/ 					
        	if(rd == -1)	
            	   printf("\n  Error! in Opening /dev/pts/22 ");                       /*various ports setting like baud rate,partiy bits,stopbits,nonblocking call,and cannonical form with  \n only the stream ends*/ 
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
                char *sread;                                                                    /* Buffer to store the data received              */
		int  bytes_read = 0;                                                            /* Number of bytes read by the read() system call */
 		int i = 0;

		bytes_read = read(rd,&read_buffer,100);                                         /* Read the data                   */
	        sread=read_buffer;
		for(i=0;i<bytes_read;i++)	                                                /*printing only the received characters*/
		    printf("%c",read_buffer[i]);
	
		printf("\n +----------------------------------+\n\n\n");

		close(rd);                                                                      /* Close the serial port */
       
                return sread;
                }

                
