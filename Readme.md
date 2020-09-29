<h1 align="center">EN;COD 👨‍💻</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
</p>

## 환경 구축
0. python -m venv myvenv (가상환경 생성)
1. python source myvenv/scripts/activate (가상환경 실행)
2. pip install -r requirements.txt
3. python manage.py makemigrations board
4. python manage.py migrate
5. python manage.py makemigrations account (한번에 makemigrations 안되는 버그)
6. python manage.py migrate
7. python manage.py createsuperuser
8. python manage.py runserver

## API 사용 방법
### 회원가입 (POST)
http://127.0.0.1:8000/rest-auth/registration/

#### Request
**[파라미터]** --> form-data
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
http://127.0.0.1:8000/rest-auth/login/
**[파라미터]** --> form-data
- username : 아이디
- password : 비밀번호

#### Response
{"token": "jwt ~~~~~~~~~~~~~"}

<hr>

### 글목록 가져오기 (GET)
http://localhost:8000/board/

#### Response
{
    "id": 게시글고유ID,
    "author": {
        "id": 사용자고유ID,
        "username": "아이디",
        "nickname": "닉네임"
    },
    "title": "제목",
    "body": "내용",
    "created_at": "생성시간",
    "updated_at": "수정시간"
} ...... 여러개

<hr>

### 글내용 가져오기 (GET)
http://localhost:8000/board/1/

#### Response
{
    "id": 게시글고유ID,
    "author": {
        "id": 사용자고유ID,
        "username": "아이디",
        "nickname": "닉네임"
    },
    "title": "제목",
    "body": "내용",
    "created_at": "생성시간",
    "updated_at": "수정시간"
} 

<hr>

### 글쓰기 (POST)
http://localhost:8000/board/
❌ 제약조건 : jwt 토큰으로 글 쓰기 가능

#### Request
**[해더s]**
Authorization : jwt ~~~~~~~~~~~

**[파라미터]** --> form-data
- username : 아이디
- password1 : 비밀번호
- password2 : 비밀번호 확인
- nickname : 닉네임

#### Response
{
    "id": 게시글고유ID,
    "author": {
        "id": 사용자고유ID,
        "username": "아이디",
        "nickname": "닉네임"
    },
    "title": "제목",
    "body": "내용",
    "created_at": "생성시간",
    "updated_at": "수정시간"
} 

<hr>

### 글삭제 (DELETE)
http://localhost:8000/board/1/
❌ 제약조건 : 작성자만이 삭제 가능

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

#### Response
NONE

<hr>

### 글수정 (PUT)
http://localhost:8000/board/1/
❌ 제약조건 : 작성자만이 수정 가능

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

**[파라미터]** --> form-data
- username : 아이디
- password1 : 비밀번호
- password2 : 비밀번호 확인
- nickname : 닉네임

#### Response
{
    "id": 게시글고유ID,
    "author": {
        "id": 사용자고유ID,
        "username": "아이디",
        "nickname": "닉네임"
    },
    "title": "제목",
    "body": "내용",
    "created_at": "생성시간",
    "updated_at": "수정시간"
} 

## 추가 기능
### 회원정보 수정 (PUT)
http://localhost:8000/accounts/user/
❌ 제약조건 : 로그인 한 사람만 접근 가능

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

**[파라미터]** --> form-data
- nickname : 닉네임

#### Response
{
    "username": "아이디",
    "email": "이메일",
    "nickname": "닉네임"
} 

<hr>

### 비밀번호 수정 (POST)
http://127.0.0.1:8000/rest-auth/password/change/
❌ 제약조건 : 로그인 한 사람만 접근 가능

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

**[파라미터]** --> form-data
- password1 : 비밀번호
- password2 : 비밀번호 확인

#### Response
{
    "detail": "New password has been saved."
}

<hr>

### 로그아웃 (POST)
http://127.0.0.1:8000/rest-auth/logout/

#### Request
**[해더s]**
- Authorization : jwt ~~~~~~~~~~~

#### Response
{
    "detail": "Successfully logged out."
}