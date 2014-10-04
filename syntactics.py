#! /usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import re
keywords=['auto','int','double','long','char','float','short','signed','unsigned','struct','union','enum','static','switch','case','default','break','register','const','volatile','typedef','extern','return','void','continue','do','while','if','else','for','goto','sizeof']
seperatelist=['{', '}', '[', ']', '(', ')', '~', ',', ';', '.', '#', '?', ':']
oplist=['+', '++', '-', '--', '*', '/', '>', '<', '>=', '<=', '=', '==', '!=', '!', '*=', '/=', '+=', '-=']
idmaps=[]
result=[]


def fileoutput(filename):
	fileout=open(filename,'w')
	for line in result:
		fileout.write(line+'\n')
	fileout.close()
def stdoutput():
	for line in result:
		print (line)
def addId(idstr):
	if tmpstr not in idmaps.keys():
		result.append('undefinded identify at '+linenum+' rows '+colnum+'cols')
	else:
		result.append((idmaps[tmpstr],tmpstr))

def detector(content):
	if not content:
		return
	if content in keywords:
		result.append(('keywords',content))
	else:
		if content not in idmaps:
			idmaps.append(content)
		result.append(('id',content))


def isidentify(ch):
	if ch=='_' or str.isalpha(ch):
		return True
	return False

def doToken(filename):
	line=1
	col=0
	filein=open(filename,'r')
	tmpstr=''
	while 1:
		c=filein.read(1)
		if not c:
			break
		col+=1
		if c=='\n':
			detector(tmpstr)
			tmpstr=''
			col=0
			line+=1
			continue
		elif c==' ':
			detector(tmpstr)
			tmpstr=''
			continue
		elif c in seperatelist:
			detector(tmpstr)
			tmpstr=''
			result.append(('sep',c))
			continue
		elif c in oplist:
			detector(tmpstr)
			tmpstr=''
			nextc=filein.read(1)
			col+=1
			if nextc in oplist:
				opstr=c+nextc
				if opstr in oplist:
					result.append(('op',opstr))
				else:
					result.append(('op',c))
					result.append(('op',nextc))
			else:
				result.append(('op',c))
				filein.seek(-1,1)
			continue
		elif c == '\'':
			nextchar=filein.read(1)
			col+=1
			nextc=filein.read(1)
			col+=1
			if (nextc=='\''):
				result.append(('sep',c))
				result.append(('const',nextchar))
				result.append(('sep',c))
			else:
				outputstr=str(line)+':'+str(col)+"  "+'error: unknown character'
				result.append(outputstr)
				filein.seek(-2,1)
				col-=2
			continue
		elif c == '\"':
			string=''
			flag=0
			while 1:
				nextc=filein.read(1)
				col+=1
				if not nextc:
					break
				if nextc=='\"':
					result.append(('sep',c))
					result.append(('const',nextchar))
					result.append(('sep',c))
					flag=1
					break
				else:
					string+=nextc
			if not flag==1:
				result.append("missing terminating \'\"\' character")
				filein.seek(-len(string),1)
				col-=len(string)
			continue
		elif str.isdigit(c):
			if not tmpstr:
				number=str(c)
				while 1:
					nextc=filein.read(1)
					if str.isdigit(nextc) or nextc=='.':
						number+=str(nextc)
					else:
						result.append(('number',number))
						filein.seek(-1,1)
						break
			else:
				tmpstr+=c
			continue

		elif isidentify(c):
			tmpstr+=c



	

def main():
	filename=sys.argv[1]
	doToken(filename)
	try:
		if sys.argv[2]:
			fileoutput(sys.argv[2])
	except IndexError:
		pass
	stdoutput()


if __name__=='__main__':
	main()