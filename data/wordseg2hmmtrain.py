import os
import sys

def wordseg2hmmtrain(argc, argv):
	if argc < 3:
		print('wordseg2hmmtrain.py  wordsegfile  wordseghmmtrainfile')
		exit()
	wordsegfile = argv[1]
	wordseghmmtrainfile = argv[2]
	with open(wordsegfile, 'r', encoding='utf8') as f1,\
		open(wordseghmmtrainfile, 'w', encoding='utf8') as f2:
		for line in f1.readlines():
			line = line.strip()
			if not line:
				continue
			words = line.split()
			for word in words:
				if word:
					length = len(word)
					if length == 1:
						f2.write(word + '	' + 'S' + '\n')
					elif length == 2:
						f2.write(word[0] + '	' + 'B' + '\n')
						f2.write(word[1] + '	' + 'E' + '\n')
					else:
						f2.write(word[0] + '	' + 'B' + '\n')
						for i in range(1, length - 1):
							f2.write(word[i] + '	' + 'M' + '\n')
						f2.write(word[-1] + '	' + 'E' + '\n')
			f2.write('\n')
			
if __name__ =='__main__':
	wordseg2hmmtrain(len(sys.argv), sys.argv)