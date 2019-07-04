#main.py: Responsible for executing function calls and control flow for BOT
import time
import pprint
from client1 import*
from zigserial import*

#Stores current location of the bot in the arena
current_location =6 
drop_location = 7
#bot_axis = '+y'

#transaction_pool: Contains the flag of cells where the bot has to go
''' -1 -> No box present in the cell
    0 -> Box is present in the cell but it has not been placed at the dropping point (waiting for pickup)
    1 -> Box is not present in the cell and it has been placed at the dropping point
'''
##After ArUco markers are detected through overhead camera 'transaction_pool' is updated with respective flags 
transaction_pool = [-1,-1,0,0,-1,-1,-1,-1,0,-1,-1,-1,-1,0,-1,0]

##Binary classification code based upon general algorithm or classification algorithms(ML)

#own_box_index_list: List that contains index numbers from 'transaction_pool' list; where the bot has to choose from first 
own_box_index_list = [2,3]
#help_box_index_list: List that contains index numbers from 'transaction_pool' list; where the bot has to choose from after it finishes its own boxes
help_box_index_list = [8,13,15]

box_number = -1

all_box_finished = False
my_own_box_are_finished = False

###Test this delay
#time.sleep(5)

init_blockchain()

def check_all_box_finished():
    global all_box_finished
    global my_own_box_are_finished
    if len(own_box_index_list) != 0:
        my_own_box_are_finished = False  
        all_box_finished = False
        print("svs")
	print(my_own_box_are_finished)
    if my_own_box_are_finished == True:
        if len(help_box_index_list) != 0:
            all_box_finished = False
    return all_box_finished

while True:
    global all_box_finished
    global my_own_box_are_finished
  
    if check_all_box_finished() == False:
        ##Call a function to another py file that returns smallest path index after list of indices and current location is given
        if my_own_box_are_finished == False:
            print("vdd");
            min_dist = 32767
            for item in own_box_index_list:
                dist = len(vrep(current_location, item, 0))
                if dist < min_dist:
                    min_dist = dist
                    box_number = item
        else:
            min_dist = 32767
            for item in help_box_index_list:
                dist = len(vrep(current_location, item, 0))
                if dist < min_dist:
                    min_dist = dist
                    box_number = item
                    
        transaction_pool[box_number] = 1
        
        #Function call to blockchain py file
        success_in_adding = add_transaction_to_blockchain(transaction_pool, box_number, my_own_box_are_finished)

        if success_in_adding == False:
            print('Already flag changed(0 -> 1);Not added to blockchain; Bot is still at base node; Searching flag for other boxes...')
        else:
            print('Added to blockchain; Picking and placing the box...')
            if vrep(current_location, box_number, 1) == 'h':
                print('Box picked')
                print(box_number)
                current_location = box_number
                time.sleep(3)
                if vrep(current_location, drop_location, 2) == 'h':
                    print('Box placed')
                    current_location = drop_location
	
	if my_own_box_are_finished == False:
            own_box_index_list.pop(own_box_index_list.index(box_number))
        else:
            help_box_index_list.pop(help_box_index_list.index(box_number))
        
	print('Searching other boxes...')
        my_own_box_are_finished = True
        all_box_finished = True

    else:
        print('All boxes are placed!')
        ##Code to stop the bot and buzzer for 5 seconds
        break
print('***END***')
