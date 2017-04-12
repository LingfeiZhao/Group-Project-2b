import random
import os
import pylab
import matplotlib.image as image
from matplotlib import animation
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy
from PIL import Image
 


class Predator_Prey(object):

    def __init__(self, n0_shark, n0_fish, breed_age_shark, breed_age_fish, starve_time_shark, gridlen=100):
        self.t=[0] #list of time 
        self.n_shark=[n0_shark] #list of number of shark
        self.n_fish=[n0_fish] #list of number of fish
        self.breed_age_shark=breed_age_shark #the breed age of shark
        self.breed_age_fish=breed_age_fish #the breed age of fish
        self.starve_time_shark=starve_time_shark #the starve time of shark
        self.gridlen=gridlen #the x or y lenth of the grid

        self.fishes={} #directory of fish (pos:age)
        self.sharks={} #directory of shark (pos:(age,hungry_time))
        self.grid=[[0]*gridlen for i in range(gridlen)] #the grid, 0 is spare, 1 is fish, -1 is shark

        #initialze the grid
        i=0
        while i < self.n_fish[0]:
            #generate a random position
            randint=random.randint(0,self.gridlen*self.gridlen-1)
            pos=(randint/self.gridlen,randint%self.gridlen)
            #if this position is spare, we put a fish with age 0
            if self.grid[pos[0]][pos[1]]==0:
                self.grid[pos[0]][pos[1]]=1
                self.fishes[pos]=0
                i+=1
        i=0
        while i < self.n_shark[0]:
            #generate a random position
            randint=random.randint(0,self.gridlen*self.gridlen-1)
            pos=(randint/self.gridlen,randint%self.gridlen)
            #if this position is spare, we put a shark with age 0 and hungry_time 0
            if self.grid[pos[0]][pos[1]]==0:
                self.grid[pos[0]][pos[1]]=-1
                self.sharks[pos]=(0,0)
                i+=1

    def neighbor(self, pos):
        fish=[]
        spare=[]
        for position in [((pos[0]+1)%self.gridlen,pos[1]),((pos[0]-1)%self.gridlen,pos[1]),(pos[0],(pos[1]+1)%self.gridlen),(pos[0],(pos[1]-1)%self.gridlen)]:
            if self.grid[position[0]][position[1]]==0:
                spare.append(position)
            if self.grid[position[0]][position[1]]==1:
                fish.append(position)
         
        return fish, spare


    def fish_update(self, pos):
        fish, spare=self.neighbor(pos)
        if spare: # if there is spare neighbor, we update this fish
            pos_new=random.choice(spare)

            if self.fishes[pos]>=self.breed_age_fish: # if the fish is at breed age, it breeds
                self.grid[pos_new[0]][pos_new[1]]=1
                self.fishes[pos]=0
                self.fishes[pos_new]=0
            else: # else it just swim and add age
                self.grid[pos[0]][pos[1]]=0
                self.grid[pos_new[0]][pos_new[1]]=1
                self.fishes[pos_new]=self.fishes.pop(pos)+1
            return
        #this fish has no place to go
        #print pos
        self.fishes[pos]+=1



    def shark_update(self, pos):
        fish, spare=self.neighbor(pos)
        if fish: # if there is fish neighbor, the shark hunts
#            print "eat fish"
            pos_new=random.choice(fish)
            # eat the fish, reset hungry_time, add age
            self.grid[pos_new[0]][pos_new[1]]=-1
            self.fishes.pop(pos_new) 
            self.sharks[pos]=(self.sharks[pos][0]+1,0)

            if self.sharks[pos][0]>=self.breed_age_shark: # if the shark is at breed age, it breeds
                self.sharks[pos]=(0,0)
                self.sharks[pos_new]=(0,0)
            else: # else it just swim
                self.grid[pos[0]][pos[1]]=0
                self.sharks[pos_new]=self.sharks.pop(pos)
            return

        elif spare: # if there is spare neighbor
#            print "shark swim"
            pos_new=random.choice(spare)
            # add hungry_time, add age
            self.sharks[pos]=(self.sharks[pos][0]+1,self.sharks[pos][1]+1)


            if self.sharks[pos][1]==self.starve_time_shark: # starve 
                self.grid[pos[0]][pos[1]]=0
                self.sharks.pop(pos)
            elif self.sharks[pos][0]>=self.breed_age_shark: # if the shark is at breed age, it breeds
                self.grid[pos_new[0]][pos_new[1]]=-1 
                self.sharks[pos]=(0,0)
                self.sharks[pos_new]=(0,0)
            else: # else it just swim
                self.grid[pos_new[0]][pos_new[1]]=-1 
                self.grid[pos[0]][pos[1]]=0
                self.sharks[pos_new]=self.sharks.pop(pos)
            return
        #print "stay"
        #it has no place to go now.
        self.sharks[pos]=(self.sharks[pos][0]+1,self.sharks[pos][1]+1)
        if self.sharks[pos][1]==self.starve_time_shark: # starve 
            self.grid[pos[0]][pos[1]]=0
            self.sharks.pop(pos)


    def update(self):
        dict_tem = dict(self.fishes)
        for pos in dict_tem:
            self.fish_update(pos)

        dict_tem = dict(self.sharks)
        for pos in dict_tem:
            self.shark_update(pos)

        self.t.append(self.t[-1]+1)
        self.n_shark.append(sum(i.count(-1) for i in self.grid))
        self.n_fish.append(sum(i.count(1) for i in self.grid))


PP=Predator_Prey(n0_shark=20, n0_fish=300, breed_age_shark=20, breed_age_fish=10, starve_time_shark=10,gridlen=40)

time=1000
#save images first
if not os.path.exists("img"):
        os.mkdir("img")
ani = pylab.figure()
images=[]
for i in range(time):
    print i
    fig=pylab.figure()
    PP.update()
    if len(PP.fishes)==0 or len(PP.sharks)==0:
        print "extincted"
        break
    #plot grid
    pylab.subplot(121)
    pylab.imshow(PP.grid,cmap='coolwarm',clim=(-1,1))
    ax=pylab.subplot(122)
    # plot population vs time
    pylab.plot(PP.t,PP.n_shark,'ko',label='shark')
    pylab.plot(PP.t,PP.n_fish,'co',label='fish')
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    pylab.legend(loc=0,numpoints=1)
    pylab.axis('tight')
    pylab.xlabel('time')
    pylab.ylabel('number')
    
    # save and read
    pylab.savefig("img/"+str(i)+".png", dpi=100)
    pylab.close(fig)
    img = Image.open("img/"+str(i)+".png")
    imgplot = pylab.imshow(img)
    pylab.title("snapshot at t="+str(i))
    imgplot.axes.get_xaxis().set_visible(False)
    imgplot.axes.get_yaxis().set_visible(False)
    images.append([imgplot])
    del imgplot

#plot animation
#read images
pylab.title("Red fish and blue shark")
myani=animation.ArtistAnimation(ani, images, interval=20, blit=True, repeat_delay=1000)
writer = animation.writers['ffmpeg'](fps=30)
myani.save("animationwithplot.mp4", writer=writer, dpi=200)
pylab.close(ani)

# plot population vs time
pylab.plot(PP.t,PP.n_shark,'ko',label='shark')
pylab.plot(PP.t,PP.n_fish,'co',label='fish')
pylab.legend(loc=0,numpoints=1)
pylab.xlabel('time')
pylab.ylabel('number')
pylab.savefig('population.pdf')
pylab.show()



