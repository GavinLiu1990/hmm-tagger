import os
import sys
import math

def hmm_learn(argc, argv):
	if argc != 3:
		print('hmm_learn.py  trainfile  modelfile')
		exit()
	
	trainfile = argv[1]
	modelfile = argv[2]
	
	tag_set = set()
	sym_set = set()
	a_dict = {}
	b_dict = {}
	pi_dict = {}
	
	BEGIN = True
	with open(trainfile, 'r', encoding='utf8') as f:
		for line in f.readlines():
			line = line.strip()
			if line and BEGIN:
				words = line.strip().split()
				
				sym = words[0]
				sym_set.add(sym)
				tag = words[1]
				tag_set.add(tag)
				
				b_key = tag+':'+sym
				if b_key not in b_dict.keys():
					b_dict[b_key] = 1
				else:
					pre_count = b_dict[b_key]
					b_dict[b_key] = pre_count + 1
					
				if tag not in pi_dict.keys():
					pi_dict[tag] = 1
				else:
					pre_count = pi_dict[tag]
					pi_dict[tag] = pre_count + 1
					
				pre_tag = tag
				BEGIN = False
				
			elif line and not BEGIN:
				words = line.strip().split()
				
				sym = words[0]
				sym_set.add(sym)
				tag = words[1]
				tag_set.add(tag)
				
				a_key = pre_tag + ':' + tag
				if a_key not in a_dict.keys():
					a_dict[a_key] = 1
				else:
					pre_count = a_dict[a_key]
					a_dict[a_key] = pre_count + 1
					
				b_key = tag+':'+sym
				if b_key not in b_dict.keys():
					b_dict[b_key] = 1
				else:
					pre_count = b_dict[b_key]
					b_dict[b_key] = pre_count + 1
					
				pre_tag = tag
				BEGIN = False
				
			else:
				BEGIN = True
	
	MIN_VALUE = '-1.0e+100'
	tag_lst = sorted(list(tag_set))
	sym_lst = sorted(list(sym_set))
	with open(modelfile, 'w', encoding='utf8') as f:
	
		f.write('N\n' + str(len(tag_set)) + '\n\n')
		
		f.write('M\n' + str(len(sym_set)) + '\n\n')
		
		f.write('A\n')		
		for tag1 in tag_lst:
			total = 0
			for tag2 in tag_lst:
				a_key = tag1 + ':' + tag2
				if a_key in a_dict.keys():
					total += a_dict[a_key]
			for tag2 in tag_lst:
				a_key = tag1 + ':' + tag2
				if a_key in a_dict.keys():
					f.write(a_key + ' ' + str(math.log(a_dict[a_key]/total)) + '    ')
				else:
					f.write(a_key + ' ' + MIN_VALUE + '    ')
			f.write('\n')
		f.write('\n')

		f.write('B\n')
		for tag in tag_lst:
			total = 0
			for sym in sym_lst:
				b_key = tag + ':' + sym
				if b_key in b_dict.keys():
					total += b_dict[b_key]
			for sym in sym_lst:
				b_key = tag + ':' + sym
				if b_key in b_dict.keys():
					f.write(b_key + ' ' + str(math.log(b_dict[b_key]/total)) + '\n')
				else:
					f.write(b_key + ' ' + MIN_VALUE + '\n')
		f.write('\n')			
		
		f.write('Pi\n')
		total = 0
		for tag in tag_lst:
			if tag in pi_dict.keys():
				total += pi_dict[tag]
		for tag in tag_lst:
			if tag in pi_dict.keys():
				f.write(tag + ' ' + str(math.log(pi_dict[tag]/total)) + '\n')
			else:
				f.write(tag + ' ' + MIN_VALUE + '\n')
				
if __name__ == '__main__':
	hmm_learn(len(sys.argv), sys.argv)