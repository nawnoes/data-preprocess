import os
import json
from tqdm import tqdm

# 파일 경로
dir_path = "/Volumes/My Passport for Mac/00_nlp/00 모두의 말뭉치/MESSANGER"
save_file_name ='/Volumes/My Passport for Mac/00_nlp/00 모두의 말뭉치/MESSANGER.txt'

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
        # save_file.write(metadata['title'] + '\n')
        save_file.write(metadata['topic'] + '\n')

        speakers = metadata['speaker']
        speakers_dict = {}
        count =65
        for speaker in speakers:
            save_file.write(f'{chr(count)}={speaker["age"]} {speaker["sex"]} {speaker["occupation"]}\n')
            speakers_dict[speaker['id']] = chr(count)
            count+=1

        paragraphs = doc['utterance']
        for paragraph in paragraphs:
            try:
                save_file.write(f'{speakers_dict[paragraph["speaker_id"]]}: {paragraph["form"]}\n')
            except Exception:
                continue
        save_file.write('\n')
save_file.close()