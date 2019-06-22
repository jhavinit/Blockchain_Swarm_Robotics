#include "NS_Task_1_Predef.h"



simxInt ID = 0, ID_vid;
char thread_stop_flag = 0;
simxUChar detection_state=0;
simxUChar *lineSensorOutput = new simxUChar[3](), *colorSensorOutput = new simxUChar[3]();
simxFloat detected_point[3] = { 0,0,0 }; 
unsigned int color_sensor_pulse_count = 0;
simxInt dir_left = 0, dir_right = 0, vis_error, prox_error, place_handle = -3;
simxInt *res = new simxInt[2](),*resVis = new simxInt[2](), *obs1 = new simxInt[1](), *obs2 = new simxInt[1](), *obs3 = new simxInt[1](), *leftJoint = new simxInt[1](), *rightJoint = new simxInt[1](), *lineSensor = new simxInt[1](), *colorSensor = new simxInt[1](), *eBot = new simxInt[1](), *cuboid0 = new simxInt[1](), *cuboid = new simxInt[1](), *cuboid3 = new simxInt[1](), *cuboid4 = new simxInt[1](), *proxSensor = new simxInt[1](), *visionSensor = new simxInt[1]();
simxFloat linear_velocity_left = 0, linear_velocity_right = 0;
int vis_i,vis_j,vis_k;
const simxFloat posObv[3] = { 50,50,50 }, posPlaceRel[3] = { 0.125, 0, 0 };
int imageAcTime=0,  prevImageAcTime = 0;

void getObjectHandles(void)
{
	simxGetObjectHandle(ID, "LeftJoint", leftJoint, simx_opmode_oneshot_wait);
	simxGetObjectHandle(ID, "RightJoint", rightJoint, simx_opmode_oneshot_wait);
	simxGetObjectHandle(ID, "LineSensor", lineSensor, simx_opmode_oneshot_wait);
	simxGetObjectHandle(ID, "ColorSensor", colorSensor, simx_opmode_oneshot_wait);
	simxGetObjectHandle(ID, "eBot", eBot, simx_opmode_oneshot_wait);
	simxGetObjectHandle(ID, "Obs1", obs1, simx_opmode_oneshot_wait);
	simxGetObjectHandle(ID, "Obs2", obs2, simx_opmode_oneshot_wait);
	simxGetObjectHandle(ID, "Obs3", obs3, simx_opmode_oneshot_wait);
	simxGetObjectHandle(ID, "ProximitySensor", proxSensor, simx_opmode_oneshot_wait);
        simxGetObjectHandle(ID, "cuboid", cuboid, simx_opmode_oneshot_wait);
        simxGetObjectHandle(ID, "cuboid0", cuboid0, simx_opmode_oneshot_wait);
        simxGetObjectHandle(ID, "cuboid1", cuboid3, simx_opmode_oneshot_wait);
}

void setJointVelocities(int opmode)
{
		simxSetJointTargetVelocity(ID, *rightJoint, linear_velocity_right, opmode);
		simxSetJointTargetVelocity(ID, *leftJoint, linear_velocity_left, opmode);
}

void forward(void)
{
	dir_left = dir_right = 1;
	linear_velocity_left = linear_velocity_right = LIN_MAX;
}

void back(void)
{
	dir_left = dir_right = -1;
	linear_velocity_left = linear_velocity_right = LIN_MAX;
}

void soft_right(void)
{
	dir_left = 1;
	dir_right = 0;
	linear_velocity_left = LIN_MAX;
	linear_velocity_right = 0;
}

void right(void)
{
	dir_left = 1;
	dir_right = -1;
	linear_velocity_left = LIN_MAX;
	linear_velocity_right = -LIN_MAX;
}

void soft_left(void)
{
	dir_left = 0;
	dir_right = 1;
	linear_velocity_left = 0;
	linear_velocity_right = LIN_MAX;
}

void left(void)
{
	dir_left = -1;
	dir_right = 1;
	linear_velocity_left = -LIN_MAX;
	linear_velocity_right = LIN_MAX;
}

void stop(void)
{
	dir_left = 0;
	dir_right = 0;
	linear_velocity_left = 0;
	linear_velocity_right = 0;
}

void velocity(int left_motor_velocity, int right_motor_velocity)
{
	if (left_motor_velocity > 255)
		left_motor_velocity = 255;
	else if (left_motor_velocity < 0)
		left_motor_velocity = 0;
	if (right_motor_velocity > 255)
		right_motor_velocity = 255;
	else if (right_motor_velocity < 0)
		right_motor_velocity = 0;

	linear_velocity_left = dir_left * LIN_MAX*left_motor_velocity / float(255.0);
	linear_velocity_right = dir_right * LIN_MAX*right_motor_velocity / float(255.0);
	

}


void getLineSensorData(void)
{
	simxGetVisionSensorImage(ID, *lineSensor, res, &lineSensorOutput, 1, simx_opmode_buffer);

}

void getColorSensorData(void)
{
	simxGetVisionSensorImage(ID, *colorSensor, res, &colorSensorOutput, 0, simx_opmode_buffer);
}

unsigned int getProxSensorDistance(void)
{
	unsigned int retval = 0;
	prox_error = simxReadProximitySensor(ID, *proxSensor, &detection_state, detected_point, NULL, NULL, simx_opmode_buffer);
	if (detection_state != 0)
	{
		detection_state = 0;
		retval = (unsigned int)(detected_point[2] * 1000);
	}

	return retval;
}


