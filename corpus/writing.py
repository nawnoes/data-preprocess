import os
import json
import kss
from tqdm import tqdm

# 파일 경로
dir_path = "/Volumes/My Passport for Mac/00_nlp/00 모두의 말뭉치/WRITING"
save_file_name ='/Volumes/My Passport for Mac/00_nlp/00 모두의 말뭉치/WRITING.txt'

# 파일 경로 내 목록
dir_list = os.listdir(dir_path)
save_file_path = f'{save_file_name}'
save_file= open(save_file_path,'w',encoding='utf-8')

# 목록 내에 json 파일 읽기
progress_bar1 = tqdm(dir_list,position=0)
for json_file_name in progress_bar1:
    progress_bar1.set_description(f'file name: {json_file_name}')
    json_file_path = f'{dir_path}/{json_file_name}'
    json_file =open(json_file_path,'r',encoding='utf-8')

    try:
        json_data = json.load(json_file)
    except Exception:
        print('error: ', Exception)
        continue
    meta_info = json_data['document'][0]['metadata']
    docs = json_data['document']
    for doc in docs:
        metadata = doc['metadata']
        save_file.write(metadata['title'] + '\n')

        paragraphs = doc['paragraph']
        for paragraph in paragraphs:
            try:
                save_file.write(f'{paragraph["form"]}\n')
                # for sent in kss.split_sentences(paragraph["form"]):
                #     save_file.write(sent.replace('\n', '') + "\n")
            except Exception:
                print('save_file error: ', Exception)
                continue
        save_file.write('\n')
save_file.close()
