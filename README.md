# Blockchain_Swarm_Robotics
```diff 
Contributions are most welcome!
```
## Objective:
To create an Immutable and Decentralised System to store
and analyse plant vitals of a eFSI farm using Iota's Tangle.
To develop a Blockchain based Decentralised Framework for a
two bot foraging system using V-rep and python.

## System:
In an arena where blocks are kept in random cells,relatively
simpler bots come together to make collective decisions and
forage all the blocks to a common place.

## Workflow of Code: 
![Capture](https://user-images.githubusercontent.com/42121605/60666672-39425c00-9e85-11e9-85a5-f996d4d9cc3f.PNG)

#### This project is implemented for 2 bots, one can scale it for more bots. 

## How to implement above code locally: 

### Understanding the file structure:
1. vrep_scenes: Contain all files that are required to run Vrep locally and are required to be started before any next step.
2. test_version_1: Contains python code to implement 2 bots ... server1/2 and client1/2 are used via sockets.
3. display_blockchain: Contains 2 files: HTML and python that is used to visualize the blockchain in a web browser.
4. communication: Contains files for communicating between Vrep and python script (zigserial) that gets the path for bot.
5. client_server_files: Contains the client and server files for each of the two bots(It has addtional for 3rd bot also but it is not used                         in this project).
6. botS: Contains files required for running bots in vrep enviornment.
7. Blockchain code working(without vrep and segregation): Contains the code for client and server for bot 1 and bot 2 without vrep. One      can test it seperately in this folder itself. Example:
   Step 1: Run server-1.py and server-2.py
   Step 2: Run client-1.py and client-2.py
   You can observer how blockchain is modified at each step after box pick and place.
8. main: It contains all the files and folders collectively in one folder from which one can run the project directly. 

### How to run code on a local system?
Step 1: Fork the repo: [https://github.com/jhavinit/Blockchain_Swarm_Robotics](https://github.com/jhavinit/Blockchain_Swarm_Robotics)<br/>
Step 2: Go inside /main ...all the files required are inside main folder<br/>
Step 3: Install Vrep v_3.6.1 (Tested in ubuntu 16.04 LTS)<br/>
Step 4: Make sure to have python > 3.5.4 and a text editor for editing C, C++ (gedit) and  python files(IDLE py:3.5.4)<br/>
Step 5: Make the virtual serial ports for 2 bots (4 terminals in total) (Refer Medium article for setting virtual port: [https://medium.com/@karthiks1701/virtual-serial-ports-hack-for-communication-between-local-scripts-883fda0f60f])
Step 6: Open the scene in Vrep: Go to vrep and open scene (filename: dual_bot.ttt or fin_rep.ttt(recommended))<br/> 
Step 7: Run server-1.py and server-2.py<br/>
Step 8: Run the cpp exe files that are in the debug folder of ebot1 and ebot2<br/>
Step 9: Run the main-1.py and main-2.py<br/>
Step 10: One can observe the results in the Vrep

## Result video:
![qr_vrep_simulation (1)](https://user-images.githubusercontent.com/42121605/60670505-7b23d000-9e8e-11e9-9b36-d7841daec432.png)

## Images during project development:
 
![Screenshot from 2019-07-03 15-58-50](https://user-images.githubusercontent.com/42121605/60670768-19b03100-9e8f-11e9-86ae-46fe9fdc47d9.png)
![Capture](https://user-images.githubusercontent.com/42121605/60670769-1a48c780-9e8f-11e9-8c2c-6faae819e98c.PNG)
![Screenshot from 2019-06-13 14-53-21](https://user-images.githubusercontent.com/42121605/60670772-1a48c780-9e8f-11e9-97a5-77f6a0337706.png)
![Screenshot from 2019-06-30 12-57-46](https://user-images.githubusercontent.com/42121605/60670773-1ae15e00-9e8f-11e9-9c5f-104f5a4fdc28.png)
![Screenshot from 2019-06-30 16-29-21](https://user-images.githubusercontent.com/42121605/60670774-1ae15e00-9e8f-11e9-8a03-d4a390caecdb.png)

## References:
1. [https://dl.acm.org/citation.cfm?id=3237464](https://dl.acm.org/citation.cfm?id=3237464)
2. [https://arxiv.org/pdf/1608.00695.pdf](https://arxiv.org/pdf/1608.00695.pdf)
