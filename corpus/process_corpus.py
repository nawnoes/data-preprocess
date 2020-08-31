import ijson
import sys
import os
import json
from tqdm import tqdm

# 파일 경로
dir_path = "/Volumes/My Passport for Mac/00_nlp/dialog/messenger"
save_file_name ='/Volumes/My Passport for Mac/00_nlp/dialog/messenger_data.txt'
# 파일 경로 내 목록
dir_list = os.listdir(dir_path)
save_file_path = f'{save_file_name}'
save_file= open(save_file_path,'w',encoding='utf-8')
# 목록 내에 json 파일 읽기
for json_file_name in tqdm(dir_list):

    json_file_path = f'{dir_path}/{json_file_name}'
    json_file =open(json_file_path,'r',encoding='utf-8')

    try:
        json_data = json.load(json_file)
    except Exception:
        print('error: ', Exception)
        continue
    meta_info = json_data['document'][0]['metadata']
    dialogs = json_data['document'][0]['utterance']
    # print(meta_info)
    for dialog in dialogs:
        save_file.write(dialog['form']+'\n')
    save_file.write('\n')
    # print(dialogs)

save_file.close()


# print(dir_list)

