"""
1. video app을 생성하고
2. 유투브 영상의 정보를 저장할 수 있는 Model구현, Migrations
3. POST요청을 받으면 요청에서 온 키워드로 유투브를 검색후 결과를 DB에 저장하는 View구현
4. 위 View를 나타낼 수 있는 Template구현
5. View 와 Template연결
6. 실행해보기
"""
from django.conf import settings
from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    youtube_id = models.CharField(unique=True, max_length=100)
    url_thumbnail = models.URLField(max_length=300, blank=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title



