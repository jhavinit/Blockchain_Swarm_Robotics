# Blockchain_Swarm_Robotics
### Contributions are most welcome!
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

## How to run above implemented code on a local system ?

### The folder structure is as follows:
1. vrep_scenes: Contain all files that are required to run Vrep locally and are required to be started before any next step.
2. test_version_1: Contains python code to implement 2 bots ... server1/2 and client1/2 are used via sockets.
3. display_blockchain: Contains 2 files: HTML and python that is used to visualize the blockchain in a web browser.
4. communication: Contains files for communicating between Vrep and python script (zigserial) that gets the path for bot.
5. client_server_files: Contains the client and server files for each of the two bots(It has addtional for 3rd bot also but it is not used                         in this project).
6. botS: Contains files required for running bots in vrep enviornment.
7. Blockchain code working(without vrep and segregation): Contains the code for client and server for bot 1 and bot 2 without vrep. One      can test it seperately in this folder itself. Example:
   Step 1. Run server-1.py and server-2.py
   Step 2. Run client-1.py and client-2.py
   You can observer how blockchain is modified at each step after box pick and place.
 
