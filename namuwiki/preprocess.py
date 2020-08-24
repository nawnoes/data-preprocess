import ijson
import codecs
import re
import kss
from soynlp.normalizer import *

def load_json(filename):
    count=0
    with open(filename, 'r') as fd:
        parser = ijson.parse(fd)
        for prefix, event, value in parser:
            if prefix.endswith('.title'):
                print('\nindex=', count+1)
                print("TITLE: %s" % value)
            elif prefix.endswith('.text'):
                print("CONTENT: %s" % value)
                count += 1
            if count==10 : # 10개만 출
                break
def load_and_write_content(filename, filename2):
    count=0
    file = codecs.open(filename2, 'w', encoding='utf-8')
    with open(filename, 'r') as fd:
        for item in ijson.items(fd, 'item'):
            count+=1
            file.write('[[제목]]: ')
            file.write(item['title'])
            file.write('\n')
            file.write('[[내용]]: \n')
            file.write(item['text'])
            file.write("\n")
    file.close()
    print('contents count=', count)

"""
doc_num 갯수만큼 나무 위키 데이터 만들기
제목, 내용으로 텍스트 파일 생성
>>> make_mini_namu(namu_origin,mini_namu,is_mini=False)
"""
def make_mini_namu(namu_origin, mini_namu, doc_num = 100, is_mini=True):
    count = 0
    mini_file = open(mini_namu, 'w', encoding='utf-8')

    with open(namu_origin, 'r') as fd:
        parser = ijson.parse(fd)
        for prefix, event, value in parser:
            if prefix.endswith('.title'): # 제목
                mini_file.write("\n\n" + remove_punct(value).replace('\n\n', '\n'))
            elif prefix.endswith('.text'): # 내용
                mini_file.write("\n" + remove_punct(value).replace('\n\n', '\n'))
                count += 1
            if is_mini and count == doc_num:  # 10개만 출
                break
    mini_file.close()

"""
일부 문자 변경
"""
def change_mapping(text, mapping):
    for p in mapping:
        text = text.replace(p, mapping[p])
    return text.strip()

"""
반복 제거
"""
def remove_repeat(text, num_repeats=2):
    text= repeat_normalize(text, num_repeats=num_repeats)
    return text

"""
"""
def namu_preprocess(namu_origin, processed_file):
    file = open(processed_file, 'w', encoding='utf-8')
    r_f= open(namu_origin, 'r')

    while True:
        line = r_f.readline()
        if not line: break

        line = remove_punct(line)
        line = replace_punct(line)
        line = clean_text_using_regexr(line)
        kss_sentence_seperator(file,line)

    file.close()

def clean_html(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def remove_punct(text):
    # punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}}~\"" #+ '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
    my_punct = ['"""', "'''", "===", "[[", "]]", "{{{", "}}}", "!!", "！！", "~~", "{{", "}}",">--", "--" ]
    for p in my_punct:
        text = text.replace(p, '')
    return text.strip()

def replace_punct(text):
    my_punct = {"||":'|'}
    for p in my_punct:
        text = text.replace(p,my_punct[p])
    return text.strip()

def clean_text_using_regexr(raw_html):
  cleaners = [re.compile('<.*?>'),               # html 태그
              re.compile('\[youtube\(.*\)\]()'), # 유튭 태그
              re.compile('\[include\(.*\)\]()'), # include 태그
              re.compile('#[0-9a-f]{3,6}'),      # 정규식 태그
              re.compile('\[\*.*\]'),    # 정규식 태그
            ]


  for cleanr in cleaners:
    raw_html = re.sub(cleanr, '', raw_html)

  return raw_html

"""
문장 분리
"""
def kss_sentence_seperator(file, text):
    for sent in kss.split_sentences(text):
        file.write(sent.replace('\n', '')+"\n")

if __name__ == "__main__":
    namu_origin = '../data/docData200302.json'
    mini_namu = './mini_namu.txt'
    processed_file = './namu_processed.txt'

    namu_preprocess(mini_namu, processed_file)


