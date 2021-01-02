
path = "/Volumes/My Passport for Mac/00_nlp/enwiki/enwik9"

with open(path ,"r",encoding='utf-8') as data:
  while True:
    line =data.readline()
    if not line: break
    print(line)