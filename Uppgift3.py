#!/usr/local/bin/python3.4
# Programmeringsteknik webbkurs KTH inlämningsuppgift 1
# lucas persson
# 2014-06-15
# funparksimulator
import random

class rides:
	def __init__(self,name,length,woolvl,wow,com):#seats
		self.name=name
		self.length=length
		#self.seats=seats#not implemented
		self.woolvl=woolvl
		self.running=0
		self.broken=0
		self.wow=wow
		self.com=com

	def start(self):
	 	self.running=1		
		
	def stop(self):
		self.running=0

		#check if broken or shutdown
	def isRunning(self):
		if self.running:
			if not self.broken:
				return 1
		return 0

		#12 % chance of ride breaking
	def breaks(self):
		if random.random()<0.12:
			#print("breaking")
			self.running=0
			self.broken=1
			
		# checks your length and rides the ride, checks if it broke
	def rideMe(self,yourLength):
		if yourLength>self.length:
			i=0 
			while i<self.woolvl:
				#print("debug i=",i)
				if not self.isRunning():
					print("buu, it broke")
					return 
				i+=1
				print(self.wow)
				self.breaks()
		else:
			print("you are to short")
		return



#init funpark
rollercoster=rides('Rollercoster',150,5,"WOOOWOHIII","Come and ride the insane Rollercoster!")
scaryHouse=rides('Scary House',130,3,"AAHAAHHHHHH","do you dare to enter the haunted Scary House?")
radioCars=rides('Radio Cars',110,4,"HAHAHHA","Radio Cars, bump in to your friends and see who is the best driver.")
funparksimulator=[rollercoster,scaryHouse,radioCars]
#user dialog
running=1
print("Hello and welcome to Lubens Funpark")
yourLength=int(input("How long are you(min 110): "))
while running:#select ride
	for x in funparksimulator:
		print(x.com)
	print("What do you want to ride:")
	i=0
	while i<3:
		funparksimulator[i].start()
		print(i+1,funparksimulator[i].name)
		i+=1
	inp=int(input("4 Leave\n"))-1

	if(inp<3):#exit 
		funparksimulator[inp].rideMe(yourLength)
	else:
		running=0

#shut down park
for ride in funparksimulator:
		ride.stop()


