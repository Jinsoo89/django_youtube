"""
1. video app을 생성하고
2. 유투브 영상의 정보를 저장할 수 있는 Model구현, Migrations
3. POST요청을 받으면 요청에서 온 키워드로 유투브를 검색후 결과를 DB에 저장하는 View구현
4. 위 View를 나타낼 수 있는 Template구현
5. View 와 Template연결
6. 실행해보기
"""

"""
1. member app 생성
2. AbstractUser를 상속받은 MyUser를 생성
3. AUTH_USER_MODEL에 등록
4. 마이그레이션 해본다

**extra**
5. Django admin에 MyUser를 등록
6. 기본 UserAdmin을 상속받아 사용자 관련 모듈이 잘 작동하도록 설정
    (기본값으로 두면 패스워드 해싱등이 작동하지 않음)

***bookmark***
1. keyword로 전달받은 검색어를 이용한 결과를 데이터베이스에 저장하는 부분 삭제
2. 결과를 적절히 가공하거나 그대로 템플릿으로 전달
3. 템플릿에서는 해당 결과를 데이터베이를 거치지않고 바로 출력

Next, Prev버튼 추가
1. Youtube Search API에 요청을 보낸 후 결과에
    1-2. nextPageToken만 올 경우에는 첫번째 페이지
    1-3. 둘다 올 경우에는 중간 어딘가
    1-4. prevPageToken만 올 경우에는 마지막 페이지 임을 알 수 있음

2. 템플릿에 nextPageToken, prevPageToken을 전달해서
    해당 token(next 또는 prev)값이 있을경우에 따라
    각각 '다음' 또는 '이전' 버튼을 만들어줌

3. 각 버튼은 a 태그를 사용해
"""

