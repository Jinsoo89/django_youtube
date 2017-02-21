import json
import os

import requests
from dateutil.parser import parse
from django.shortcuts import render, redirect

from video.forms import KeywordForm
from video.models import Video


def get_search_list_from_youtube(keyword):
    # 1. .conf폴더의 settings_local.json을 읽어온다
    # .conf폴더까지의 PATH를 특정화해서 변수에 할당
    # -> print(특정화한 PATH변수) 를 하면
    #       .....(경로)/.conf/settings_local.json
    #            이 출력되어야 함
    # 파이썬에서 파일 읽는 내장함수를 사용해서 결과를 다시 변수에 할당
    # 현재 파일 (youtube/code/youtube.py)

    current_file_path = os.path.abspath(__file__)

    # code디렉토리 보다 한 단계 위, 즉 현재 파이참 프로젝트 루트 폴더 (youtube)
    path_dir_youtube = os.path.dirname(
        os.path.dirname(os.path.dirname(current_file_path)))

    # 루트 폴더의 바로 아래 .conf폴더 (youtube/.conf)
    path_dir_conf = os.path.join(path_dir_youtube, '.conf')

    # .conf폴더 내부의 settings_local.json파일
    path_file_settings_local = os.path.join(path_dir_conf,
                                            'settings_local.json')

    # 파일을 열고 읽고 닫아준다
    # f = open(path_file_settings_local, 'r')
    # config_str = f.read()
    # f.close()
    with open(path_file_settings_local, 'r') as f:
        config_str = f.read()

    # 2. 해당 내용을 json.loads()를 이용해 str -> dict형태로 변환
    # 해당내용 -> 1번에서 최종 결과
    config = json.loads(config_str)
    youtube_api_key = config['youtube']['API_KEY']

    # 3. requests 라이브러리를 이용(pip install requests), GET요청으로 데이터를 받아온 후
    # 이렇게 Parameter와 URL을 분리합니다
    params = {
        'part': 'snippet',
        'q': keyword,
        'maxResults': 5,
        'key': youtube_api_key,
        'type': 'video',
    }
    r = requests.get('https://www.googleapis.com/youtube/v3/search',
                     params=params)
    result = r.text

    # 4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
    result_dict = json.loads(result)

    items = result_dict['items']
    return items


def save_to_db(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        form = KeywordForm()

        # if form.is_valid():
        items = get_search_list_from_youtube(keyword)

        for item in items:
            youtube_id = item['id']['videoId']
            title = item['snippet']['title']
            published_date_str = item['snippet']['publishedAt']
            published_date = parse(published_date_str)
            # title = item.get('snippet').get('title')
            description = item['snippet']['description']
            # youtube_id = item.get('id').get('videoId')
            # published_date = item['snippet']['publishedAt']
            if Video.objects.filter(youtube_id=youtube_id).exists():
                pass
            else:
                Video.objects.create(
                    title=title,
                    description=description,
                    youtube_id=youtube_id,
                    published_date=published_date,
                )

        return redirect('video:search')

    else:
        form = KeywordForm()
    results = Video.objects.all()
    context = {
        'form': form,
        'videos': results,
    }

    return render(request, 'video/search.html', context)
