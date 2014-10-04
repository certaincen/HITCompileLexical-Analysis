f=open('keywords.txt','r')
fw=open('keywords','w')
while 1:
	line=f.readline()
	if not line:
		break
	word=line.split(' ')[0][0:-1]
	outword='\''+word+'\''
	fw.write(outword+',')
f.close()
fw.close()

