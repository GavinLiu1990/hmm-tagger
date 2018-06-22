#### 概述

1.此程序主要用于序列标记，比如中文分词(B/E/M/S)，比如词性标注(n/v/a/m...)。 <br>
2.此处HMM模型训练，是监督式学习，即训练文件是带有标记的。 <br>
3.需要python3及以上，需要安装numpy，文件编码格式需为utf8。 <br>

#### 训练HMM模型

>hmm_learn.py  trainfile  modelfile

>比如中文分词  hmm_learn.py  data/pd98month1_wordseg_hmmtrain  data/pd98month1_wordseg_model <br>
>比如词性标注  hmm_learn.py  data/pd98month1_pos_hmmtrain  data/pd98month1_pos_model


#### 测试HMM模型

>hmm_test.py  modelfile  testfile  testresultfile  [options]

>比如中文分词  hmm_test.py  data/pd98month1_wordseg_model data/test_wordseg  data/test_wordseg_result <br>
>比如词性标注  hmm_test.py  data/pd98month1_pos_model  data/test_pos  data/test_pos_result


#### data文件夹下的辅助脚本

* 将分词文本转为hmm训练格式 wordseg2hmmtrain.py

>比如  wordseg2hmmtrain.py  pd98month1_wordseg  pd98month1_wordseg_hmmtrain

* 将词性标注文本转为hmm训练格式 pos2hmmtrain.py

>比如  pos2hmmtrain.py  pd98month1_pos  pd98month1_pos_hmmtrain

* 将分词标记模型转为正常分词 wordseg_result_postproc.py

>比如  wordseg_result_postproc.py  test_wordseg_result  test_wordseg_normal 

#### data文件夹下的辅助文件

pd98month1_wordseg(1998年人民日报1月的分词文本) <br>
pd98month1_wordseg_hmmtrain(1998年人民日报1月的分词hmm训练格式) <br>
pd98month1_pos(1998年人民日报1月的词性标注文本) <br>
pd98month1_pos_hmmtrain(1998年人民日报1月的词性标注hmm训练格式) <br>