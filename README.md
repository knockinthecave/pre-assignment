# Pre-assignment Project

## 📝 프로젝트 개요
이 프로젝트는 **Django 기반 백엔드 서버**로, **MySQL과 MongoDB를 활용한 사용자 및 게시글 관리**를 수행합니다.  
JWT 인증을 활용하여 **사용자 인증 및 토큰 재발급**을 구현하였으며,  
**게시글 CRUD API**를 제공하고, **unittest 기반 테스트 코드**를 포함합니다.

---

## 📌 주요 기능
✅ **MySQL** – 사용자 정보 (`User`, `RefreshToken`) 저장  
✅ **MongoDB** – 게시글 데이터 관리  
✅ **JWT 인증** – 사용자 로그인, 토큰 발급 및 재발급  
✅ **게시글 CRUD API** – 게시글 생성, 조회, 수정, 삭제  
✅ **UnitTest 작성** – `unittest` 기반 API 테스트 코드 포함  
✅ **Docker 환경 구성** – `docker-compose`를 이용한 개발 환경 설정  

---

## 🚀 실행 방법

### **1️⃣ Docker 컨테이너 실행**
프로젝트 루트 디렉터리에서 아래 명령어 실행:
```bash
docker-compose up --build
```

### **2️⃣ Django 서버 접속 확인**
컨테이너가 정상적으로 실행되면 `http://0.0.0.0:8000` 또는 `http://localhost:8000` 에서 API를 확인할 수 있습니다.

### **3️⃣ DB 마이그레이션 (필요시 수동 실행)**
컨테이너 실행 시 자동으로 마이그레이션이 수행됩니다.  
추가적으로 수동으로 실행하려면:
```bash
docker-compose exec django python manage.py makemigrations
docker-compose exec django python manage.py migrate
```

---

## 📑 **API 명세**
### **회원가입**
- **URL**: `/users/signup`
- **Method**: `POST`
- **Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
- **Response (201 Created)**:
```json
{
  "id": 1,
  "email": "user@example.com"
}
```
- **Response (400 Bad Request)**:
```json
{
    "msg": "user@example.com은 이미 존재하는 이메일입니다."
}
```

### **로그인**
- **URL**: `/users/login`
- **Method**: `POST`
- **Request Body**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
- **Response (200 OK)**:
```json
{
  "access_token": "ACCESS_TOKEN",
  "refresh_token": "REFRESH_TOKEN"
}
```
- **Response (400 Bad Request)**:
```json
{
  "msg": "이메일과 비밀번호를 모두 입력해주세요."
}
```
- **Response (401 Unauthorized)**:
```json
{
  "msg": "비밀번호가 일치하지 않습니다."
}
```
```json
{
  "msg": "존재하지 않는 사용자입니다."
}
```
- **Response (500 Internal Server Error)**:
```json
{
  "msg": "서버 오류가 발생했습니다.",
  "errors": "error message"
}
```

### **토큰 갱신**
- **URL**: `/users/refresh`
- **Method**: `POST`
- **Request Body**:
```json
{
  "refresh_token": "REFRESH_TOKEN"
}
```
- **Response (200 OK)**:
```json
{
  "access_token": "ACCESS_TOKEN",
  "refresh_token": "REFRESH_TOKEN"
}
```
- **Response (400 Bad Request)**:
```json
{
  "msg": "토큰이 제공되지 않았습니다."
}
```
- **Response (401 Unauthorized)**:
```json
{
  "msg": "유효하지 않은 토큰입니다."
}
```
- **Response (400 Bad Request)**:
```json
{
  "msg": "유효하지 않은 데이터입니다.",
  "errors": {}
}
```
- **Response (500 Internal Server Error)**:
```json
{
  "msg": "서버 오류가 발생했습니다.",
  "errors": "error message"
}
```

### **로그아웃**
- **URL**: `/users/logout`
- **Method**: `POST`
- **Request Body**:
```json
{
  "refresh_token": "REFRESH_TOKEN"
}
```
- **Response (200 OK)**:
```json
{
  "msg": "로그아웃 되었습니다."
}
```
- **Response (400 Bad Request)**:
```json
{
  "msg": "토큰이 제공되지 않았습니다."
}
```
```json
{
  "msg": "유효하지 않은 데이터입니다.",
  "errors": {}
}
```
- **Response (401 Unauthorized)**:
```json
{
  "msg": "유효하지 않은 토큰입니다."
}
```
- **Response (500 Internal Server Error)**:
```json
{
  "msg": "서버 오류가 발생했습니다.",
  "errors": "error message"
}
```

### **게시글 생성**
- **URL**: `/posts`
- **Method**: `POST`
- **Headers**:
  - `Authorization: Bearer {ACCESS_TOKEN}`
