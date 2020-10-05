<h1 align="center">📄 투표게시판 EN;COD 👨‍💻</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.2.0-blue.svg?cacheSeconds=2592000" />
</p>

## 완성 결과
<img alt="finish" src="https://github.com/cwadven/encod/blob/master/%EB%8B%AC%EA%B3%A0%EB%82%98.png?raw=true" />

### 서비스 주소
http://dalgona.shop/

## 개발자
👤 김수연
- Github : https://github.com/su100
- Frontend : React

👤 이창우
- Github : https://github.com/cwadven
- Backend : Django Rest Framework
- Service : AWS ec2 (Ubuntu), RDS (mysql)
- Server : nginx (uwsgi)

## 디자이너
👤 김가영
- Github : https://github.com/joanna-hash
- Tool : Figma

## 환경 구축
0. python -m venv myvenv (가상환경 생성)
1. python source myvenv/scripts/activate (가상환경 실행)
2. pip install -r requirements.txt
3. python manage.py collectstatic
4. python manage.py runserver

~~~
추가적인 기능을 위해서
가상환경에 있는 라이브러리중 rest_auth의
app_settings.py
serializers.py
views.py
코드 수정 필요

app_settings.py
JWTSerializer2 = import_callable(
    serializers.get('JWT_SERIALIZER', DefaultJWTSerializer2))
추가

serializers.py
class JWTSerializer2(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    token = serializers.CharField()
    user = serializers.SerializerMethodField()
    superuser = serializers.BooleanField()

    def get_user(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        rest_auth_serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})
        JWTUserDetailsSerializer = import_callable(
            rest_auth_serializers.get('USER_DETAILS_SERIALIZER', UserDetailsSerializer)
        )
        user_data = JWTUserDetailsSerializer(obj['user'], context=self.context).data
        return user_data
추가

