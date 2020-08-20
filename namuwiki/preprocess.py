"""
나무위키 데이터 확
"""
import ijson
import codecs
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
"""
def make_mini_namu(namu_origin, mini_namu, doc_num = 100, is_mini=True):
    count = 0
    mini_file = open(mini_namu, 'w', encoding='utf-8')

    with open(namu_origin, 'r') as fd:
        parser = ijson.parse(fd)
        for prefix, event, value in parser:
            if prefix.endswith('.title'): # 제목
                mini_file.write("\n\n" + clean_punc(value).replace('\n\n', '\n'))
            elif prefix.endswith('.text'): # 내용
                mini_file.write("\n" + clean_punc(value).replace('\n\n', '\n'))
                count += 1
            if is_mini and count == doc_num:  # 10개만 출
                break
    mini_file.close()

"""
특수 문자 제거
"""
def clean_punc(text):
    # punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}}~\"" #+ '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
    my_punct = ['"""', "'''","==","[[", "]]","{{{", "}}}", "!!", "！！","~~", "{{","}}"]
    for p in my_punct:
        text = text.replace(p,'')
    return text.strip()

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
if __name__ == "__main__":
    namu_origin = '../data/docData200302.json'
    mini_namu = 'mini_namu.txt'

    make_mini_namu(namu_origin,mini_namu,is_mini=False)



