import ijson
import codecs
import re
import kss
from tqdm import tqdm
from soynlp.normalizer import *

WIKI_REMOVE_CHARS = re.compile("'+|(=+.{2,30}=+)|__TOC__|(ファイル:).+|:(en|de|it|fr|es|kr|zh|no|fi):|\n")
WIKI_SPACE_CHARS = re.compile("(\\s|゙|゚|　)+")
EMAIL_PATTERN = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
URL_PATTERN = re.compile("(ftp|http|https)?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
WIKI_REMOVE_TOKEN_CHARS = re.compile("(\\*$|:$|^파일:.+|^;)")
MULTIPLE_SPACES = re.compile(' +')


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
                mini_file.write("\n\n\n" + remove_punct(value).replace('\n', ''))
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
        if line =='\n':
            file.write(line)
            continue
        line = remove_punct(line)
        line = replace_punct(line)
        line = clean_text_using_regexr(line)
        line = remove_line(line)
        if line =='':
            continue
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

"""
WIKI_REMOVE_CHARS = re.compile("'+|(=+.{2,30}=+)|__TOC__|(ファイル:).+|:(en|de|it|fr|es|kr|zh|no|fi):|\n", re.UNICODE)
WIKI_SPACE_CHARS = re.compile("(\\s|゙|゚|　)+", re.UNICODE)
EMAIL_PATTERN = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.UNICODE)
URL_PATTERN = re.compile("(ftp|http|https)?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.UNICODE)
WIKI_REMOVE_TOKEN_CHARS = re.compile("(\\*$|:$|^파일:.+|^;)", re.UNICODE)
MULTIPLE_SPACES = re.compile(' +', re.UNICODE)

"""
def clean_text_using_regexr(raw_html):
  cleaners = [re.compile('<.*?>'),               # html 태그
              re.compile('\[youtube\(.*\)\]()'), # 유튭 태그
              re.compile('\[include\(.*\)\]()'), # include 태그
              re.compile('#[0-9a-f]{3,6}'),      # 정규식 태그
              re.compile('\[\*.*\]'),    # 정규식 태그
              # WIKI_REMOVE_CHARS,
              # WIKI_SPACE_CHARS,
              EMAIL_PATTERN,
              URL_PATTERN,
              # WIKI_REMOVE_TOKEN_CHARS,
              # MULTIPLE_SPACES
              ]


  for cleanr in cleaners:
    raw_html = re.sub(cleanr, '', raw_html)

  return raw_html

def remove_line(raw_text):
    cleaner = [
        "#redirect",
    ]
    for pattern in cleaner:
        if pattern in raw_text:
            return ''
        else:
            return raw_text

"""
문장 분리
"""
def kss_sentence_seperator(file, text):
    for sent in kss.split_sentences(text):
        file.write(sent.replace('\n', '')+"\n")

"""
"""
def remove_short_docs(from_file, to_file, cut_len=10):
    file = open(to_file, 'w', encoding='utf-8')
    r_f= open(from_file, 'r')

    # 전체 라인 세기
    num_lines = sum(1 for line in open(from_file, 'r'))
    print(num_lines)
    count = 0
    doc = ""

    for line in tqdm(r_f,
                     desc='namuwiki data maker',
                     total=num_lines):
        if line == "\n":
            if count<3:
                count+=1
            else:
                if len(doc) < cut_len:
                    doc =""
                    count = 1
                else:
                    file.write("\n"+doc)
                    doc = ""
                    count = 1
        elif line != "\n":
            doc += line

    r_f.close()
    file.close()

if __name__ == "__main__":
    namu_origin = '../data/docData200302.json'
    mini_namu = './namuwiki.txt'
    processed_file1 = './namu_processed.txt'
    processed_file2 = './namu_processed-doc.txt'
    # 나무위키 데이터 json -> text
    # make_mini_namu(namu_origin,mini_namu,is_mini=False)

    # 데이터 전처리
    # namu_preprocess(mini_namu, processed_file1)

    # 짧은 문서 삭제
    remove_short_docs(processed_file1,processed_file2,20)