- **Request Body**:
```json
{
  "title": "게시글 제목",
  "content": "게시글 내용"
}
```
- **Response (201 Created)**:
```json
{
  "id": "게시글 ID",
  "title": "게시글 제목",
  "content": "게시글 내용",
  "author_id": "작성자 ID",
  "created_at": "작성일시"
}
```
- **Response (400 Bad Request)**:
```json
{
  "msg": "제목과 내용을 모두 입력해주세요."
}
```
```json
{
  "msg": "유효하지 않은 데이터입니다."
}
```
- **Response (401 Unauthorized)**:
```json
{
  "msg": "유효하지 않은 토큰입니다."
}
```
- **Response (500 Internal Server Error)**:
```json
{
  "msg": "서버 오류가 발생했습니다."
}
```

### **게시글 조회**
- **URL**: `/posts`
- **Method**: `POST`
- **Parameters**: `page`, `page_size` OR `author_id`
- **Response (200 OK)**:
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```
- **Response (400 Bad Request)**:
```json
{
  "msg": "유효하지 않은 데이터입니다.",
  "errors": {}
}
```
- **Response (500 Internal Sercer Error)**:
```json
{
  "msg": "서버 오류가 발생했습니다."
}
```

### **게시글 상세 조회**
- **URL**: `/posts/<post_id>`
- **Method**: `POST`
- **Response (200 OK)**:
```json
{
  "id": "게시글 ID",
  "title": "게시글 제목",
  "content": "게시글 내용",
  "author_id": "작성자 ID",
  "created_at": "작성일시"
}
```
- **Response (404 Not Found)**:
```json
{
  "msg": "존재하지 않는 게시글입니다."
}
```
- **Response (400 Bad Request)**:
```json
{
  "msg": "유효하지 않은 데이터입니다.",
  "errors": {}
}
```
- **Response (500 Internal Server Error)**:
```json
{
  "msg": "서버 오류가 발생했습니다.",
  "errors": "error message"
}
```

### **게시글 수정**
- **URL**: `/posts/<post_id>`
- **Method**: `PUT`
- **Headers**:
  - `Authorization: Bearer {ACCESS_TOKEN}`
- **Request Body**:
```json
{
  "title": "수정된 제목",
  "content": "수정된 내용"
}
```
- **Response (200 OK)**:
```json
{
  "id": "게시글 ID",
  "title": "수정된 제목",
  "content": "수정된 내용",
  "author_id": "작성자 ID",
  "created_at": "작성일시"
}
```
- **Response (400 Bad Request)**:
```json
{
  "msg": "유효하지 않은 데이터입니다.",
  "errors": {}
}
```
- **Response (401 Unauthorized)**:
```json
{
  "msg": "유효하지 않은 토큰입니다."
}
```
- **Response (404 Not Found)**:
```json
{
  "msg": "존재하지 않는 게시글입니다."
}
```
- **Response (500 Internal Server Error)**:
```json
{
  "msg": "서버 오류가 발생했습니다.",
  "errors": "error message"
}
```

### **게시글 삭제**
- **URL**: `/posts/<post_id>`
- **Method**: `DELETE`
- **Headers**:
  - `Authorization: Bearer {ACCESS_TOKEN}`
- **Response (204 No Content)**:
- **Response (400 Bad Request)**:
```json
{
  "msg": "유효하지 않은 데이터입니다.",
  "errors": {}
}
```
- **Response (401 Unauthorized)**:
```json
{
  "msg": "유효하지 않은 토큰입니다."
}
```
- **Response (404 Not Found)**:
```json
{
  "msg": "존재하지 않는 게시글입니다."
}
```
- **Response (500 Internal Server Error)**:
```json
{
  "msg": "서버 오류가 발생했습니다.",
  "errors": "error message"
}
```
---

## 🛠 **개발 환경**
- **Backend**: Django 4.2.16, Django REST Framework
- **Database**: MySQL 8.0, MongoDB 8.0
- **Auth**: JWT (SimpleJWT)
- **Docker**: `docker-compose` 기반 컨테이너 관리
- **Testing**: `unittest` 기반 API 테스트 작성

---

## 🧪 **UnitTest 실행 방법**
컨테이너 내에서 테스트 실행:
```bash
docker-compose exec django python manage.py test
```
또는 로컬에서 실행:
```bash
python manage.py test
```

---

## 📜 **디렉터리 구조**
```plaintext
backend/
│── api/
│   ├── users/
│   │   ├── models.py       # User, RefreshToken 모델 정의 (MySQL)
│   │   ├── views.py        # 회원가입, 로그인 API
│   │   ├── serializers.py  # UserSerializer
│   ├── posts/
│   │   ├── documents.py    # Post 모델 정의 (MongoDB)
│   │   ├── views.py        # 게시글 CRUD API
│── config/
│   ├── settings.py         # DB, JWT, REST 설정
│   ├── urls.py             # URL 라우팅 설정
│── manage.py               # Django 실행 파일
│── Dockerfile              # Django 컨테이너 설정
│── docker-compose.yml      # MySQL, MongoDB, Django 컨테이너 구성
│── requirements.txt        # 필요한 패키지 목록
```

---

## 🛑 **에러 해결**
### **`ModuleNotFoundError: No module named 'backend.settings'`**
👉 **해결:** `DJANGO_SETTINGS_MODULE`을 명시적으로 설정하고 실행  
```bash
export DJANGO_SETTINGS_MODULE=backend.settings
python manage.py runserver
```