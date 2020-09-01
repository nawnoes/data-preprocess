import warnings
warnings.filterwarnings("ignore")

import os
import re
import kss
import json
import logging
import torch
from tqdm import tqdm
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, random_split
from transformers import BertTokenizer

"""
max_len길이의 데이터 셋 생성
"""
def make_data_upto_maxlen( tokenizer, max_len, path="../data/namuwiki.txt"):
    split_data = path.split('.')
    split_data[-2]+= f'-{max_len}'
    return_file_path = '.'.join(split_data)
    logging.info('file name:'+return_file_path)

    return_file= open(return_file_path,'w',encoding='utf-8')
    docs = []
    doc = ""
    doc_len = 0

    num_lines = sum(1 for line in open(path, 'r',encoding='utf-8'))
    logging.info('file line number: '+str(num_lines))
    data_file = open(path, 'r')

    for line in tqdm(data_file,
                     desc='namuwiki data maker',
                     total=num_lines):
        line = line[:-1]
        line_len = len(tokenizer.encode(line))
        added_doc_len = doc_len +line_len
        if line =="":
            return_file.write(doc + "\n")
            doc = ""
            doc_len = 0
        elif  doc_len <max_len and added_doc_len<max_len:
            doc += line
            doc_len += line_len
        elif added_doc_len>= max_len and doc_len<max_len:
            return_file.write(doc+"\n")
            # print(f"max_len-{max_len} real_len-{len(tokenizer.encode(doc))} doc-{doc}\n\n")
            doc = line
            doc_len = line_len
    return_file.close()
    data_file.close()

"""
문장 분리
"""
def kss_sentence_seperator(file, text):
    for sent in kss.split_sentences(text):
        file.write(sent.replace('\n', '')+"\n")


def count_docs_maxlen( tokenizer, path):
    docs_len = []
    doc = ""
    max_value = 0

    num_lines = sum(1 for line in open(path, 'r',encoding='utf-8'))
    logging.info('file line number: '+str(num_lines))
    data_file = open(path, 'r')

    for line in tqdm(data_file,
                     desc='data counter',
                     total=num_lines):
        line = line[:-1]

        if line =="":
            doc_length = len(tokenizer.encode(doc))
            max_value = max(max_value, doc_length)
            docs_len.append(doc_length)
            doc = ""
        else:
            doc +=line
    print(f'max_length-{max_value}')
    print(f'average_length-{sum(docs_len)/len(docs_len)}')

    data_file.close()
if __name__ == '__main__':
    root_dir = "/Users/a60058238/Desktop/dev/workspace/reformer-playground/data/"
    wordpiece_vocab_path = f"{root_dir}/vocab.txt"
    wiki_data_path = f"{root_dir}/namuwiki.txt"



    tokenizer = BertTokenizer(vocab_file=wordpiece_vocab_path, do_lower_case=False)

    count_docs_maxlen(tokenizer, path=wiki_data_path)