import json

import requests
from dateutil.parser import parse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render

from member.models import BookmarkVideo
from utils.settings import get_setting
from video.models import Video

"""
170222 숙제
1. 북마크 기능을 만든다.
    검색 결과의 각 아이템에 '북마크하기'버튼을 만들어서 누르면 DB에 저장
2. 북마크 목록 보기 페이지를 만든다.
    북마크한 영상 목록을 볼 수 있는 페이지 구현
**extra
3. 사용자 별로 북마크를 구분할 수 있도록 한다.
4. 검색 결과에서 이미 북마크를 누른 영상은
    '북마크 되어있음' 또는 '북마크 해제'버튼이 나타나도록 한다.
5. 북마크 목록에서 해당 아이템을 클릭 할 경우 유튜브 페이지로 이동하지 않고,
    자체 video_detail페이지를 구현해서 보여주도록 한다.
6. 그외 넣고싶은 기능 마음껏 넣어보기
7. 또는 CSS로 반응형 모바일 만들어보기
8. 로그인/회원가입 만들기
"""


def search_from_youtube(keyword, page_token=None):
    youtube_api_key = get_setting()['youtube']['API_KEY']

    # 3. requests 라이브러리를 이용(pip install requests), GET요청으로 데이터를 받아온 후
    # 이렇게 Parameter와 URL을 분리합니다
    params = {
        'part': 'snippet',
        'q': keyword,
        'maxResults': 15,
        'key': youtube_api_key,
        'type': 'video',
    }
    r = requests.get('https://www.googleapis.com/youtube/v3/search',
                     params=params)
    # print(type(r))
    result = r.text

    # 4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
    result_dict = json.loads(result)

    return result_dict


def search_results(request):
    videos = []
    context = {
        'videos': videos,
    }
    # 포스트일 경우에만 검색결과에 내용이 추가됨
    keyword = request.GET.get('keyword', '').strip()
    page_token = request.GET.get('page_token')

    if keyword != '':
        search_result = search_from_youtube(keyword, page_token)

        next_page_token = search_result.get('nextPageToken')
        prev_page_token = search_result.get('prevPageToken')
        total_results = search_result['pageInfo'].get('totalResults')
        context['next_page_token'] = next_page_token
        context['prev_page_token'] = prev_page_token
        context['total_results'] = total_results

        items = search_result['items']
        for item in items:
            published_date_str = item['snippet']['publishedAt']

            # 다음페이지 있냐 없냐

            youtube_id = item['id']['videoId']
            title = item['snippet']['title']
            published_date = parse(published_date_str)
            description = item['snippet']['description']
            url_thumbnail = item['snippet']['thumbnails']['high']['url']
            is_exist = BookmarkVideo.objects.filter(
                user=request.user,
                video__youtube_id=youtube_id,
            ).exists()

            cur_item_dict = {
                "title": title,
                "description": description,
                'published_date': published_date,
                'youtube_id': youtube_id,
                'url_thumbnail': url_thumbnail,
                'is_exist': is_exist,
            }

            videos.append(cur_item_dict)

    return render(request, 'video/search.html', context)


def delete_video(request, id_to_delete):
    if request.method == "POST":
        video = Video.objects.filter(youtube_id=id_to_delete)
        video.delete()

        return redirect('video:search')


@login_required
def bookmark_toggle(request):

    def get_or_create_video_and_add_bookmark():
        defaults = {
            'title': title,
            'description': description,
            'published_date': published_date,
            'url_thumbnail': url_thumbnail,
        }
        video, _ = Video.objects.get_or_create(
            defaults=defaults,
            youtube_id=youtube_id,
        )

        # 중간자 모델 없이 M2M필드에 바로 인스턴스를 추가할때
        # request.user.bookmark_videos.add(video)

        # BookmarkVideo 중간자 모델의 매니저를 직접사용
        # BookmarkVideo.objects.create(
        #     user=request.user,
        #     video=video,
        # )

        # MyUser와 중간자모델을 연결시켜주는 related_manager를 사용
        request.user.bookmarkvideo_set.create(
            video=video,
        )

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        youtube_id = request.POST['youtube_id']
        url_thumbnail = request.POST['url_thumbnail']
        published_date_str = request.POST['published_date']
        published_date = parse(published_date_str)
        prev_path = request.POST['path']

        # 이미 북마크가 되어 있는지 확인
        exist_bookmark_list = request.user.bookmarkvideo_set.filter(
            video__youtube_id=youtube_id)
        if exist_bookmark_list:
            exist_bookmark_list.delete()
        else:
            get_or_create_video_and_add_bookmark()

        return redirect(prev_path)


@login_required
def bookmark_list(request):
    all_bookmarks = request.user.bookmarkvideo_set.select_related('video')

    # 전체 북마크 리스트를 페이지네이션 처리리
    paginator = Paginator(all_bookmarks, 5)
    page = request.GET.get('page')
    try:
        bookmarks = paginator.page(page)
    except PageNotAnInteger:
        bookmarks = paginator.page(1)
    except EmptyPage:
        bookmarks = paginator.page(paginator.num_pages)

    context = {
        'bookmarks': bookmarks,
    }

    return render(request, 'video/bookmark_list.html', context)

# def bookmark(request):
#     if request.method == 'POST':
#         r = request.POST['video']
#         print(type(r))
#         print(r)
#         new_r = r.replace('\'', '"').replace(' ', '')
#         print(new_r)
#         temp = json.loads(new_r)
#
#         Video.objects.create(
#             # title=temp['title'],
#             # description=temp['description']
#             # youtube_id=temp['youtube_id'],
#             # published_date=temp['published_date'],
#         )
#         print('hello')
#         return redirect('video:bookmark')
#
#     bookmarked_list = Video.objects.all()
#     context = {
#         'bookmarked_list': bookmarked_list,
#     }
#
#     return render(request, 'video/bookmark_list.html', context)


# def save_to_db(request):
#     if request.method == 'POST':
#         # keyword = request.POST['keyword']
#         form = KeywordForm(request.POST)
#
#         if form.is_valid():
#             keyword = form.cleaned_data['keyword']
#             items = get_search_list_from_youtube(keyword)
#
#             for item in items:
#                 youtube_id = item['id']['videoId']
#                 title = item['snippet']['title']
#                 published_date_str = item['snippet']['publishedAt']
#                 published_date = parse(published_date_str)
#                 # title = item.get('snippet').get('title')
#                 description = item['snippet']['description']
#                 # youtube_id = item.get('id').get('videoId')
#                 # published_date = item['snippet']['publishedAt']
#                 defaults = {
#                     'title': title,
#                     'description': description,
#                     'published_date': published_date
#                 }
#
#                 Video.objects.get_or_create(
#                     youtube_id=youtube_id,
#                     defaults=defaults
#                 )
#             return redirect('video:search')
#     else:
#         form = KeywordForm()
#     results = Video.objects.all()
#     context = {
#         'form': form,
#         'videos': results,
#     }
#
#     return render(request, 'video/search.html', context)
