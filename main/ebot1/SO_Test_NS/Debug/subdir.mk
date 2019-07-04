################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../NS_Task_1.cpp \
../NS_Task_1_Predef.cpp \
../NS_Task_1_Sandbox.cpp 

C_SRCS += \
../extApi.c \
../extApiPlatform.c 

OBJS += \
./NS_Task_1.o \
./NS_Task_1_Predef.o \
./NS_Task_1_Sandbox.o \
./extApi.o \
./extApiPlatform.o 

CPP_DEPS += \
./NS_Task_1.d \
./NS_Task_1_Predef.d \
./NS_Task_1_Sandbox.d 

C_DEPS += \
./extApi.d \
./extApiPlatform.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -std=c++1y -I/usr/local/include/opencv -O0 -g3 -Wall -c -fmessage-length=0 -pthread -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

%.o: ../%.c
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -std=c11 -O0 -g3 -Wall -c -fmessage-length=0 -pthread -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


