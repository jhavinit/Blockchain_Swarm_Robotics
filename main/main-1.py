#* Responsible for executing function calls and control flow for BOT-1
#* Filename: main-1.py
#* Project: Blockchain_Swarm_Robotics
#* Functions: init_blockchain(), check_all_box_finished()
#* Global Variables: current_location, drop_location, transaction_pool, own_box_index_list, help_box_index_list, box_number
#*					 all_box_finished, my_own_box_are_finished

#Imported for creating delays for simulation purpose and in some places for handshakes between files
import time
#Imported for printing large dictionaries with proper indentation
import pprint
#Imported client1 for calling these functions: init_blockchain(), add_transaction_to_blockchain()
from client1 import*
#Imported zigserial for calling these functions: vrep(current_location, box_number, option_flag)
from zigserial import*

#current_location: Stores current location of the bot in the arena
current_location = 6
#drop_location: Stores the drop location for bot-1
drop_location = 7

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

#box_number: Box number is the index number of the box to be picked or placed 
box_number = -1
#all_box_finished: It stores the boolean value of wheather all boxes are placed at their locations or not
all_box_finished = False
#my_own_box_are_finished: It stores boolean value about the boxes that were assigned to bot-1
my_own_box_are_finished = False

#Called in client1.py that creates a connection with server-1.py and connect it with other nodes 
init_blockchain()

'''
* Function Name: check_all_box_finished()
* Input: None
* Output: all_box_finished, all_box_finished: means that all the boxes are finished in the arena or not 
* Logic: First it checks for length of 'own_box_index_list' if it is 0 that means that my_own_box_are_finished = True. Then a similar check is created for all_box_finished.  
* Example Call: check_all_box_finished()
'''
def check_all_box_finished():
    global all_box_finished
    global my_own_box_are_finished
    if len(own_box_index_list) != 0:
        my_own_box_are_finished = False  
        all_box_finished = False
    if my_own_box_are_finished == True:
        if len(help_box_index_list) != 0:
            all_box_finished = False
    return all_box_finished

#*	Runs infinitely and checks wheather own or total boxes are placed or not, after that from the selected list it selects the shortest distance node to it by calling vrep() function
#*	in zigserial python code, it uses A-star algorithm for finding the shortest path to that node and returns the distance from current location. After that transaction_pool is changed at the index from 0 to 1.
#*	After that add_transaction_to_blockchain() is called for adding the transaction_pool in the blockchain, based on success or failure action is taken. If faliure then message is prompted else
#*	vrep(current_location, box_number, 1) is called for moving the bot to that location in arena for picking (option_flag=1 -> picking, option_flag = 2 ->placing), after that vrep(current_location, box_number, 2)
#*	is called for placing the box. After that it checks that my_own_box_are_finished = True or False and on basis of that pops the added box from the respective list.    
#*	After that it sets my_own_box_are_finished = True and all_box_finished = True so that these values can be unset or remain same in While loop.
while True:
    global all_box_finished
    global my_own_box_are_finished
  
    if check_all_box_finished() == False:
        ##Call a function to another py file that returns smallest path index after list of indices and current location is given
        if my_own_box_are_finished == False:
            #print("vdd");
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
