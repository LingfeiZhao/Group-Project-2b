import random
import pylab

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

			if self.fishes[pos]==self.breed_age_fish: # if the fish is at breed age, it breeds
				self.grid[pos_new[0]][pos_new[1]]=1
				self.fishes[pos]=0
				self.fishes[pos_new]=0
			else: # else it just swim and add age
				self.grid[pos[0]][pos[1]]=0
				self.grid[pos_new[0]][pos_new[1]]=1
				self.fishes[pos_new]=self.fishes.pop(pos)+1



	def shark_update(self, pos):
		fish, spare=self.neighbor(pos)
		if fish: # if there is fish neighbor, the shark hunts
			pos_new=random.choice(fish)
			# eat the fish, reset hungry_time, add age
			self.grid[pos_new[0]][pos_new[1]]=-1
			self.fishes.pop(pos_new) 
			self.sharks[pos]=(self.sharks[pos][0]+1,0)

			if self.sharks[pos][0]==self.breed_age_shark: # if the shark is at breed age, it breeds
				self.sharks[pos]=(0,0)
				self.sharks[pos_new]=(0,0)
			else: # else it just swim
				self.grid[pos[0]][pos[1]]=0
				self.sharks[pos_new]=self.sharks.pop(pos)

		elif spare: # if there is spare neighbor
			pos_new=random.choice(spare)
			# add hungry_time, add age
			self.sharks[pos]=(self.sharks[pos][0]+1,self.sharks[pos][1]+1)


			if self.sharks[pos][1]==self.starve_time_shark: # starve 
				self.grid[pos[0]][pos[1]]=0
				self.sharks.pop(pos)
			elif self.sharks[pos][0]==self.breed_age_shark: # if the shark is at breed age, it breeds
				self.grid[pos_new[0]][pos_new[1]]=-1 
				self.sharks[pos]=(0,0)
				self.sharks[pos_new]=(0,0)
			else: # else it just swim
				self.grid[pos_new[0]][pos_new[1]]=-1 
				self.grid[pos[0]][pos[1]]=0
				self.sharks[pos_new]=self.sharks.pop(pos)


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
#img=pylab.imshow(PP.grid,cmap='RdBu',clim=(-1,1),animated=True)
for i in range(1000):
	PP.update()

pylab.show()
pylab.plot(PP.t,PP.n_shark,'ro',label='shark')
pylab.plot(PP.t,PP.n_fish,'co',label='fish')
pylab.legend(loc=0,numpoints=1)
pylab.xlabel('time')
pylab.ylabel('number')
pylab.show()


