#!/usr/local/bin/python3.4
# -*- coding: latin-1 -*-
# Programmeringsteknik webbkurs KTH inlamningsuppgift 1
# lucas persson
# 2015-08-17
# kontaktformedling, ett program som bygger en databas och viktar och matchar ihop personer
import pickle #using built in library to save binarys
import uuid

#user interface called feed me beacuse its hungry for the users information
class feedMe:
	#sanity check on input gender
	def sanityCheckStr(self):
		food=input("Vilket kön sökes? m (man) / k (kvinna) / b (bägge): ")
		if food=="m" or food=="k" or food=="b":
			return food
		else:
			self.sanityCheckStr()

	#sanity check on input opinions inputtext str
	def sanityCheckInt(self,str):
		food=input(str+": ")
		try:#TODO funkar inte 
			food=int(food)
			if food<6 and food>0 :
				return food
			else:
				print("försök igen")
				self.sanityCheckInt(str)#try again
		except ValueError:
			print("försök igen")
			self.sanityCheckInt(str)

		

	#takes users opinion 
	def opinion(self,populate=0):
		values=person(uuid.uuid4())
		if populate:
			values.dict["Namn"]=input("namn: ")#populate only
		values.dict["Kön"]=self.sanityCheckStr()
		print("Gradera från 0 till 5 hur du värdesätter följande:")
		for atribute in values.a:
			if populate:
				values.dict[atribute] =float(input(atribute+": "))#populate only
			else:
				values.dict[atribute] =self.sanityCheckInt(atribute)
			

		return values

	#ask if edit 
	def edit(self,db):
		self.present(db)
		print("vill du:\n1: lägga till\n2: ta bort\n0: avsluta")
		n=input()
		if n is "1":
			db.append(self.opinion(1))
		
		elif n is "2":
			print("inte implementerad")				

		else:
			return 1 
		self.edit(db)


	#presents the matches to the user
	def present(self,matches):
		print("Namn\tKön",end="\t")
		for atr in matches[0].a:
			print(atr,end="\t")
		print("")
		print("----------------------------------------------------------------------------------------------------------")
		for match in matches:
			print(match.dict["Namn"]+"\t"+match.dict["Kön"],end="\t")
			for a in match.a:
				print(match.dict[a],end="\t")
				if a == "Skönhet" or a == "Intelligens" or a == "Förmögenhet" or a == "Sexighet":
					print("",end="\t")
			print("")
		print("")

		



class prog:
	

	#saves to file
	def save(self,db):
		with open('data.db', 'wb') as output:
			pickle.dump(db,output,pickle.HIGHEST_PROTOCOL)


	#loads from file
	def load(self):
		with open('data.db', 'rb') as input:
			db= pickle.load(input)
		if not db:
			print("feed me")
			db=[feedMe().opinion()]
		return db



	#normalizes the database values
	def normalize(self,db,values):
		maxi=person("maxi")
		for a in maxi.a:	#fills up empty max array
			maxi.dict[a]=0.0

		for data in db:		#finds the highest values 
			for a in maxi.a:
				if maxi.dict[a] < float(data.dict[a]):
					maxi.dict[a]=float(data.dict[a])
		#print(maxi.dict)
		for data in db:		#normalizes the values with user weigth and max value
			for a in maxi.a:
				data.dict[a]=float(data.dict[a])/maxi.dict[a]
				data.dict[a]=float(data.dict[a])*values.dict[a]
				data.tot+=data.dict[a]#wft
				#print(a+":"+str(data.dict[a]))

		return db

		

	#finds a match based on opinions from user
	def findMatch(self,ndb,gender):
		sorted(ndb, key=lambda person: person.tot)
		out=[]
		for pers in ndb:
			if gender == pers.dict["Kön"] or gender == "b":
			#	print(pers.dict["Namn"]+":"+str(pers.tot))
				out.append(pers)
			
		return out[:10]

	



	

class person:
	tot=0

	def __init__(self,guid):
		self.a=["Mognad","Skönhet","Intelligens","Humor","Förmögenhet","Sexighet","Utbildning"]
		self.dict={}
		self.guid=guid




#calls functions 
if __name__ == '__main__':
	main=prog()
	food=feedMe()
	db=main.load()
	#realdb=db.deepcopy()
	if input("vill du ändra databasen (y)") is "y":
		food.edit(db)
		if input("vill du verkligen spara (y)") is "y":
			main.save(db)
			print("sparat")
	else:
		values=food.opinion()
	#values=""
	#db.append(values)
	#main.save(db)
		ndb=main.normalize(db,values)
		matches=main.findMatch(ndb,values.dict["Kön"])
		food.present(matches)

	
		
