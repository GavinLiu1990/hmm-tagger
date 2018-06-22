import os
import sys
import math
import numpy as np
import getopt

MIN_VALUE = -1.0e+100

def usage():
	print('hmm_test.py  modelfile  testfile  testresultfile  [options]\n\
options:\n\
-d  debug info such as viterbi probability, forward probability, backward probability, 0/1, default=0')

def B_proc(B, b_key, N):
	if b_key in B.keys():
		return(B[b_key])
	else:
		return(math.log(1 / N))

		 
def viterbi(N, M, A, B, Pi, O):
	T = len(O)
	delta = np.zeros([T, N])
	path = np.zeros([T, N], dtype=np.int)
	tmp_dict = {}
	tag = sorted(Pi.keys())
	for i in range(N):
		tmp_dict[i] = tag[i]
	for n in range(N):
		delta[0][n] = Pi[tmp_dict[n]] + B_proc(B, tmp_dict[n]+':'+O[0], N)
		path[0][n] = n
	for t in range(1, T):
		for n1 in range(N):
			max = delta[t-1, 0] + A[tmp_dict[0]+':'+tmp_dict[n1]]
			maxid = 0
			for n2 in range(1, N):
				val = delta[t-1, n2] + A[tmp_dict[n2]+':'+tmp_dict[n1]]
				if val > max:
					max = val
					maxid = n2				
			delta[t][n1] = max + B_proc(B, tmp_dict[n1]+':'+O[t], N)
			path[t][n1] = maxid

	final_lst = []
	max = delta[T-1][0]
	maxid = 0
	for n in range(1, N):
		if delta[T-1][n] > max:
			max = delta[T-1][n]
			maxid = n
	final_lst.append(tmp_dict[maxid])
	
	t = T-2
	while(t >= 0):
		final_lst.append(tmp_dict[path[t+1][maxid]])
		maxid = path[t+1][maxid]
		t -= 1

	return final_lst[::-1], max


def forward(N, M, A, B, Pi, O):
	T = len(O)
	alpha = np.zeros([T, N])
	tmp_dict = {}
	tag = sorted(Pi.keys())
	for i in range(N):
		tmp_dict[i] = tag[i]
	for n in range(N):
		alpha[0][n] = Pi[tmp_dict[n]] + B_proc(B, tmp_dict[n]+':'+O[0], N)
	for t in range(1, T):
		for n1 in range(N):
			partial_sum = 0
			for n2 in range(N):
				partial_sum += math.exp(alpha[t-1][n2] + A[tmp_dict[n2]+':'+tmp_dict[n1]])
			if partial_sum == 0:
				alpha[t][n1] = MIN_VALUE + B_proc(B, tmp_dict[n1]+':'+O[t], N)
			else:
				alpha[t][n1] = math.log(partial_sum) + B_proc(B, tmp_dict[n1]+':'+O[t], N)
	final_sum = 0
	for n in range(N):
		final_sum += math.exp(alpha[T-1][n])
	return math.log(final_sum)

def backward(N, M, A, B, Pi, O):
	T = len(O)
	beta = np.zeros([T, N])
	tmp_dict = {}
	tag = sorted(Pi.keys())
	for i in range(N):
		tmp_dict[i] = tag[i]
	for n in range(N):
		beta[T-1][n] = 0
	t = T - 2
	while(t >= 0):
		for n1 in range(N):
			partial_sum = 0
			for n2 in range(N):
				partial_sum += math.exp(A[tmp_dict[n1]+':'+tmp_dict[n2]] + B_proc(B, tmp_dict[n2]+':'+O[t+1], N) + beta[t+1][n2])
			if partial_sum == 0:
				beta[t][n1] = MIN_VALUE
			else:
				beta[t][n1] = math.log(partial_sum)
			
		t -= 1
	final_sum = 0
	for n in range(N):
		final_sum += math.exp(Pi[tmp_dict[n]] + B_proc(B, tmp_dict[n]+':'+O[0], N) + beta[0][n])
	return math.log(final_sum)
	
def readmodel(modelfile):
	with open(modelfile, 'r', encoding='utf8') as f:
		N = 0
		M = 0
		A = {}
		B = {}
		Pi = {}
		
		f_N = False
		f_M = False
		f_A = False
		f_B = False
		f_Pi = False
		
		for line in f.readlines():
			line  = line.strip()
			if line == 'N':
				f_N = True
				continue
			elif line == 'M':
				f_M = True
				continue
			elif line == 'A':
				f_A = True
				continue
			elif line == 'B':
				f_B = True
				continue
			elif line == 'Pi':
				f_Pi = True
				continue
		
			if f_N and line:
				N = int(line)
			elif f_N and not line:
				f_N = False
			elif f_M and line:
				M = int(line)
			elif f_M and not line:
				f_M = False
			elif f_A and line:
				words = line.split('    ')
				for word in words:
					if word:
						A[word.split(' ')[0]] = float(word.split(' ')[1])
			elif f_A and not line:
				f_A = False
			elif f_B and line:
				words = line[::-1].split(' ',1)
				B[words[1][::-1]] = float(words[0][::-1])
			elif f_B and not line:
				f_B = False
			elif f_Pi and line:
				words = line.split()
				Pi[words[0]] = float(words[1])		
	return N, M, A, B, Pi
	
def hmm_test(argc, argv):
	if argc < 4:
		usage()
		exit()
		
	modelfile = argv[1]
	testfile = argv[2]
	testresultfile = argv[3]
	
	opts, args = getopt.getopt(sys.argv[4:],"d:")
	debug = False
	for opt, value in opts:
		if opt == '-d':
			dflag = int(value)
			if dflag != 0:
				debug = True
		
	N, M, A, B, Pi = readmodel(modelfile)
	
	with open(testfile, 'r', encoding='utf8') as f1,\
		open(testresultfile, 'w', encoding='utf8') as f2:
		sents = f1.readlines()
		sentnum = len(sents)
		O = []
		n = 0
		for sent in sents:
			n += 1
			sent = sent.strip('\n')
			if sent:
				O.append(sent)		
			if not sent or n == sentnum:
				tag_lst, pv = viterbi(N, M, A, B, Pi, O)
				length1 = len(tag_lst)
				length2 = len(O)
				if length1 == length2:
					for i in range(length1):
						f2.write(O[i] + '	' + tag_lst[i] + '\n')
					if debug:
						pf = forward(N, M, A, B, Pi, O)
						pb = backward(N, M, A, B, Pi, O)
						f2.write('viterbi probability:' + str(pv) + '\n')
						f2.write('forward probability:' + str(pf) + '\n')
						f2.write('backward probability:' + str(pb) + '\n')
					f2.write('\n')				
				O = []
						
if __name__ == '__main__':
	hmm_test(len(sys.argv), sys.argv)