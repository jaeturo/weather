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
├── weather_app.py                    # 메인 Streamlit 애플리케이션
├── config.py                        # API 설정 파일 (Git에 업로드하지 마세요)
├── requirements.txt                  # Python 의존성 목록
├── .gitignore                       # Git 무시 파일 목록
├── README.md                        # 프로젝트 설명서
├── SECURITY_CHECKLIST.md            # 보안 체크리스트
├── .streamlit/
│   ├── config.toml                  # Streamlit 설정 파일
│   └── secrets.toml                 # 로컬 개발용 secrets 파일
├── streamlit_secrets_template.toml  # Streamlit 클라우드용 secrets 템플릿
└── images/                          # 날씨 이미지 폴더
    ├── rain.jpg
    ├── snow.jpg
    ├── sun.jpg
    └── cloud.jpg
```

## 🚀 Streamlit 클라우드 배포

### 1. GitHub에 코드 업로드
```bash
git add .
git commit -m "Add weather app"
git push origin main
```

### 2. Streamlit 클라우드에서 배포
1. [Streamlit Cloud](https://share.streamlit.io/)에 접속
2. "New app" 클릭
3. GitHub 저장소 연결
4. 메인 파일 경로: `weather_app.py`
5. "Deploy!" 클릭

### 3. 환경변수 설정 (필수)
Streamlit 클라우드에서 환경변수를 설정해야 합니다:

#### 방법 1: Streamlit 클라우드 Secrets 탭 사용
1. 앱 설정 → "Secrets" 탭
2. `OPENWEATHER_API_KEY` 추가
3. API 키 값 입력

#### 방법 2: TOML 파일 사용 (권장)
1. **로컬 개발 시**: `.streamlit/secrets.toml` 파일에서 API 키 설정
2. **Streamlit 클라우드 배포 시**: 
   - `streamlit_secrets_template.toml` 파일을 참고
   - "Secrets" 탭에 TOML 형식으로 입력:
   ```toml
   OPENWEATHER_API_KEY = "your_api_key_here"
   ```

### 4. API 키 발급 및 설정
1. [OpenWeather API](https://openweathermap.org/api)에 가입
2. 무료 API 키 발급
3. 위의 방법으로 API 키 설정

**중요**: API 키는 반드시 환경변수로 설정해야 합니다. 코드에 직접 포함하면 보안에 문제가 됩니다.

## 🔒 보안 주의사항

- **API 키 보안**: 
  - ❌ **절대 코드에 API 키를 직접 포함하지 마세요**
  - ✅ **반드시 환경변수를 사용하여 API 키를 관리하세요**
  - ✅ **Git에 API 키가 포함된 파일을 업로드하지 마세요**
- **.gitignore**: 민감한 정보가 포함된 파일들이 Git에 업로드되지 않도록 `.gitignore` 파일을 확인하세요
- **API 키 관리**: 
  - 정기적으로 API 키를 갱신하세요
  - 사용하지 않는 API 키는 비활성화하세요
  - API 키 사용량을 모니터링하세요

## 🌐 API 정보

이 애플리케이션은 [OpenWeather API](https://openweathermap.org/api)를 사용합니다.
- 현재 날씨 데이터 API 사용
- 섭씨 온도 단위
- 한국어 응답 지원
