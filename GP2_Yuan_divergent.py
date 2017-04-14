'''
group assignment 2b
'''
from random import randint, choice
import numpy as np
import matplotlib.pyplot as plt
from copy import copy
class predatorprey(object):
    
    def __init__(self,x=20,y=20, fish_total=3, shark_total=2):
        self.time=0
        self.procreate_time_fish=10
        #self.starve_time_fish=5
        self.procreate_time_shark=20
        self.starve_time_shark=10
        self.grid=[[0]*y for i in range(x)]
        self.fish=[[-1]*y for i in range(x)]   #-1:nonexist, otherwise age
        self.shark=[[-1]*y for i in range(x)]
        self.sharkstarve=[[-1]*y for i in range(x)]
        self.occupied=[]
        s=0
        while s<shark_total:
            xs=randint(0,x-1)
            ys=randint(0,y-1)
            if self.grid[xs][ys]==0:
                self.grid[xs][ys]=1
                self.sharkstarve[xs][ys]=0
                s+=1
                
        f=0
        while f<fish_total:
            xf=randint(0,x-1)
            yf=randint(0,y-1)
            if self.grid[xf][yf]==0:
                self.grid[xf][yf]=-1
                f+=1

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j]==-1:
                    self.fish[i][j]=0
                    self.occupied.append((i,j))
                if self.grid[i][j]==1:
                    self.shark[i][j]=0
                    self.occupied.append((i,j))
    
    def envolve(self,time=1):
        T=range(time)
        for t in T:
            
            
            if not self.exist(self.fish):
                print "fish extincted!"
                
            
            if not self.exist(self.shark):
                print "shark extincted!"
            
            occupied=copy(self.occupied)
            
            res=copy(occupied)
            
            grid_old=copy(self.grid)
            #print occupied
            
            fisheatenpositions=[]
            for position,(rx, ry) in enumerate(occupied):
            
                #self.test()
                
                if self.grid[rx][ry]==-1:
                    
                    succ=self.successors((rx,ry))
                    
                    #if no successors
                    if len(succ)==0:
                        #stay same position: survival time+1
                        #print "fish stay at", (rx, ry)
                        self.fish[rx][ry]+=1
                        continue
                    
                    #if successors exist, pick a random one and swap. life+1
                    (nx, ny)=choice(succ)
                    #print "fish: swim from",(rx, ry), "to", (nx, ny)
                    self.grid[nx][ny]=-1
                    self.grid[rx][ry]=0
                    
                    self.fish[nx][ny]=self.fish[rx][ry]
                    self.fish[rx][ry]=-1
                    self.fish[nx][ny]+=1
                    res.remove((rx,ry))
                    res.append((nx,ny)) #replace old occupied coordinate with new one 

                    if self.fish[nx][ny]>0 and self.fish[nx][ny]%self.procreate_time_fish==0:
                        #procreate
                        places=self.successors((nx,ny))
                        if len(places)!=0:
                            (nnx, nny)=choice(places)
                            #print "fish procreate",(nnx, nny),"at", (nx, ny)
                            self.grid[nnx][nny]=-1
                            self.fish[nnx][nny]=0
                            
                            res.append((nnx,nny))
            
                if self.grid[rx][ry]==1:
                    if (rx, ry) in fisheatenpositions:
                        #print "already operated", (rx, ry)
                        continue
                    if self.sharkstarve[rx][ry]==self.starve_time_shark:
                        #print "shark die at", (rx, ry)
                        self.shark[rx][ry]=-1
                        self.grid[rx][ry]=0
                        self.sharkstarve[rx][ry]=-1
                        res.remove((rx,ry))
                        continue
                    fish_to_eat=self.successors((rx,ry),shark=True)
                    if len(fish_to_eat)!=0:
                        (nx,ny)=choice(fish_to_eat)
                        #print "shark at",(rx, ry),"eat fish at",(nx, ny)
                        self.grid[nx][ny]=1
                        self.grid[rx][ry]=0
                        self.shark[nx][ny]=self.shark[rx][ry]+1
                        self.shark[rx][ry]=-1
                        self.fish[nx][ny]=-1
                        self.sharkstarve[rx][ry]=-1
                        self.sharkstarve[nx][ny]=0
                        res.remove((rx,ry))
                        fisheatenpositions.append((nx, ny))
                        continue
                    
                    succ=self.successors((rx,ry))
                    if len(succ)==0:
                        #print "shark stay at", (rx, ry)
                        self.shark[rx][ry]+=1
                        self.sharkstarve[rx][ry]+=1
                        continue

                    (nx, ny)=choice(succ)
                    #print "shark: swim from",(rx, ry), "to", (nx, ny)
                    self.grid[nx][ny]=1
                    self.grid[rx][ry]=0
                    self.shark[nx][ny]=self.shark[rx][ry]+1
                    self.shark[rx][ry]=-1
                    self.sharkstarve[nx][ny]=self.sharkstarve[rx][ry]+1
                    self.sharkstarve[rx][ry]=-1
                    res.remove((rx,ry))
                    res.append((nx,ny))
                    
                    if self.shark[nx][ny]>0 and self.shark[nx][ny]%self.procreate_time_shark==0:
                        #procreate
                        places=self.successors((nx,ny))
                        if len(places)!=0:
                            (nnx, nny)=choice(places)
                            #print "shark procreate",(nnx, nny),"at", (nx, ny)
                            self.grid[nnx][nny]=1
                            self.shark[nnx][nny]=0
                            self.sharkstarve[nnx][nny]=0
                            res.append((nnx,nny))
            self.occupied=res
            self.time+=1
            '''
            print "time",self.time,":"
            print "fish #: ",self.stats()[0],"shark #:", self.stats()[1]
            print 
            '''
        
            
    
    def stats(self):
        sharktotal=0
        fishtotal=0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j]==1:
                    sharktotal+=1
                if self.grid[i][j]==-1:
                    fishtotal+=1
        return (fishtotal,sharktotal)
    
        
    def successors(self,point,shark=False):
        dxlist=[-1,1,0,0]
        dylist=[0,0,-1,1]
        succ=[]
        xp=point[0]
        yp=point[1]
        for (dx,dy) in zip(dxlist,dylist):
            nx=(xp+dx)%len(self.grid)
            ny=(yp+dy)%len(self.grid[0])
            if shark:
                if self.grid[nx][ny]==-1:
                    succ.append((nx,ny))
            else:
                if self.grid[nx][ny]==0:
                    succ.append((nx,ny))
        return succ
    
    def niceprint(self,s):
        for i in s:
            print i
            
    
    def exist(self,s):
        for i in range(len(s)):
            for j in range(len(s[0])):
                if s[i][j]!=-1:
                    return True
        return False
        
    def test(self):
        print "fish map:"
        self.niceprint(self.fish)
        print "shark map: "
        self.niceprint(self.shark)
        print "sharkstarve map: "
        self.niceprint(self.sharkstarve)
        plt.matshow(self.grid,cmap='RdBu')
        plt.show()

p=predatorprey(40,40,250,80)
T=range(1000)
fish=[]
shark=[]
for t in T:
    p.envolve(1)
    fish.append(p.stats()[0])
    shark.append(p.stats()[1])

plt.plot(T,fish,'-',T,shark,'-')
plt.title("# of fish and shark vs. time")
plt.xlabel('t')
plt.ylabel('Population')
plt.legend(['fish','shark'],loc='upper right')
plt.savefig("GP2a_divergent.pdf")

