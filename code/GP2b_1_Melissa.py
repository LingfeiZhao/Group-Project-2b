
# coding: utf-8

# In[ ]:

#My attempt at number 1


# In[ ]:

import matplotlib
import numpy as np
import random
import matplotlib.pyplot as plt


# In[125]:

fish_init = 5000 #inital number of fish
shark_init = 2000 #inital number of shark
fish_procr_time = 5 #procreation time of fish
shark_procr_time = -7 #procreation time of shark
starve_shark = 10 #time it takes for shark to starve
timesteps = 100 #number of timesteps to iterate through
i = 102 #dimension of square grid
water = [[0 for l in range(i)] for m in range(i)] #water grid, contains both sharks and fish
move = [[0 for l in range(i)] for m in range(i)] #move grid, contains record of whether spot on water grid has been operated on
sharkstarve = [[0 for l in range(i)] for m in range(i)] #shark starve grid, contains time since last meal of shark
timestep_list = list(range(timesteps)) #list of timesteps
numfish_list = [0]*timesteps #list of number of fish per timestep
numshark_list = [0]*timesteps #list of number of shark per timestep


# In[126]:

#setting a border of numbers so we don't need to check border indices later; we'll only operate on the
#boxes within the borders
for index in range(i):
    water[0][index] = 1.25
    water[i-1][index] = 1.25
    water[index][0] = 1.25
    water[index][i-1] = 1.25


# In[127]:

#function to generate random grid points for places of shark and fish
def samplegrid(j, n):
    coordinates = np.array([(x,y) for x in range(1,j-1) for y in range(1,j-1)])
    indices = np.random.choice(len(coordinates),n,replace = False)
    return coordinates[indices]


# In[128]:

#list of random grid points
randanimals = samplegrid(i-1,fish_init+shark_init)


# In[129]:

#fish will be denoted by positive numbers, with age corresponding to number
#shark will be denoted by negative numbers, with age corresponding to absolute value of number
#empty spots will be denoted by zeros

#placing fish in grid points
for index in range(fish_init):
    x = randanimals[index][0]
    y = randanimals[index][1]
    water[x][y] = 1

#placing shark in grid points
for index in range(fish_init,fish_init+shark_init):
    x = randanimals[index][0]
    y = randanimals[index][1]
    water[x][y] = -1


# In[ ]:

