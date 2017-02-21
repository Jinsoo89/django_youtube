"""

"""
import json
import os
from pprint import pprint

import requests

# 1. .conf폴더의 settings_local.json을 읽어온다

# 현재 파일 (youtube/code/youtube.py

current_file_path = os.path.abspath(__file__)

# 현재 파일에서 두단계 부모 디렉토리 (youtube)
go_to_parent_path = os.path.dirname(os.path.dirname(current_file_path))

# .conf 디렉토리 안의 settings_local.json의 경로를 지정
go_to_child_path_or_file = os.path.join(go_to_parent_path,
                                        '.conf/settings_local.json')

# 파일을 열고 읽는다
# f = open(go_to_child_path_or_file, 'r')
# config_str = f.read()
# f.close()
# print(config_str)

with open(go_to_child_path_or_file, 'r') as f:
    config_str = f.read()

print(config_str)
print(type(config_str))

# 2. 해당 내용을 json.loads()를 이용해 str -> dict형태로 반환
config = json.loads(config_str)

youtube_api_key = config['youtube']['API_KEY']


# 3. requests 라이브러리를 이용(pip install requests), GET요청으로 데이터를 받아온 후
params = {
    'part': 'snippet', 'q': '쯔위',
    'key': youtube_api_key, 'maxResults': 50,
}
r = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
result = r.text

# 4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
content1 = json.loads(result)
content2 = content1.get('items')

# 5. 이후 내부에 있는 검색결과를 적절히 루프하여 print해주기


for index, item in enumerate(content2):
    print(index, item['snippet']['title'])

