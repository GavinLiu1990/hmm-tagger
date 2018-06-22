import os
import sys

def pos2hmmtrain(argc, argv):
	if argc < 3:
		print('pos2hmmtrain.py  posfile  poshmmtrainfile')
		exit()
	posfile = argv[1]
	poshmmtrainfile = argv[2]
	with open(posfile, 'r', encoding='utf8') as f1,\
		open(poshmmtrainfile, 'w', encoding='utf8') as f2:
		for line in f1.readlines():
			line = line.strip()
			if not line:
				continue
			words = line.split()
			for word in words:
				if word:
					f2.write(word.split('/')[0] + '	' + word.split('/')[1] + '\n')
			f2.write('\n')
			
if __name__ =='__main__':
	pos2hmmtrain(len(sys.argv), sys.argv)