# Python 이미지 선택
FROM python:3.10

# 작업 디렉터리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 기본 명령어 설정 (CMD는 `docker-compose.yml`에서 실행됨)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
