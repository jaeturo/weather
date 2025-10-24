# 🔒 GitHub 업로드 전 보안 체크리스트

## ✅ API 키 보안 확인

### 1. 하드코딩된 API 키 제거 확인
- [ ] `weather_app.py`에 API 키가 하드코딩되지 않았는지 확인
- [ ] `config.py`에 API 키가 하드코딩되지 않았는지 확인
- [ ] 다른 Python 파일에 API 키가 하드코딩되지 않았는지 확인

### 2. .gitignore 파일 확인
- [ ] `config.py`가 .gitignore에 포함되어 있는지 확인
- [ ] `secrets.toml`이 .gitignore에 포함되어 있는지 확인
- [ ] `.streamlit/secrets.toml`이 .gitignore에 포함되어 있는지 확인
- [ ] `.env` 파일들이 .gitignore에 포함되어 있는지 확인

### 3. 민감한 정보 검색
다음 명령어로 프로젝트에서 API 키를 검색해보세요:
```bash
# API 키 패턴 검색 (실제 키의 일부를 사용)
grep -r "907e5cf5" .
grep -r "OPENWEATHER_API_KEY.*=" .
grep -r "api.*key" . -i
```

## 🚀 GitHub 업로드 방법

### 1. Git 상태 확인
```bash
# 현재 Git 상태 확인
git status

# 추가될 파일들 확인
git add -n .
```

### 2. 안전한 업로드
```bash
# 파일 추가 (민감한 파일은 자동으로 제외됨)
git add .

# 커밋
git commit -m "Add weather app with secure API key management"

# GitHub에 푸시
git push origin main
```

### 3. 업로드 후 확인
- [ ] GitHub 저장소에서 민감한 파일이 업로드되지 않았는지 확인
- [ ] API 키가 코드에 노출되지 않았는지 확인

## 🔧 Streamlit 클라우드 배포

### 1. 환경변수 설정
Streamlit 클라우드에서:
1. 앱 설정 → "Secrets" 탭
2. TOML 형식으로 입력:
```toml
OPENWEATHER_API_KEY = "your_actual_api_key_here"
```

### 2. 배포 확인
- [ ] 앱이 정상적으로 실행되는지 확인
- [ ] 날씨 데이터가 올바르게 표시되는지 확인
- [ ] API 키 오류가 발생하지 않는지 확인

## ⚠️ 보안 주의사항

### ❌ 절대 하지 말아야 할 것들
- API 키를 코드에 직접 포함
- 민감한 정보를 커밋 메시지에 포함
- API 키를 공개 채팅이나 이메일에 전송
- API 키를 스크린샷에 포함

### ✅ 반드시 해야 할 것들
- 환경변수나 secrets 사용
- 정기적인 API 키 갱신
- API 사용량 모니터링
- .gitignore 파일 유지

## 🆘 문제 발생 시 대처법

### API 키가 실수로 업로드된 경우
1. 즉시 GitHub에서 해당 커밋 삭제
2. API 키 재발급
3. Git 히스토리 정리 (필요시)

### API 키가 노출된 경우
1. 즉시 API 키 비활성화
2. 새로운 API 키 발급
3. 모든 환경에서 새 키로 교체
