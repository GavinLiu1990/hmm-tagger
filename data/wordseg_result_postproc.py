import os
import sys

def wordseg_result_postproc(argc, argv):
	if argc < 3:
		print('wordseg_result_postproc.py  wordsegresult  wordsegnormal')
		exit()
	wordsegresult = argv[1]
	wordsegnormal = argv[2]
	with open(wordsegresult, 'r', encoding='utf8') as f1,\
		open(wordsegnormal, 'w', encoding='utf8') as f2:
		resulut = ''
		for line in f1.readlines():
			line = line.strip()
			if line:
				words = line.split()
				if words[1] == 'E' or words[1] == 'S':
					resulut = resulut + words[0] + ' '
				else:
					resulut = resulut + words[0]
			else:
				f2.write(resulut.strip() + '\n')
				resulut = ''
if __name__ =='__main__':
	wordseg_result_postproc(len(sys.argv), sys.argv)