#iterate over each timestep and go through each grid point 
for index in range(timesteps):
    for n in range(1,i-1):
        for m in range(1,i-1):
            #if the grid point hasn't been operated on, and it contains a fish
            if move[n][m] == 0 and water[n][m] > 0:
                neighbours = [(n+1,m),(n-1,m),(n,m+1),(n,m-1)]
                random.shuffle(neighbours) #randomly order neighbours
                #go through list of random neighbours, move fish to the first empty one
                if water[neighbours[0][0]][neighbours[0][1]] == 0:
                    #if the fish has reached procreation time, move fish and make a new fish where old spot was 
                    if water[n][m] == fish_procr_time:
                        water[neighbours[0][0]][neighbours[0][1]] = 1
                        water[n][m] = 1
                    #otherwise, move fish and increase age    
                    else:
                        water[neighbours[0][0]][neighbours[0][1]] = water[n][m] + 1
                        water[n][m] = 0
                    move[neighbours[0][0]][neighbours[0][1]] = 1
                elif water[neighbours[1][0]][neighbours[1][1]] == 0:
                    if water[n][m] == fish_procr_time:
                        water[neighbours[1][0]][neighbours[1][1]] = 1
                        water[n][m] = 1
                    else:
                        water[neighbours[1][0]][neighbours[1][1]] + 1
                        water[n][m] = 0
                    move[neighbours[1][0]][neighbours[1][1]] = 1
                elif water[neighbours[2][0]][neighbours[2][1]] == 0:
                    if water[n][m] == fish_procr_time:
                        water[neighbours[2][0]][neighbours[2][1]] = 1
                        water[n][m] = 1
                    else:
                        water[neighbours[2][0]][neighbours[2][1]] = water[n][m] + 1
                        water[n][m] = 0
                    move[neighbours[2][0]][neighbours[2][1]] = 1
                elif water[neighbours[3][0]][neighbours[3][1]] == 0:
                    if water[n][m] == fish_procr_time:
                        water[neighbours[3][0]][neighbours[3][1]] = 1
                        water[n][m] = 1
                    else:
                        water[neighbours[3][0]][neighbours[3][1]] = water[n][m] + 1
                        water[n][m] = 0
                    move[neighbours[3][0]][neighbours[3][1]] = 1
            #if grid point has not been operated on and contains a shark
            elif move[n][m] == 0 and water[n][m] < 0:
                neighbours = [(n+1,m),(n-1,m),(n,m+1),(n,m-1)]
                random.shuffle(neighbours)
                #go through list of random neighbours, eat first fish
                if water[neighbours[0][0]][neighbours[0][1]] > 0 and water[neighbours[0][0]][neighbours[0][1]]%1 == 0:
                    #if shark reaches procreation age, eat fish and make new shark at old spot
                    if water[n][m] == shark_procr_time:
                        water[neighbours[0][0]][neighbours[0][1]] = -1
                        water[n][m] = -1
                    else:
                        water[neighbours[0][0]][neighbours[0][1]] = water[n][m] - 1
                        water[n][m] = 0
                    #set time of last meal to zero    
                    sharkstarve[neighbours[0][0]][neighbours[0][1]] = 0
                    sharkstarve[n][m] = 0
                    move[neighbours[0][0]][neighbours[0][1]] = 1
                elif water[neighbours[1][0]][neighbours[1][1]] > 0 and water[neighbours[1][0]][neighbours[1][1]]%1 == 0:
                    if water[n][m] == shark_procr_time:
                        water[neighbours[1][0]][neighbours[1][1]] = -1
                        water[n][m] = -1
                    else:
                        water[neighbours[1][0]][neighbours[1][1]] = water[n][m] - 1
                        water[n][m] = 0
                    sharkstarve[neighbours[1][0]][neighbours[1][1]] = 0
                    sharkstarve[n][m] = 0
                    move[neighbours[1][0]][neighbours[1][1]] = 1
                elif water[neighbours[2][0]][neighbours[2][1]] > 0 and water[neighbours[2][0]][neighbours[2][1]]%1 == 0:
                    if water[n][m] == shark_procr_time:
                        water[neighbours[2][0]][neighbours[2][1]] = -1
                        water[n][m] = -1
                    else:
                        water[neighbours[2][0]][neighbours[2][1]] = water[n][m] - 1
                        water[n][m] = 0
                    sharkstarve[neighbours[2][0]][neighbours[2][1]] = 0
                    sharkstarve[n][m] = 0
                    move[neighbours[2][0]][neighbours[2][1]] = 1
                elif water[neighbours[3][0]][neighbours[3][1]] > 0 and water[neighbours[3][0]][neighbours[3][1]]%1 == 0:
                    if water[n][m] == shark_procr_time:
                        water[neighbours[3][0]][neighbours[3][1]] = -1
                        water[n][m] = -1
                    else:
                        water[neighbours[3][0]][neighbours[3][1]] = water[n][m] - 1
                        water[n][m] = 0
                    sharkstarve[neighbours[3][0]][neighbours[3][1]] = 0
                    sharkstarve[n][m] = 0
                    move[neighbours[3][0]][neighbours[3][1]] = 1
                #if no fish are around, move shark to a random location
                elif water[neighbours[0][0]][neighbours[0][1]] == 0:
                    #if procreation time, make a new shark at old spot
                    if water[n][m] == shark_procr_time:
                        water[neighbours[0][0]][neighbours[0][1]] = -1
                        water[n][m] = -1
                    else:
                        water[neighbours[0][0]][neighbours[0][1]] = water[n][m] - 1
                        water[n][m] = 0
                    sharkstarve[neighbours[0][0]][neighbours[0][1]] = sharkstarve[n][m] + 1
                    sharkstarve[n][m] = 0
                    move[neighbours[0][0]][neighbours[0][1]] = 1
                    if sharkstarve[neighbours[0][0]][neighbours[0][1]] == starve_shark:
                        water[n][m] = 0
                        sharkstarve[neighbours[0][0]][neighbours[0][1]] = 0
                elif water[neighbours[1][0]][neighbours[1][1]] == 0:
                    if water[n][m] == shark_procr_time:
                        water[neighbours[1][0]][neighbours[1][1]] = -1
                        water[n][m] = -1
                    else:
                        water[neighbours[1][0]][neighbours[1][1]] = water[n][m] - 1
                        water[n][m] = 0
                    sharkstarve[neighbours[1][0]][neighbours[1][1]] = sharkstarve[n][m] + 1
                    sharkstarve[n][m] = 0
                    move[neighbours[1][0]][neighbours[1][1]] = 1
                    if sharkstarve[neighbours[1][0]][neighbours[1][1]] == starve_shark:
                        water[n][m] = 0
                        sharkstarve[neighbours[1][0]][neighbours[1][1]] = 0
                elif water[neighbours[2][0]][neighbours[2][1]] == 0:
                    if water[n][m] == shark_procr_time:
                        water[neighbours[2][0]][neighbours[2][1]] = -1
                        water[n][m] = -1
                    else:
                        water[neighbours[2][0]][neighbours[2][1]] = water[n][m] - 1
                        water[n][m] = 0
                    sharkstarve[neighbours[2][0]][neighbours[2][1]] = sharkstarve[n][m] + 1
                    sharkstarve[n][m] = 0
                    move[neighbours[2][0]][neighbours[2][1]] = 1
                    if sharkstarve[neighbours[2][0]][neighbours[2][1]] == starve_shark:
                        water[n][m] = 0
                        sharkstarve[neighbours[2][0]][neighbours[2][1]] = 0
                elif water[neighbours[3][0]][neighbours[3][1]] == 0:
                    if water[n][m] == shark_procr_time:
                        water[neighbours[3][0]][neighbours[3][1]] = -1
                        water[n][m] = -1
                    else:
                        water[neighbours[3][0]][neighbours[3][1]] = water[n][m] - 1
                        water[n][m] = 0
                    sharkstarve[neighbours[3][0]][neighbours[3][1]] = sharkstarve[n][m] + 1
                    sharkstarve[n][m] = 0
                    move[neighbours[3][0]][neighbours[3][1]] = 1
                    if sharkstarve[neighbours[3][0]][neighbours[3][1]] == starve_shark:
                        water[n][m] = 0
                        sharkstarve[neighbours[3][0]][neighbours[3][1]] = 0
    #now count total number of fish and shark in the grid
    numfish = 0
    numshark = 0
    for n in range(1,i-1):
        for m in range(1,i-1):
            if water[n][m] > 0:
                numfish = numfish + 1
            elif water[n][m] < 0:
                numshark = numshark + 1
    #update record of number of fish and sharks for each timestep
    numfish_list[index] = numfish
    numshark_list[index] = numshark
    move = [[0 for l in range(i)] for m in range(i)]


# In[ ]:

#plot figure
plt.plot(timesteps,numfish_list,label = "Number of fish")
plt.plot(timesteps,numshark_list, label = "Number of sharks")
plt.legend(loc = "best")
plt.xlabel("Timestep")
plt.ylabel("Number of animals")
plt.title("Number of fish and sharks versus time")

