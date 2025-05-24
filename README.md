# 설교 요약 API

이 API는 설교 원고나 영상 스크립트를 입력받아 Gemini AI를 사용하여 요약해주는 서비스입니다.

## 설치 방법

1. Pipenv 설치 (아직 설치하지 않은 경우):
```bash
pip install pipenv
```

2. 가상환경 생성 및 패키지 설치:
```bash
pipenv install
pipenv install --dev  # 테스트 패키지 설치
```

3. 가상환경 활성화:
```bash
pipenv shell
```

4. `.env` 파일 생성 및 Google API 키 설정:
```
GOOGLE_API_KEY=your_api_key_here
```

## 실행 방법

가상환경이 활성화된 상태에서:
```bash
uvicorn main:app --reload
```

서버가 실행되면 `http://localhost:8000`에서 API를 사용할 수 있습니다.

## 테스트 실행

가상환경이 활성화된 상태에서 프로젝트 루트 디렉토리에서:
```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일만 실행
pytest tests/test_main.py
pytest tests/test_summarizer.py

# 자세한 출력으로 테스트 실행
pytest -v

# 테스트 커버리지 확인
pytest --cov=.
```

## API 사용 방법

### 텍스트 요약하기

POST 요청을 `/summarize` 엔드포인트로 보내세요:

```bash
curl -X POST "http://localhost:8000/summarize" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@your_script.txt"
```

### API 문서 확인

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 개발 환경 관리

- 새로운 패키지 설치:
```bash
pipenv install 패키지명
```

- 개발용 패키지 설치:
```bash
pipenv install 패키지명 --dev
```

- 가상환경 종료:
```bash
exit
``` 