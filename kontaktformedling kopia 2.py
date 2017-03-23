#!/usr/local/bin/python3.4
# -*- coding: UTF-8 -*-
# Programmeringsteknik webbkurs KTH inlamningsuppgift 1
# lucas persson
# 2015-08-17
# kontaktformedling, ett Program som bygger en databas och viktar och matchar ihop Personer
import pickle #using built in library to save binarys
import uuid

#user interface called
class UserInterface:
	#sanity check on input gender
	def sanityCheckStr(self):
		inputs=input("Vilket kön sökes? m (man) / k (kvinna) / b (bägge): ")
		if inputs=="m" or inputs=="k" or inputs=="b":
			return inputs
		else:
			self.sanityCheckStr()

	#sanity check on input opinions inputtext str
	def sanityCheckInt(self,str):
		inputs=input(str+": ")
		try:
			n=int(inputs)
			if n<6 and n>0 :
				return n
			else:
				print("försök igen")
				self.sanityCheckInt(str)#try again
		except ValueError:
			print("försök igen")
			self.sanityCheckInt(str)

	def sanityCheckFix(self,str):
		out=None
		while out is None:
			out=self.sanityCheckInt(str)
		return out
		

	#takes users opinion 
	def opinion(self,populate=0):
		values=Person()
		if populate:
			values.dict["Namn"]=input("namn: ")#populate only
		values.dict["Kön"]=self.sanityCheckStr()
		print("Gradera från 0 till 5 hur du värdesätter följande:")
		for atribute in values.a:
			if populate:
				values.dict[atribute] =float(input(atribute+": "))#populate only
			else:
				values.dict[atribute] =self.sanityCheckFix(atribute)
				#print(values.dict[atribute])


		return values

	#ask if edit 
	def edit(self,db):
		self.present(db)
		print("vill du:\n1: lägga till\n2: ta bort\n0: avsluta")
		n=input()
		if n is "1":
			db.append(self.opinion(1))
		
		elif n is "2":
			
			inputs=input("vilket index?")
			try:
				index=int(inputs)-1
				if input("vill du verkligen ta bort: "+db[index].dict["Namn"]+"(y)") is "y":
					del db[index]

			except:
				print("ERROR\n fel värden, du får inte radera nått då")
		else:
			return 1 
		self.edit(db)


	#presents the matches to the user
	def present(self,matches,normlized=0):
		db=Prog().load()
		print("index\tNamn\tKön",end="\t")
		for atr in matches[0].a:
			print(atr,end="\t")
		print("")
		print("----------------------------------------------------------------------------------------------------------")
		i=0
		for match in matches:
			if normlized == 1:
				match=next((x for x in db if x.guid == match.guid), None)
			else:
				i+= 1
				print(str(i)+".",end="\t")			
			print(match.dict["Namn"]+"\t"+match.dict["Kön"],end="\t")
			for a in match.a:
				print(match.dict[a],end="\t")
				if  a == "Intelligens" or a == "Förmögenhet" or a == "Sexighet":
					print("",end="\t")

			print("")
		print("")

		


#core functions like I/O and calculation
class Prog:
	

	#saves to file
	def save(self,db):
		with open('data.db', 'wb') as output:
			pickle.dump(db,output,pickle.HIGHEST_PROTOCOL)


	#loads from file
	def load(self):
		try:
			with open('data.db', 'rb') as input:
				db= pickle.load(input)
		except EnvironmentError:
			print("error creating new DB")
			print("feed me:")
			db=[UserInterface().opinion(1)]
		return db



	#normalizes the database values
	def normalize(self,db,values):
		maxi=Person()
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
	def findMatch(self,normlizedDB,gender):
		sorted(normlizedDB, key=lambda Person: Person.tot)
		out=[]
		for pers in normlizedDB:
			if gender == pers.dict["Kön"] or gender == "b":
			#	print(pers.dict["Namn"]+":"+str(pers.tot))
				out.append(pers)
			
		return out[:10]

	



	
#Person represents a person with tot for a total wegithed point, constant atributes for iteration, dict contains the values of a person with keys based on atributes
class Person:
	tot=0
	atributes=["Mognad","Skönhet","Intelligens","Humor","Förmögenhet","Sexighet","Utbildning"]#TODO add namn in atributes and change UserInterface().opinion and UserInterface().present acordningly

	def __init__(self):
		self.dict={}
		self.guid=uuid.uuid4()




#calls functions 
if __name__ == '__main__':
	main=Prog()
	inputs=UserInterface()
	db=main.load()
	#realdb=db.deepcopy()
	if input("vill du ändra databasen (y)") is "y":
		inputs.edit(db)
		if input("vill du verkligen spara (y)") is "y":
			main.save(db)
			print("sparat")
	else:
		values=inputs.opinion()
	#values=""
	#db.append(values)
	#main.save(db)
		normlizedDB=main.normalize(db,values)
		matches=main.findMatch(normlizedDB,values.dict["Kön"])
		inputs.present(matches,1)

	
		
