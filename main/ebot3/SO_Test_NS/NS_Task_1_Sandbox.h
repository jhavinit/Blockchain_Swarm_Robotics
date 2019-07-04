#include "NS_Task_1_Predef.h"
extern unsigned int color_sensor_pulse_count;

void forward_wls(unsigned char node);

void left_turn_wls(int ms);

void right_turn_wls(int ms);

void Square(void);

void Task_1_1();

void Task_1_2(void);

void line_follow(void);

void follow_back(void);

void Map_of_the_scene(void);

void get_Shortest_path(int starting_node , int ending_node);

void initiate_direction(void);

void actuate_left(int ms);

void actuate_right(int ms);

void actuate_forward(unsigned char forward_mode);

void actuate(int a ,int b);

void update_path(void);

void set_Deposit(void);

void set_Pickup(void);


