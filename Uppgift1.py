#!/usr/local/bin/python3.4
# Programmeringsteknik webbkurs KTH inlämningsuppgift 1
# lucas persson
# 2014-06-15
# räknar ut hur många iterationer som krävs tills skillnaden mellan ett 4 siffrigt tal sorterat LSD och sorterat MSD är 6174 
import sys


def main():
	n=input('Ange ett fyrsiffrigt tal:')
	n=sys.argv[1]
	print(n)
	print('Det tog ',rakna(n),' iterationer att nå 6174.')
	
def rakna(n):
	i=0
	while n!='6174':#framme än?
		if len(n)<2:#fylla upp med 0 ifall 
			n='000'+n
		elif len(n)<3:
			n='00'+n
		elif len(n)<4:
			n='0'+n
		lsd="".join(sorted(n))#sortera på största och minsta
		msd="".join(sorted(n, reverse=True))
		n=str(int(msd)-int(lsd))#räkna
		i=i+1
	return i


if __name__ == '__main__':
  main()