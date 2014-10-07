#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
keywords=['auto','int','double','long','char','float','short','signed','unsigned','struct','union','enum','static','switch','case','default','break','register','const','volatile','typedef','extern','return','void','continue','do','while','if','else','for','goto','sizeof']
seperatelist=['{', '}', '[', ']', '(', ')', '~', ',', ';', '.', '#', '?', ':']
oplist=['+', '++', '-', '--', '*', '/', '>', '<', '>=', '<=', '=', '==', '!=', '!', '*=', '/=', '+=', '-=']
oct_list= ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e']
ES_list = ['\\', 't', 'a', 'b', 'f', 'n', 'r', 't', 'v', '\'', '\"', '0']
idmaps=[]
result=[]
line = 1
col = 0

def fileoutput(filename):
	fileout=open(filename,'w')
	for line in result:
		fileout.write(line+'\n')
	fileout.close()
def stdoutput():
	for line in result:
		print (line)

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

def is_comment(filein):
	global line
	global col
	tmpline = line
	tmpcol = col
	nextc = filein.read(1)
	tmpcol += 1
	if nextc == '/':
		while 1:
			nextc = filein.read(1)
			tmpline+= 1
			if nextc == '\n':
				col=0
				line=tmpline+1
				break
		return True
	elif nextc == '*':
		commentlen = 0
		state = 0
		while 1:
			nextc=filein.read(1)
			if not nextc:
				outputstr=str(line)+':'+str(col)+"  "+'unterminated /* comment'
				result.append(outputstr)
				filein.seek(-(commentlen+state),1)
				tmpcol-=(commentlen+state)
				break
			tmpcol+=1
			if nextc == '*':
				state=1
				commentlen+=1
			elif nextc == '/' and state == 1:
				line=tmpline
				col=tmpcol
				break
			else:
				if nextc == '\n':
					tmpcol=0
					tmpline+=1
					commentlen+=1
		return True
	else:
		return False	

def get_operation(c,filein):
	global col
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
		col-=1
	return

def char_DFA(filein):
	global col
	global line
	nextchar=filein.read(1)
	col+=1
	nextc=filein.read(1)
	col+=1
	if (nextc=='\''):
		result.append(('sep',nextc))
		result.append(('const',nextchar))
		result.append(('sep',nextc))
	else:
		outputstr=str(line)+':'+str(col)+"  "+'error: unknown character'
		result.append(outputstr)
		filein.seek(-2,1)
		col-=2
	return

def string_DFA(filein):
	global col
	global line
	tmpcol = col
	tmpline = line
	string = ''
	flag = 0
	while 1:
		nextc=filein.read(1)
		if not nextc:
			break
		col += 1
		if nextc=='\"':
			result.append(('sep',nextc))
			result.append(('const',string))
			result.append(('sep',nextc))
			flag = 1
			col = tmpcol
			line = tmpline
			break
		else:
			if (nextc == '\n'):
				tmpcol = 0
				tmpline += 1
			string += nextc
	if not flag == 1:
		outputstr=str(line)+':'+str(col)+"  "+'error: missing terminating \'\"\' character'
		result.append(outputstr)
		filein.seek(-len(string),1)
	return
def scientific_num_DFA(num, filein):
	global col
	global line
	state = 0
	while True:
		nextc = filein.read(1)
		if nextc == '-' and state == 0:
			state = 1
			num += nextc
		elif str.isdigit(nextc):
			num += nextc
		else:
			result.append(('number', num))
			filein.seek(-1, 1)
			return

def number_DFA(c, filein):
	global col
	global line
	num = str(c)
	mode = 0
	while True:
		nextc = filein.read(1)
		col += 1
		if (str.isdigit(nextc)):
			num += nextc
		elif (nextc == '.' and mode == 0):
			mode = 1
			num += nextc
		elif (nextc == 'f' and mode == 1):
			num +=nextc
			result.append(('number', num))
			return
		elif (nextc == 'e'):
			num += nextc
			scientific_num_DFA(num, filein)
			return

		else:
			col -= 1
			result.append(('number', num))
			filein.seek(-1,1)
			return


def oct_DFA(filein):
	global col
	global line
	num = '0x'
	while True:
		nextc = filein.read(1)
		col += 1
		if (str.isdigit(nextc) or nextc in oct_list):
			num += nextc
		else:
			col -= 1
			result.append(('number', num))
			filein.seek(-1,1)
			return


def hex_DFA(filein):
	global col
	global line
	while True:
		nextc = filein.read(1)
		col += 1
		if (str.isdigit(nextc) and nextc not in ['8', '9']):
			num += nextc
		else:
			col -= 1
			result.append(('number', num))
			filein.seek(-1,1)
			return




def doToken(filename):
	global line
	global col
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
		elif str.isspace(c):
			detector(tmpstr)
			tmpstr = ''
			continue
		elif c in seperatelist:
			detector(tmpstr)
			tmpstr = ''
			result.append(('sep',c))
			continue
		elif c == '/':
			if (is_comment(filein)):
				continue
		elif c == '-':
			nextc = filein.read(1)
			if (str.isdigit(nextc)):
				filein.seek(-1, 1)
				number_DFA(c, filein)
				continue
			else:
				filein.seek(-1, 1)
		if c in oplist:
			detector(tmpstr)
			tmpstr = ''
			get_operation(c,filein)
			continue
		elif c == '\'':
			char_DFA(filein)
			continue
		elif c == '\"':
			string_DFA(filein)
			continue
		elif str.isdigit(c):
			if not tmpstr:
				nextc = filein.read(1)
				col += 1
				if (c == 0 and nextc in ['x', 'X'] ):
					hex_DFA(filein)
				if (c == 0 and str.isdigit(nextc)):
					oct_DFA(nextc, filein)
				else:
					col -= 1
					filein.seek(-1, 1)
					number_DFA(c, filein)
			else:
				tmpstr+=c
			continue
		elif isidentify(c):
			tmpstr+=c
			continue
		outputstr = str(line)+':'+str(col)+"  "+'error: illegal character'
		result.append(outputstr)



	

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