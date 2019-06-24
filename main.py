#main.py: Responsible for executing function calls and control flow for BOT
import socket 
import json
import time
import pprint

#Stores current location of the bot in the arena
current_location = (0,0) 

#transaction_pool: Contains the flag of cells where the bot has to go
''' -1 -> No box present in the cell
    0 -> Box is present in the cell but it has not been placed at the dropping point (waiting for pickup)
    0 -> Box is not present in the cell and it has been placed at the dropping point
'''
##After ArUco markers are detected through overhead camera 'transaction_pool' is updated with respective flags 
transaction_pool = [-1,-1,0,0,-1,-1,-1,-1,-1,-1,0,-1,-1,0,-1,0]

##Binary classification code based upon general algorithm or classification algorithms(ML)

#own_box_index_list: List that contains index numbers from 'transaction_pool' list; where the bot has to choose from first 
own_box_index_list = [2,3]

#help_box_index_list: List that contains index numbers from 'transaction_pool' list; where the bot has to choose from after it finishes its own boxes
help_box_index_list = [10,13,15]

box_number = -1

all_box_finished = True
my_own_box_are_finished = True

###Test this delay
time.sleep(5)

def check_all_box_finished():
    if len(own_block_index_list) != 0:
        my_own_box_are_finished = False
        all_box_finished = False
    if my_own_box_are_finished == True:
        if len(help_box_index_list) != 0:
            all_box_finished = False
    return all_box_finished

while True:
    if check_all_box_finished() == False:
        ##Call a function to another py file that returns smallest path index after list of indices and current location is given
        '''if my_own_box_are_finished == False:
              box_number = function(current_location,all item of own_box_index_list)
        else:
              box_number = function(current_location,all item of help_box_index_list)
        '''
        transaction_pool[box_number] = 1
        ##Function call to blockchain py file
        ##success_in_adding = function(transaction_pool,my_own_box_are_finished) ...myownboxarefinsihed is for own block and thsi function would return add_it variable
        if success_in_adding == False:
            print('Already flag changed(0 -> 1);Not added to blockchain; Bot is still at base node; Searching flag for other boxes...')
        else:
        '''if my_own_box_are_finished == False:
              pop ele from own_box_index_list
        else:
               pop ele from  help_box_index_list
        '''
            print('Added to blockchain; Picking and placing the box...')
            #path = Code to call file function with inp as current locayion and final location and returns path
            #wait_for_2h = code to call the function other file with path and send the data to vrep , recieve h and then send done or 2h
            
        my_own_box_are_finished = True
        all_box_finished = True

    else:
        print('All boxes are placed!')
        ##Code to stop the bot and buzzer for 5 seconds
        break
print('***END***')