views.py
from .app_settings import ( 안에
JWTSerializer2 추가

또한

Class LoginView() 쪽에서
def get_response_serializer(self):
    if getattr(settings, 'REST_USE_JWT', False):
        response_serializer = JWTSerializer2
    else:
        response_serializer = TokenSerializer
    return response_serializer

JWTSerializer를 JWTSerializer2로 수정

~~~

## API 사용 방법
### 회원가입 (POST)
http://127.0.0.1:8000/rest-auth/registration

#### Request
**[Body]** --> form-data
- username : 아이디
- password1 : 비밀번호
- password2 : 비밀번호 확인
- nickname : 닉네임

❌ 제약조건 : 
username - 중복이 없어야 한다
nickname - 중복이 없어야 한다, 3글자 이상이어야 한다

#### Response
{"token": "jwt ~~~~~~~~~~~~~"}
user : { "username": "아이디", "email":"이메일", "nickname": "닉네임" }

<hr>

### 로그인 (POST)
http://127.0.0.1:8000/rest-auth/login

**[Body]** --> form-data
- username : 아이디
- password : 비밀번호

#### Response
{"token": "jwt ~~~~~~~~~~~~~"}

<hr>

### 회원정보 수정 (PUT)
http://localhost:8000/accounts/user

❌ 제약조건 : 로그인 한 사람만 접근 가능

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

**[Body]** --> form-data
- nickname : 닉네임

#### Response
{<br>
    "username": "아이디",<br>
    "email": "이메일",<br>
    "nickname": "닉네임"<br>
} 

<hr>

### 회원 삭제 (DELETE)
http://localhost:8000/accounts/user

❌ 제약조건 : 로그인 한 사람만 접근 가능

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

#### Response
{<br>
    detial:'user deleted'
} 

<hr>

### 비밀번호 수정 (POST)
http://127.0.0.1:8000/rest-auth/password/change

❌ 제약조건 : 로그인 한 사람만 접근 가능

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

**[Body]** --> form-data
- new_password1 : 비밀번호
- new_password2 : 비밀번호 확인

#### Response
{<br>
    "detail": "New password has been saved."<br>
}

<hr>

### 로그아웃 (POST)
http://127.0.0.1:8000/rest-auth/logout

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

#### Response
{
    "detail": "Successfully logged out."
}

<hr>

### 투표 게시글 목록 가져오기 (GET)
http://localhost:8000/board

**[헤더s]** --> form-data
- Authorization : jwt ~~~~~~~~~~~
(이게 있어야 로그인자가 투표를 했는지 안했는지 알 수 있습니다)

**[Params]**
[필수사항 아님]
- ended=0 혹은 false : 진행중 투표게시판
- ended=1 혹은 true : 끝난 투표게시판
- voted=0 혹은 false : 투표 참가하지 않은 투표게시판
- voted=1 혹은 true : 투표 참가한 투표게시판

#### Response
[<br>
    {<br>
        "id": 1, (해당 게시글의 id)<br>
        "title": "가장 좋아하는 프로그래밍 언어", (제목)<br>
        "voter_count": 1, (총 몇명이 투표를 했는지)<br>
        "contents": [ (해당 게시글의 투표 컨텐츠들)<br>
            {<br>
                "id": 1, (투표 컨텐츠 id)<br>
                "boardid": 1, (이 투표 컨텐츠를 포함하는 게시글 id)<br>
                "title": "자바", (제목)<br>
                "created_at": "2020-09-30T23:32:55.523007+09:00", (생성날짜)<br>
                "updated_at": "2020-09-30T23:36:21.456401+09:00", (수정날짜 --> 투표하기 하면 계속 최신화됩니다)<br>
                "voter_count": 1, (이 투표 컨텐츠에 투표한 명수)<br>
                "voted": true, (로그인자가 투표를 했는지 --> Header에 jwt를 보내면 내가 투표를 했었는지 알 수 있다)<br>
                "image": null (이 투표 컨텐츠의 사진)<br>
            }<br>
        ],<br>
        "winner_id": [<br>
            1 (투표 컨텐츠의 투표수가 많은 것 --> 리스트로 감싼 이유는 동점도 있을 수 있기 때문에 설정)<br>
        ],<br>
        "ended": false, (끝난 투표 게시글인지 알기)<br>
        "voted": true, (내가 이 투표 게시글에 투표를 했는지 알기)<br>
        "created_at": "2020-09-30T23:30:29.209573+09:00", (투표 게시판이 만들어진 시간)<br>
        "updated_at": "2020-09-30T23:30:29.209573+09:00" (투표 게시판이 수정된 시간)<br>
    },<br>
    ..... 여러개!<br>
]

<hr>

### 투표 게시글 내용 가져오기 (GET)
http://localhost:8000/board/(boardId)

**[헤더s]** --> form-data
- Authorization : jwt ~~~~~~~~~~~
(이게 있어야 로그인자가 투표를 했는지 안했는지 알 수 있습니다)

#### Response
{<br>
    "id": 1, (해당 게시글의 id)<br>
    "title": "가장 좋아하는 프로그래밍 언어", (제목)<br>
    "voter_count": 1, (총 몇명이 투표를 했는지)<br>
    "contents": [ (해당 게시글의 투표 컨텐츠들)<br>
        {<br>
            "id": 1, (투표 컨텐츠 id)<br>
            "boardid": 1, (이 투표 컨텐츠를 포함하는 게시글 id)<br>
            "title": "자바", (제목)<br>
            "created_at": "2020-09-30T23:32:55.523007+09:00", (생성날짜)<br>
            "updated_at": "2020-09-30T23:36:21.456401+09:00", (수정날짜 --> 투표하기 하면 계속 최신화됩니다)<br>
            "voter_count": 1, (이 투표 컨텐츠에 투표한 명수)<br>
            "voted": true, (로그인자가 투표를 했는지 --> Header에 jwt를 보내면 내가 투표를 했었는지 알 수 있다)<br>
            "image": null (이 투표 컨텐츠의 사진)<br>
        }<br>
    ],<br>
    "winner_id": [<br>
        1 (투표 컨텐츠의 투표수가 많은 것 --> 리스트로 감싼 이유는 동점도 있을 수 있기 때문에 설정)<br>
    ],<br>
    "ended": false, (끝난 투표 게시글인지 알기)<br>
    "voted": true, (내가 이 투표 게시글에 투표를 했는지 알기)<br>
    "created_at": "2020-09-30T23:30:29.209573+09:00", (투표 게시판이 만들어진 시간)<br>
    "updated_at": "2020-09-30T23:30:29.209573+09:00" (투표 게시판이 수정된 시간)<br>
}

<hr>

### 투표 게시글 쓰기 (POST)
http://localhost:8000/board

❌ 제약조건 : superuser만 작성 가능

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~
(이게 있어야 로그인자가 투표를 했는지 안했는지 알 수 있습니다)

**[Body]** --> form-data
- title : 제목 [필수는 아님]
- ended : true 혹은 false (완료되었는지 default는 false 이다) [필수는 아님]

#### Response
{<br>
    "id": 2, (해당 게시글의 id)<br>
    "title": "", (제목)<br>
    "voter_count": 0, (총 몇명이 투표를 했는지)<br>
    "contents": [], (해당 게시글의 투표 컨텐츠들)<br>
    "winner_id": [], (투표 컨텐츠의 투표수가 많은 것 --> 리스트로 감싼 이유는 동점도 있을 수 있기 때문에 설정)<br>
    "ended": false, (끝난 투표 게시글인지 알기)<br>
    "voted": false, (로그인자가 투표를 했는지 --> Header에 jwt를 보내면 내가 투표를 했었는지 알 수 있다)<br>
    "created_at": "2020-10-01T00:13:10.676685+09:00", (투표 게시판이 만들어진 시간)<br>
    "updated_at": "2020-10-01T00:13:10.676685+09:00" (투표 게시판이 수정된 시간)<br>
}

<hr>

### 투표 게시글 삭제 (DELETE)
http://localhost:8000/board/(boardId)

❌ 제약조건 : superuser만 작성 삭제

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

#### Response
NONE

<hr>

### 투표 게시글 수정 (PUT)
http://localhost:8000/board/(boardId)

❌ 제약조건 : superuser만 작성 수정

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

**[Body]** --> form-data
- title : 제목 [필수는 아님]
- ended : true 혹은 false (완료되었는지 default는 false 이다) [필수는 아님]

#### Response
{<br>
    "id": 2, (해당 게시글의 id)<br>
    "title": "", (제목)<br>
    "voter_count": 0, (총 몇명이 투표를 했는지)<br>
    "contents": [], (해당 게시글의 투표 컨텐츠들)<br>
    "winner_id": [], (투표 컨텐츠의 투표수가 많은 것 --> 리스트로 감싼 이유는 동점도 있을 수 있기 때문에 설정)<br>
    "ended": false, (끝난 투표 게시글인지 알기)<br>
    "voted": false, (로그인자가 투표를 했는지 --> Header에 jwt를 보내면 내가 투표를 했었는지 알 수 있다)<br>
    "created_at": "2020-10-01T00:13:10.676685+09:00", (투표 게시판이 만들어진 시간)<br>
    "updated_at": "2020-10-01T00:13:10.676685+09:00" (투표 게시판이 수정된 시간)<br>
}

<hr>

## 투표 기능
### 투표 컨텐츠 생성 (POST)
http://127.0.0.1:8000/voteboard

❌ 제약조건 : 투표 게시글의 작성자만 작성 가능 (투표 게시글은 superuser만 생성 가능하기 때문에 결국 superuser야 한다)

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

**[Body]** --> form-data
- boardid (어느 투표 게시글에 속하는 것인지) [필수]
- title : 제목 [필수는 아님]
- image : 이미지 [필수는 아님]

#### Response
{<br>
    "id": 1, (투표 컨텐츠 id)<br>
    "boardid": 1, (이 투표 컨텐츠를 포함하는 게시글 id)<br>
    "title": "자바", (제목)<br>
    "created_at": "2020-09-30T23:32:55.523007+09:00", (생성날짜)<br>
    "updated_at": "2020-09-30T23:36:21.456401+09:00", (수정날짜 --> 투표하기 하면 계속 최신화됩니다)<br>
    "voter_count": 0, (이 투표 컨텐츠에 투표한 명수)<br>
    "voted": true, (로그인자가 투표를 했는지 --> Header에 jwt를 보내면 내가 투표를 했었는지 알 수 있다)<br>
    "image": null (이 투표 컨텐츠의 사진)<br>
}

<hr>

### 투표 컨텐츠 전부 가져오기 (GET)
http://127.0.0.1:8000/voteboard

(이게 있어야 로그인자가 투표를 했는지 안했는지 알 수 있습니다)

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

#### Response
[<br>
    {<br>
        "id": 1, (투표 컨텐츠 id)<br>
        "boardid": 1, (이 투표 컨텐츠를 포함하는 게시글 id)<br>
        "title": "자바", (제목)<br>
        "created_at": "2020-09-30T23:32:55.523007+09:00", (생성날짜)<br>
        "updated_at": "2020-09-30T23:36:21.456401+09:00", (수정날짜 --> 투표하기 하면 계속 최신화됩니다)<br>
        "voter_count": 0, (이 투표 컨텐츠에 투표한 명수)<br>
        "voted": true, (로그인자가 투표를 했는지 --> Header에 jwt를 보내면 내가 투표를 했었는지 알 수 있다)<br>
        "image": null (이 투표 컨텐츠의 사진)<br>
    }<br>
    ....<br>
]

<hr>

### 투표 컨텐츠 특정 가져오기 (GET)
http://127.0.0.1:8000/voteboard/(voteboardid)

(이게 있어야 로그인자가 투표를 했는지 안했는지 알 수 있습니다)

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

#### Response
{<br>
    "id": 1, (투표 컨텐츠 id)<br>
    "boardid": 1, (이 투표 컨텐츠를 포함하는 게시글 id)<br>
    "title": "자바", (제목)<br>
    "created_at": "2020-09-30T23:32:55.523007+09:00", (생성날짜)<br>
    "updated_at": "2020-09-30T23:36:21.456401+09:00", (수정날짜 --> 투표하기 하면 계속 최신화됩니다)<br>
    "voter_count": 0, (이 투표 컨텐츠에 투표한 명수)<br>
    "voted": true, (로그인자가 투표를 했는지 --> Header에 jwt를 보내면 내가 투표를 했었는지 알 수 있다)<br>
    "image": null (이 투표 컨텐츠의 사진)<br>
}

<hr>

### 투표 컨텐츠에 투표하기 (POST)
http://127.0.0.1:8000/voteboard/(voteboardid)

(이게 있어야 로그인자가 투표를 했는지 안했는지 알 수 있습니다)
❌ 제약조건 : jwt로 로그인한 사람만 투표 가능

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

#### Response
- 해당으로 POST를 보내면 voted가 false일 경우 true로 바뀌고 true 였을 경우는 false로 바뀐다.
- voted가 true가 되면 voter_count가 올라가고 voted가 false가 되면 voter_count가 내려간다.
- 만약에 투표 컨텐츠에 1개라도 true가 있을 경우 투표 게시글의 voted는 true가 된다.
- 만약 false로 바뀌는 경우 투표 게시판에 있는 voter_count 또한 빼기가 된다.
- 투표는 오로지 투표 컨텐츠에서 1개만 투표 가능하다!

{<br>
    "id": 1, (투표 컨텐츠 id)<br>
    "boardid": 1, (이 투표 컨텐츠를 포함하는 게시글 id)<br>
    "title": "자바", (제목)<br>
    "created_at": "2020-09-30T23:32:55.523007+09:00", (생성날짜)<br>
    "updated_at": "2020-09-30T23:36:21.456401+09:00", (수정날짜 --> 투표하기 하면 계속 최신화됩니다)<br>
    "voter_count": 0, (이 투표 컨텐츠에 투표한 명수)<br>
    "voted": true, (로그인자가 투표를 했는지 --> Header에 jwt를 보내면 내가 투표를 했었는지 알 수 있다)<br>
    "image": null (이 투표 컨텐츠의 사진)<br>
}

<hr>

### 특정 투표 컨텐츠 정보 수정하기 (PUT)
http://127.0.0.1:8000/voteboard/(voteboardid)

(이게 있어야 로그인자가 투표를 했는지 안했는지 알 수 있습니다)

❌ 제약조건 : 투표 게시글의 작성자만 수정 가능 (투표 게시글은 superuser만 생성 가능하기 때문에 결국 superuser야 한다)

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

**[Body]** --> form-data
- title : 제목 [필수는 아님]
- image : 이미지 [필수는 아님]

#### Response
{<br>
    "id": 1, (투표 컨텐츠 id)<br>
    "boardid": 1, (이 투표 컨텐츠를 포함하는 게시글 id)<br>
    "title": "자바", (제목)<br>
    "created_at": "2020-09-30T23:32:55.523007+09:00", (생성날짜)<br>
    "updated_at": "2020-09-30T23:36:21.456401+09:00", (수정날짜 --> 투표하기 하면 계속 최신화됩니다)<br>
    "voter_count": 0, (이 투표 컨텐츠에 투표한 명수)<br>
    "voted": true, (로그인자가 투표를 했는지 --> Header에 jwt를 보내면 내가 투표를 했었는지 알 수 있다)<br>
    "image": null (이 투표 컨텐츠의 사진)<br>
}

<hr>

### 특정 투표 컨텐츠 정보 수정하기 (DELETE)
http://127.0.0.1:8000/voteboard/(voteboardid)

(이게 있어야 로그인자가 투표를 했는지 안했는지 알 수 있습니다)

❌ 제약조건 : 투표 게시글의 작성자만 삭제 가능 (투표 게시글은 superuser만 생성 가능하기 때문에 결국 superuser야 한다)

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

#### Response
NONE

<hr>

### HOT한!! 투표 게시글 내용 가져오기 (GET)
http://localhost:8000/hotboard

**[헤더s]** --> form-data
- Authorization : jwt ~~~~~~~~~~~
(이게 있어야 로그인자가 투표를 했는지 안했는지 알 수 있습니다)

#### Response
{<br>
    "id": 1, (해당 게시글의 id)<br>
    "title": "가장 좋아하는 프로그래밍 언어", (제목)<br>
    "voter_count": 1, (총 몇명이 투표를 했는지)<br>
    "contents": [ (해당 게시글의 투표 컨텐츠들)<br>
        {<br>
            "id": 1, (투표 컨텐츠 id)<br>
            "boardid": 1, (이 투표 컨텐츠를 포함하는 게시글 id)<br>
            "title": "자바", (제목)<br>
            "created_at": "2020-09-30T23:32:55.523007+09:00", (생성날짜)<br>
            "updated_at": "2020-09-30T23:36:21.456401+09:00", (수정날짜 --> 투표하기 하면 계속 최신화됩니다)<br>
            "voter_count": 1, (이 투표 컨텐츠에 투표한 명수)<br>
            "voted": true, (로그인자가 투표를 했는지 --> Header에 jwt를 보내면 내가 투표를 했었는지 알 수 있다)<br>
            "image": null (이 투표 컨텐츠의 사진)<br>
        }<br>
    ],<br>
    "winner_id": [<br>
        1 (투표 컨텐츠의 투표수가 많은 것 --> 리스트로 감싼 이유는 동점도 있을 수 있기 때문에 설정)<br>
    ],<br>
    "ended": false, (끝난 투표 게시글인지 알기)<br>
    "voted": true, (내가 이 투표 게시글에 투표를 했는지 알기)<br>
    "created_at": "2020-09-30T23:30:29.209573+09:00", (투표 게시판이 만들어진 시간)<br>
    "updated_at": "2020-09-30T23:30:29.209573+09:00" (투표 게시판이 수정된 시간)<br>
}

<hr>

