"""
1. video app을 생성하고
2. 유투브 영상의 정보를 저장할 수 있는 Model구현, Migrations
3. POST요청을 받으면 요청에서 온 키워드로 유투브를 검색후 결과를 DB에 저장하는 View구현
4. 위 View를 나타낼 수 있는 Template구현
5. View 와 Template연결
6. 실행해보기
"""

from django.db import models

# class VideoManager(models.Manager):
#     def


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    # url = models.URLField()
    youtube_id = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return 'the title of this video is {}'.format(self.title)