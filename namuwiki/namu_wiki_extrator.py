import json
import re
import ijson
from namuwiki.extractor import extract_text
from preprocess import kss_sentence_seperator

path = "/Volumes/My Passport for Mac/00_nlp/나무위키/docData200302.json"

capture_values = [
  ("item.namespace", "string"),
  ("item.title", "string"),
  ("item.text", "string")
]


def parse_namuwiki_json(limit=-1, debug=False):
  i = 0
  doc = {}
  with open(path) as f:
    for prefix, event, value in ijson.parse(f):

      if debug:
        print(prefix, event, value)
      if (prefix, event) in capture_values:
        doc[prefix[5:]] = value
      if (prefix, event, value) == ("item", "end_map", None):
        yield doc
        doc = {}
        i += 1

        if limit > 0 and i >= limit:
          break

cleaning_first_patterns = [
  r"~~[^~]+~~"
]
cleaning_first_patterns = [re.compile(pattern, re.IGNORECASE | re.MULTILINE) for pattern in cleaning_first_patterns]

cleaning_patterns = [
  # 괄호와 그 내용들 제거,
  # 안녕(하세요) -> 안녕
  r"\([^\)]+\)"
  r"/^#[0-9a-f]{3,6}$/i"
]
cleaning_patterns = [re.compile(pattern, re.IGNORECASE | re.MULTILINE) for pattern in cleaning_patterns]

# \n -> 띄어쓰기
# \' -> '
replace_patterns = {
  '\\n': "\n",
  "\\'": "'"
}


def clean_text(text):
  for regex in cleaning_first_patterns:
    text = re.sub(regex, "", text)

  text = extract_text(text)

  for regex in cleaning_patterns:
    text = re.sub(regex, "", text)
  for k, v in replace_patterns:
    text = text.replace(k, v)
  return text

if __name__=="__main__":
  processed_file = "../namuwiki/namuwiki.txt"
  file = open(processed_file, 'w', encoding='utf-8')
  flag = True
  for doc in parse_namuwiki_json():
    # print(doc['text'])
    # print("===" * 10)
    doc['title'] = clean_text(doc['title'])
    doc['text'] = clean_text(doc['text'])
    plain = doc['text'].replace('\n\n','\n')
    if len(plain)<5:
      continue
    if flag:
      file.write(doc['title'] + "\n")
      flag = False
    else:
      file.write("\n"+doc['title']+"\n")
    kss_sentence_seperator(file,plain)
