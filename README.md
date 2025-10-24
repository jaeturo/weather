# 🌤️ 날씨 웹앱

Streamlit과 OpenWeather API를 사용한 실시간 날씨 정보 웹 애플리케이션입니다.

## ✨ 주요 기능

- 🌍 전 세계 도시의 실시간 날씨 정보 조회
- 🌡️ 현재 온도, 체감온도, 습도, 기압, 풍속 정보
- 🌅 일출/일몰 시간 표시
- 🌦️ 날씨 상태 표시
- 🏙️ 인기 도시 빠른 검색 버튼

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. API 키 설정
OpenWeather API 키를 설정해야 합니다. 다음 방법 중 하나를 선택하세요:

#### 방법 1: 환경변수 사용 (권장)
```bash
# Windows (PowerShell)
$env:OPENWEATHER_API_KEY="your_api_key_here"

# Windows (Command Prompt)
set OPENWEATHER_API_KEY=your_api_key_here

# Linux/Mac
export OPENWEATHER_API_KEY="your_api_key_here"
```

#### 방법 2: config.py 파일 사용
`config.py` 파일에서 `OPENWEATHER_API_KEY` 값을 수정하세요.

### 3. API 키 발급
1. [OpenWeather API](https://openweathermap.org/api)에 가입
2. 무료 API 키 발급
3. 위의 방법으로 API 키 설정

### 4. 애플리케이션 실행
```bash
streamlit run weather_app.py
```

### 5. 브라우저에서 확인
애플리케이션이 실행되면 자동으로 브라우저가 열리며, `http://localhost:8501`에서 확인할 수 있습니다.

## 📋 사용법

1. 왼쪽 사이드바에서 도시 이름을 입력하세요
2. "날씨 검색" 버튼을 클릭하세요
3. 실시간 날씨 정보를 확인하세요
4. 인기 도시 버튼을 클릭하여 빠르게 검색할 수도 있습니다

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **API**: OpenWeather API
- **Language**: Python 3.7+
- **Dependencies**: streamlit, requests

## 📁 프로젝트 구조

```
weather/
├── weather_app.py      # 메인 Streamlit 애플리케이션
├── config.py          # API 설정 파일 (Git에 업로드하지 마세요)
├── requirements.txt    # Python 의존성 목록
├── .gitignore         # Git 무시 파일 목록
└── README.md          # 프로젝트 설명서
```

## 🔒 보안 주의사항

- **API 키 보안**: `config.py` 파일은 Git에 업로드하지 마세요
- **환경변수 사용**: 프로덕션 환경에서는 환경변수를 사용하여 API 키를 관리하세요
- **.gitignore**: 민감한 정보가 포함된 파일들이 Git에 업로드되지 않도록 `.gitignore` 파일을 확인하세요

## 🌐 API 정보

이 애플리케이션은 [OpenWeather API](https://openweathermap.org/api)를 사용합니다.
- 현재 날씨 데이터 API 사용
- 섭씨 온도 단위
- 한국어 응답 지원
