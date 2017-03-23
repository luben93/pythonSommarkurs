#!/usr/local/bin/python3.4
# Programmeringsteknik webbkurs KTH inlämningsuppgift 1
# lucas persson
# 2014-06-15
# gör en rondelet av 4 meningar

#return fromated rondelet string 
def skriv(sent):
	out="\n"
	out+=fourOut(sent[0].upper())+"\n"
	out+="\n"
	out+=fourOut(sent[0])+"\n"
	i=4
	while i<len(sent[0].split()):
		out+=sent[0].split()[i]+" "
		i+=1
	out+="\n"
	out+=fourOut(sent[0])+"\n"
	i=1
	while i<4:
		out+=sent[i]+"\n"
		i+=1
	out+=fourOut(sent[0])+"\n"
	return out

#returns the first 4 words
def fourOut(sent): 
	i=0
	out=""
	while i<4:
		out+=sent.split()[i]+" "
		i+=1
	return out


#main
def main():
	i=0
	sentence=["","","",""]
	while i<4:
		out="Skriv mening nr "+str(i+1)+": "
		sentence[i]=input(out)
		i+=1
	#sentence[0] = "Det fanns ingen fil nar jag handlade pa Konsum."
	#sentence[1] = "Bananerna var ocksa slut."
	#sentence[2] = "Jag kopte brod istallet."
	#sentence[3] = "Nan sorts limpa med mycket fibrer."

	if len(sentence[0].split())<4:
		print("Error, first sentence needs to be atleast 4 characters long")
		return

	print(skriv(sentence))

#calls main
if __name__ == '__main__':
  main()