void filter_red(void)
{
	getColorSensorData();
	color_sensor_pulse_count = (unsigned int)(colorSensorOutput[0] * 5000 / 255.0)+(rand()%1001);
}

void filter_green(void)
{
	getColorSensorData();
	color_sensor_pulse_count = (unsigned int)(colorSensorOutput[1] * 5000 / 255.0)+(rand() % 1001);
}

void filter_blue(void)
{
	getColorSensorData();
	color_sensor_pulse_count = (unsigned int)(colorSensorOutput[2] * 5000 / 255.0)+ (rand() % 1001);
}

void filter_clear(void)
{
	getColorSensorData();
	color_sensor_pulse_count = (unsigned int)((colorSensorOutput[0]+ colorSensorOutput[1]+ colorSensorOutput[2]) * 5000 / 255.0)+(rand() % 1001);
}


int initial(int portNb)
{
	int clientID = -1;
	simxFinish(-1);
	clientID = simxStart("127.0.0.1", portNb, true, true, 5000, 5);
	printf("%d\n",clientID);
	return clientID;
}

void simulatorStart(int ID)
{
	char start;
	do
		start = simxStartSimulation(ID, simx_opmode_oneshot_wait);
	while (start != simx_return_ok);
}

void initVisionSensors(void)
{
	do 
		vis_error = simxGetVisionSensorImage(ID, *lineSensor, res, &lineSensorOutput, 1, simx_opmode_streaming);
	while (vis_error != simx_return_ok || vis_error == simx_error_novalue_flag);
	do
		vis_error = simxGetVisionSensorImage(ID, *colorSensor, res, &colorSensorOutput, 0, simx_opmode_streaming);
	while (vis_error != simx_return_ok || vis_error == simx_error_novalue_flag);
	for(int i = 0; i < VIS_SEN_INIT_VAL; i++)
	{
		getLineSensorData();
		getColorSensorData();
	}
}


void initProxSensor(void)
{
	do
		prox_error = simxReadProximitySensor(ID, *proxSensor, NULL, NULL, NULL, NULL, simx_opmode_streaming);
	while (prox_error != simx_return_ok || prox_error == simx_error_novalue_flag);
}

void initSensors(void)
{
	initVisionSensors();
	initProxSensor();
}

void pick(void)
{

        printf("trying to pick");
	simxInt pickDetectObjectHandle = -2;
	do
		prox_error = simxReadProximitySensor(ID, *proxSensor, NULL, NULL, &pickDetectObjectHandle, NULL, simx_opmode_buffer);
	while (prox_error != simx_return_ok || prox_error == simx_error_novalue_flag);
	if (pickDetectObjectHandle != -2)
	{
		if (pickDetectObjectHandle == *obs1 || pickDetectObjectHandle == *obs2 || pickDetectObjectHandle == *obs3)
		{
			printf("\nCan't pick an obstacle!");
		}
		else
		{
			if (place_handle == -3)
				simxSetObjectPosition(ID, pickDetectObjectHandle, -1, posObv, simx_opmode_oneshot);
			else
				printf("\nCan't pick, another block already picked up.");
		}

	}
	else
		printf("\nNo object to pick.");
        
	place_handle = pickDetectObjectHandle;
}

void place(void)
{
	//setobjpos relative to Robot
	if (place_handle != -3)
	{	
		simxSetObjectPosition(ID, place_handle, *eBot, posPlaceRel, simx_opmode_oneshot);
		place_handle = -3;
	}
	else
		printf("Nothing has been picked");

}


unsigned char ADC_Conversion(unsigned char ch_no)
{
	if (ch_no == 1)	//Left Line Sensor
		return ~lineSensorOutput[0];
	else if (ch_no == 2)//Middle Line Sensor
		return ~lineSensorOutput[1];
	else if (ch_no == 3)//Right Line Sensor
		return ~lineSensorOutput[2];
	else if (ch_no == FRONT_IR_ADC_CHANNEL) //Channel for Proximity sensor
		return getProxSensorDistance();
	return 255;
}


void _delay_ms(unsigned int ms)
{
	std::this_thread::sleep_for(std::chrono::milliseconds(ms));
}



void video_init()
{
	ID_vid = initial(19998);
	//cout << "Reached init" << endl;
}

void init(void)
{
	printf("here\n");
	ID = initial(19997);
	printf("there\n");
	//ID_vid = initial(19998);
        printf("1\n");
	getObjectHandles();
        printf("2\n");
	simulatorStart(ID);
        printf("3\n");
	initSensors();
        
	//simxGetObjectHandle(ID_vid, "VisionSensor", visionSensor, simx_opmode_oneshot_wait);
	//printf("\n		%d\n\n", *visionSensor);
	printf("4\n");
}


void threadStop(void)
{
	thread_stop_flag = -1;
}

void cleanUp(void)
{
	printf("That's it folks!");

	char check;
	do
		check = simxStopSimulation(ID, simx_opmode_oneshot_wait);

	while (check != simx_return_ok);
	//simxFinish(ID);
	//printf("\n\n%d\n\n%d\n\n", ID, ID_vid);
	//simxFinish(ID_vid);
	simxFinish(-1);
//	cout<<ID<<endl;
}

void threadCalls(void)
{
	//cout << "Start thread vrep " << endl;
	while (thread_stop_flag != -1)
	{
		setJointVelocities(simx_opmode_oneshot);
		getLineSensorData();
	}
	linear_velocity_right = linear_velocity_left = 0;
	setJointVelocities(simx_opmode_oneshot_wait);


	//cout << "Released" << endl;
}
