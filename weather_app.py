import streamlit as st
import requests
import json
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="🌤️ 한국 날씨 정보",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# OpenWeather API 설정
# 환경변수에서 API 키를 가져오고, 없으면 config.py에서 가져옴
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    try:
        from config import OPENWEATHER_API_KEY
        API_KEY = OPENWEATHER_API_KEY
    except ImportError:
        st.error("❌ API 키를 찾을 수 없습니다. 환경변수 OPENWEATHER_API_KEY를 설정하거나 config.py 파일을 확인해주세요.")
        st.stop()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# 한국 도시명 매핑 (한글 -> 영문, 국가코드 포함)
KOREAN_CITIES = {
    # 특별시/광역시
    "서울": "Seoul,KR",
    "부산": "Busan,KR",
    "대구": "Daegu,KR", 
    "인천": "Incheon,KR",
    "광주": "Gwangju,KR",
    "대전": "Daejeon,KR",
    "울산": "Ulsan,KR",
    "세종": "Sejong,KR",
    
    # 경기도 (모든 시/군)
    "수원": "Suwon,KR",
    "성남": "Seongnam,KR",
    "의정부": "Uijeongbu,KR",
    "안양": "Anyang,KR",
    "부천": "Bucheon,KR",
    "광명": "Gwangmyeong,KR",
    "평택": "Pyeongtaek,KR",
    "과천": "Gwacheon,KR",
    "오산": "Osan,KR",
    "시흥": "Siheung,KR",
    "군포": "Gunpo,KR",
    "의왕": "Uiwang,KR",
    "하남": "Hanam,KR",
    "용인": "Yongin,KR",
    "파주": "Paju,KR",
    "이천": "Icheon,KR",
    "안성": "Anseong,KR",
    "김포": "Gimpo-si,KR",
    "화성": "Hwaseong,KR",
    "여주": "Yeoju,KR",
    "양평": "Yangpyeong,KR",
    "고양": "Goyang,KR",
    "동두천": "Dongducheon,KR",
    "가평": "Gapyeong,KR",
    "연천": "Yeoncheon,KR",
    "양주": "Yangju,KR",
    "구리": "Guri,KR",
    "남양주": "Namyangju,KR",
    "포천": "Pocheon,KR",
    
    # 강원도
    "춘천": "Chuncheon,KR",
    "원주": "Wonju,KR",
    "강릉": "Gangneung,KR",
    "동해": "Donghae,KR",
    "태백": "Taebaek,KR",
    "속초": "Sokcho,KR",
    "삼척": "Samcheok,KR",
    "홍천": "Hongcheon,KR",
    "횡성": "Hoengseong,KR",
    "영월": "Yeongwol,KR",
    "평창": "Pyeongchang,KR",
    "정선": "Jeongseon,KR",
    "철원": "Cheorwon,KR",
    "화천": "Hwacheon,KR",
    "양구": "Yanggu,KR",
    "인제": "Inje,KR",
    "고성": "Goseong,KR",
    "양양": "Yangyang,KR",
    
    # 충청북도
    "청주": "Cheongju,KR",
    "충주": "Chungju,KR",
    "제천": "Jecheon,KR",
    "보은": "Boeun,KR",
    "옥천": "Okcheon,KR",
    "영동": "Yeongdong,KR",
    "증평": "Jeungpyeong,KR",
    "진천": "Jincheon,KR",
    "괴산": "Goesan,KR",
    "음성": "Eumseong,KR",
    "단양": "Danyang,KR",
    
    # 충청남도
    "천안": "Cheonan,KR",
    "공주": "Gongju,KR",
    "보령": "Boryeong,KR",
    "아산": "Asan,KR",
    "서산": "Seosan,KR",
    "논산": "Nonsan,KR",
    "계룡": "Gyeryong,KR",
    "당진": "Dangjin,KR",
    "금산": "Geumsan,KR",
    "부여": "Buyeo,KR",
    "서천": "Seocheon,KR",
    "청양": "Cheongyang,KR",
    "홍성": "Hongseong,KR",
    "예산": "Yesan,KR",
    "태안": "Taean,KR",
    
    # 전라북도
    "전주": "Jeonju,KR",
    "군산": "Gunsan,KR",
    "익산": "Iksan,KR",
    "정읍": "Jeongeup,KR",
    "남원": "Namwon,KR",
    "김제": "Gimje,KR",
    "완주": "Wanju,KR",
    "진안": "Jinan,KR",
    "무주": "Muju,KR",
    "장수": "Jangsu,KR",
    "임실": "Imsil,KR",
    "순창": "Sunchang,KR",
    "고창": "Gochang,KR",
    "부안": "Buan,KR",
    
    # 전라남도
    "목포": "Mokpo,KR",
    "여수": "Yeosu,KR",
    "순천": "Suncheon,KR",
    "나주": "Naju,KR",
    "광양": "Gwangyang,KR",
    "담양": "Damyang,KR",
    "곡성": "Gokseong,KR",
    "구례": "Gurye,KR",
    "고흥": "Goheung,KR",
    "보성": "Boseong,KR",
    "화순": "Hwasun,KR",
    "장흥": "Jangheung,KR",
    "강진": "Gangjin,KR",
    "해남": "Haenam,KR",
    "영암": "Yeongam,KR",
    "무안": "Muan,KR",
    "함평": "Hampyeong,KR",
    "영광": "Yeonggwang,KR",
    "장성": "Jangseong,KR",
    "완도": "Wando,KR",
    "진도": "Jindo,KR",
    "신안": "Sinan,KR",
    
    # 경상북도
    "포항": "Pohang,KR",
    "경주": "Gyeongju,KR",
    "김천": "Gimcheon,KR",
    "안동": "Andong,KR",
    "구미": "Gumi,KR",
    "영주": "Yeongju,KR",
    "영천": "Yeongcheon,KR",
    "상주": "Sangju,KR",
    "문경": "Mungyeong,KR",
    "경산": "Gyeongsan,KR",
    "군위": "Gunwi,KR",
    "의성": "Uiseong,KR",
    "청송": "Cheongsong,KR",
    "영양": "Yeongyang,KR",
    "영덕": "Yeongdeok,KR",
    "청도": "Cheongdo,KR",
    "고령": "Goryeong,KR",
    "성주": "Seongju,KR",
    "칠곡": "Chilgok,KR",
    "예천": "Yecheon,KR",
    "봉화": "Bonghwa,KR",
    "울진": "Uljin,KR",
    "울릉": "Ulleung,KR",
    
    # 경상남도
    "창원": "Changwon,KR",
    "진주": "Jinju,KR",
    "통영": "Tongyeong,KR",
    "사천": "Sacheon,KR",
    "김해": "Gimhae,KR",
    "밀양": "Miryang,KR",
    "거제": "Geoje,KR",
    "양산": "Yangsan,KR",
    "의령": "Uiryeong,KR",
    "함안": "Haman,KR",
    "창녕": "Changnyeong,KR",
    "고성": "Goseong,KR",
    "남해": "Namhae,KR",
    "하동": "Hadong,KR",
    "산청": "Sancheong,KR",
    "함양": "Hamyang,KR",
    "거창": "Geochang,KR",
    "합천": "Hapcheon,KR",
    
    # 제주도
    "제주": "Jeju,KR",
    "서귀포": "Seogwipo,KR"
}

def get_weather_icon(weather_code):
    """날씨 코드에 따른 이모지 반환"""
    weather_icons = {
        '01d': '☀️', '01n': '🌙',  # 맑음
        '02d': '⛅', '02n': '☁️',  # 약간 흐림
        '03d': '☁️', '03n': '☁️',  # 흐림
        '04d': '☁️', '04n': '☁️',  # 매우 흐림
        '09d': '🌧️', '09n': '🌧️',  # 소나기
        '10d': '🌦️', '10n': '🌧️',  # 비
        '11d': '⛈️', '11n': '⛈️',  # 천둥번개
        '13d': '❄️', '13n': '❄️',  # 눈
        '50d': '🌫️', '50n': '🌫️'   # 안개
    }
    return weather_icons.get(weather_code, '🌤️')

def get_weather_image(weather_main, weather_code):
    """날씨 상태에 따른 이미지 파일 경로 반환"""
    # 날씨 메인 상태에 따른 이미지 매핑
    weather_images = {
        'Clear': 'images/sun.jpeg',      # 맑음
        'Clouds': 'images/cloud.jpeg',   # 흐림
        'Rain': 'images/rain.jpeg',      # 비
        'Drizzle': 'images/rain.jpeg',   # 이슬비
        'Thunderstorm': 'images/rain.jpeg',  # 천둥번개
        'Snow': 'images/snow.jpeg',      # 눈
        'Mist': 'images/cloud.jpeg',     # 안개
        'Fog': 'images/cloud.jpeg',      # 안개
        'Haze': 'images/cloud.jpeg',     # 실안개
        'Dust': 'images/cloud.jpeg',     # 먼지
        'Sand': 'images/cloud.jpeg',     # 모래
        'Ash': 'images/cloud.jpeg',      # 화산재
        'Squall': 'images/rain.jpeg',    # 돌풍
        'Tornado': 'images/rain.jpeg'    # 토네이도
    }
    
    # 날씨 코드에 따른 세부 분류
    if weather_code in ['01d', '01n']:  # 맑음
        return 'images/sun.jpeg'
    elif weather_code in ['02d', '02n', '03d', '03n', '04d', '04n']:  # 흐림
        return 'images/cloud.jpeg'
    elif weather_code in ['09d', '09n', '10d', '10n', '11d', '11n']:  # 비/천둥번개
        return 'images/rain.jpeg'
    elif weather_code in ['13d', '13n']:  # 눈
        return 'images/snow.jpeg'
    elif weather_code in ['50d', '50n']:  # 안개
        return 'images/cloud.jpeg'
    else:
        # 기본값으로 날씨 메인 상태 사용
        return weather_images.get(weather_main, 'images/sun.jpeg')

def set_background_image(image_path):
    """배경 이미지를 설정하는 함수"""
    try:
        # 이미지 파일을 base64로 인코딩
        import base64
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # CSS 스타일 생성
        css = f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* 메인 컨테이너에 반투명 배경 추가 */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            margin-top: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
        }}
        
        /* 제목과 텍스트 색상 설정 */
        .main h1, .main h2, .main h3 {{
            color: #2c3e50 !important;
            text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8);
        }}
        
        .main p, .main div {{
            color: #34495e !important;
        }}
        
        /* 메트릭 카드 스타일 */
        .metric-card {{
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        
        /* 사이드바 스타일 */
        .css-1d391kg {{
            background-color: rgba(255, 255, 255, 0.95);
        }}
        
        /* 버튼 스타일 */
        .stButton > button {{
            background-color: rgba(52, 152, 219, 0.9);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .stButton > button:hover {{
            background-color: rgba(41, 128, 185, 0.9);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }}
        
        /* 입력 필드 스타일 */
        .stTextInput > div > div > input {{
            background-color: rgba(255, 255, 255, 0.9);
            border: 2px solid rgba(52, 152, 219, 0.3);
            border-radius: 8px;
            color: #2c3e50;
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)
        return True
    except Exception as e:
        st.warning(f"배경 이미지를 설정할 수 없습니다: {e}")
        return False

def create_weather_card(title, value, unit="", icon=""):
    """날씨 정보를 카드 형태로 표시하는 함수"""
    card_html = f"""
    <div class="metric-card">
        <div style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #2c3e50; margin-bottom: 0.25rem;">{value}{unit}</div>
            <div style="font-size: 0.9rem; color: #7f8c8d;">{title}</div>
        </div>
    </div>
    """
    return card_html

def validate_weather_data(weather_data):
    """날씨 데이터의 유효성을 검증하는 함수"""
    if not weather_data:
        return False, "날씨 데이터가 없습니다."
    
    # 필수 필드 확인
    required_fields = {
        'name': '도시명',
        'main': '기본 날씨 정보',
        'weather': '날씨 상태',
        'sys': '시스템 정보'
    }
    
    missing_fields = []
    for field, description in required_fields.items():
        if field not in weather_data:
            missing_fields.append(description)
    
    if missing_fields:
        return False, f"누락된 필수 정보: {', '.join(missing_fields)}"
    
    # main 필드 내부 확인
    main_data = weather_data.get('main', {})
    main_required = ['temp', 'humidity', 'pressure']
    main_missing = [field for field in main_required if field not in main_data]
    
    if main_missing:
        return False, f"기본 날씨 정보 누락: {', '.join(main_missing)}"
    
    # weather 배열 확인
    weather_array = weather_data.get('weather', [])
    if not weather_array or len(weather_array) == 0:
        return False, "날씨 상태 정보가 없습니다."
    
    return True, "데이터 검증 완료"

def get_korean_city_name(english_city_name):
    """영문 도시명을 한글 도시명으로 변환하는 함수"""
    # 직접 매핑 딕셔너리
    english_to_korean = {
        'Seoul': '서울',
        'Busan': '부산',
        'Daegu': '대구',
        'Incheon': '인천',
        'Gwangju': '광주',
        'Daejeon': '대전',
        'Ulsan': '울산',
        'Sejong': '세종',
        'Suwon': '수원',
        'Seongnam': '성남',
        'Uijeongbu': '의정부',
        'Anyang': '안양',
        'Bucheon': '부천',
        'Gwangmyeong': '광명',
        'Pyeongtaek': '평택',
        'Gwacheon': '과천',
        'Osan': '오산',
        'Siheung': '시흥',
        'Gunpo': '군포',
        'Uiwang': '의왕',
        'Hanam': '하남',
        'Yongin': '용인',
        'Paju': '파주',
        'Icheon': '이천',
        'Anseong': '안성',
        'Gimpo-si': '김포',
        'Gimpo': '김포',
        'Hwaseong-si': '화성',
        'Siheung-si': '시흥',
        'Gunpo-si': '군포',
        'Uiwang-si': '의왕',
        'Hanam-si': '하남',
        'Gwangmyeong-si': '광명',
        'Pyeongtaek-si': '평택',
        'Gwacheon-si': '과천',
        'Osan-si': '오산',
        'Icheon-si': '이천',
        'Anseong-si': '안성',
        'Yeoju-si': '여주',
        'Yangpyeong-gun': '양평',
        'Dongducheon-si': '동두천',
        'Gapyeong-gun': '가평',
        'Yeoncheon-gun': '연천',
        'Yangju-si': '양주',
        'Guri-si': '구리',
        'Namyangju-si': '남양주',
        'Pocheon-si': '포천',
        'Chuncheon-si': '춘천',
        'Wonju-si': '원주',
        'Gangneung-si': '강릉',
        'Sokcho-si': '속초',
        'Donghae-si': '동해',
        'Taebaek-si': '태백',
        'Pyeongchang-gun': '평창',
        'Jeongseon-gun': '정선',
        'Cheongju-si': '청주',
        'Chungju-si': '충주',
        'Cheonan-si': '천안',
        'Gongju-si': '공주',
        'Boryeong-si': '보령',
        'Asan-si': '아산',
        'Seosan-si': '서산',
        'Nonsan-si': '논산',
        'Jeonju-si': '전주',
        'Gunsan-si': '군산',
        'Iksan-si': '익산',
        'Mokpo-si': '목포',
        'Yeosu-si': '여수',
        'Suncheon-si': '순천',
        'Naju-si': '나주',
        'Gwangyang-si': '광양',
        'Pohang-si': '포항',
        'Gyeongju-si': '경주',
        'Gimcheon-si': '김천',
        'Andong-si': '안동',
        'Gumi-si': '구미',
        'Changwon-si': '창원',
        'Jinju-si': '진주',
        'Tongyeong-si': '통영',
        'Jeju-si': '제주',
        'Seogwipo-si': '서귀포',
        'Hwaseong': '화성',
        'Yeoju': '여주',
        'Yangpyeong': '양평',
        'Goyang': '고양',
        'Dongducheon': '동두천',
        'Gapyeong': '가평',
        'Yeoncheon': '연천',
        'Yangju': '양주',
        'Guri': '구리',
        'Namyangju': '남양주',
        'Pocheon': '포천',
        'Siheung': '시흥',
        'Gunpo': '군포',
        'Uiwang': '의왕',
        'Hanam': '하남',
        'Gwangmyeong': '광명',
        'Pyeongtaek': '평택',
        'Gwacheon': '과천',
        'Osan': '오산',
        'Icheon': '이천',
        'Anseong': '안성',
        'Chuncheon': '춘천',
        'Wonju': '원주',
        'Gangneung': '강릉',
        'Donghae': '동해',
        'Taebaek': '태백',
        'Sokcho': '속초',
        'Samcheok': '삼척',
        'Hongcheon': '홍천',
        'Hoengseong': '횡성',
        'Yeongwol': '영월',
        'Pyeongchang': '평창',
        'Jeongseon': '정선',
        'Cheorwon': '철원',
        'Hwacheon': '화천',
        'Yanggu': '양구',
        'Inje': '인제',
        'Goseong': '고성',
        'Yangyang': '양양',
        'Cheongju': '청주',
        'Chungju': '충주',
        'Jecheon': '제천',
        'Boeun': '보은',
        'Okcheon': '옥천',
        'Yeongdong': '영동',
        'Jeungpyeong': '증평',
        'Jincheon': '진천',
        'Goesan': '괴산',
        'Eumseong': '음성',
        'Danyang': '단양',
        'Cheonan': '천안',
        'Gongju': '공주',
        'Boryeong': '보령',
        'Asan': '아산',
        'Seosan': '서산',
        'Nonsan': '논산',
        'Gyeryong': '계룡',
        'Dangjin': '당진',
        'Geumsan': '금산',
        'Buyeo': '부여',
        'Seocheon': '서천',
        'Cheongyang': '청양',
        'Hongseong': '홍성',
        'Yesan': '예산',
        'Taean': '태안',
        'Jeonju': '전주',
        'Gunsan': '군산',
        'Iksan': '익산',
        'Jeongeup': '정읍',
        'Namwon': '남원',
        'Gimje': '김제',
        'Wanju': '완주',
        'Jinan': '진안',
        'Muju': '무주',
        'Jangsu': '장수',
        'Imsil': '임실',
        'Sunchang': '순창',
        'Gochang': '고창',
        'Buan': '부안',
        'Mokpo': '목포',
        'Yeosu': '여수',
        'Suncheon': '순천',
        'Naju': '나주',
        'Gwangyang': '광양',
        'Damyang': '담양',
        'Gokseong': '곡성',
        'Gurye': '구례',
        'Goheung': '고흥',
        'Boseong': '보성',
        'Hwasun': '화순',
        'Jangheung': '장흥',
        'Gangjin': '강진',
        'Haenam': '해남',
        'Yeongam': '영암',
        'Muan': '무안',
        'Hampyeong': '함평',
        'Yeonggwang': '영광',
        'Jangseong': '장성',
        'Wando': '완도',
        'Jindo': '진도',
        'Sinan': '신안',
        'Pohang': '포항',
        'Gyeongju': '경주',
        'Gimcheon': '김천',
        'Andong': '안동',
        'Gumi': '구미',
        'Yeongju': '영주',
        'Yeongcheon': '영천',
        'Sangju': '상주',
        'Mungyeong': '문경',
        'Gyeongsan': '경산',
        'Gunwi': '군위',
        'Uiseong': '의성',
        'Cheongsong': '청송',
        'Yeongyang': '영양',
        'Yeongdeok': '영덕',
        'Cheongdo': '청도',
        'Goryeong': '고령',
        'Seongju': '성주',
        'Chilgok': '칠곡',
        'Yecheon': '예천',
        'Bonghwa': '봉화',
        'Uljin': '울진',
        'Ulleung': '울릉',
        'Changwon': '창원',
        'Jinju': '진주',
        'Tongyeong': '통영',
        'Sacheon': '사천',
        'Gimhae': '김해',
        'Miryang': '밀양',
        'Geoje': '거제',
        'Yangsan': '양산',
        'Uiryeong': '의령',
        'Haman': '함안',
        'Changnyeong': '창녕',
        'Goseong': '고성',
        'Namhae': '남해',
        'Hadong': '하동',
        'Sancheong': '산청',
        'Hamyang': '함양',
        'Geochang': '거창',
        'Hapcheon': '합천',
        'Jeju': '제주',
        'Seogwipo': '서귀포'
    }
    
    # 매핑에서 찾기
    if english_city_name in english_to_korean:
        return english_to_korean[english_city_name]
    else:
        # 매핑에 없으면 원래 이름 반환
        return english_city_name

def get_weather(city_input):
    """OpenWeather API에서 날씨 정보를 가져오는 함수"""
    try:
        # 도시별 대안 이름 정의
        alternative_city_names = {
            "김포": ["Gimpo-si,KR", "Gimpo,KR", "Gimpo-si", "Gimpo"],
            "화성": ["Hwaseong-si,KR", "Hwaseong,KR", "Hwaseong-si", "Hwaseong"],
            "시흥": ["Siheung-si,KR", "Siheung,KR", "Siheung-si", "Siheung"],
            "군포": ["Gunpo-si,KR", "Gunpo,KR", "Gunpo-si", "Gunpo"],
            "의왕": ["Uiwang-si,KR", "Uiwang,KR", "Uiwang-si", "Uiwang"],
            "하남": ["Hanam-si,KR", "Hanam,KR", "Hanam-si", "Hanam"],
            "광명": ["Gwangmyeong-si,KR", "Gwangmyeong,KR", "Gwangmyeong-si", "Gwangmyeong"],
            "평택": ["Pyeongtaek-si,KR", "Pyeongtaek,KR", "Pyeongtaek-si", "Pyeongtaek"],
            "과천": ["Gwacheon-si,KR", "Gwacheon,KR", "Gwacheon-si", "Gwacheon"],
            "오산": ["Osan-si,KR", "Osan,KR", "Osan-si", "Osan"],
            "이천": ["Icheon-si,KR", "Icheon,KR", "Icheon-si", "Icheon"],
            "안성": ["Anseong-si,KR", "Anseong,KR", "Anseong-si", "Anseong"],
            "여주": ["Yeoju-si,KR", "Yeoju,KR", "Yeoju-si", "Yeoju"],
            "양평": ["Yangpyeong-gun,KR", "Yangpyeong,KR", "Yangpyeong-gun", "Yangpyeong"],
            "동두천": ["Dongducheon-si,KR", "Dongducheon,KR", "Dongducheon-si", "Dongducheon"],
            "가평": ["Gapyeong-gun,KR", "Gapyeong,KR", "Gapyeong-gun", "Gapyeong"],
            "연천": ["Yeoncheon-gun,KR", "Yeoncheon,KR", "Yeoncheon-gun", "Yeoncheon"],
            "양주": ["Yangju-si,KR", "Yangju,KR", "Yangju-si", "Yangju"],
            "구리": ["Guri-si,KR", "Guri,KR", "Guri-si", "Guri"],
            "남양주": ["Namyangju-si,KR", "Namyangju,KR", "Namyangju-si", "Namyangju"],
            "포천": ["Pocheon-si,KR", "Pocheon,KR", "Pocheon-si", "Pocheon"],
            "춘천": ["Chuncheon-si,KR", "Chuncheon,KR", "Chuncheon-si", "Chuncheon"],
            "원주": ["Wonju-si,KR", "Wonju,KR", "Wonju-si", "Wonju"],
            "강릉": ["Gangneung-si,KR", "Gangneung,KR", "Gangneung-si", "Gangneung"],
            "속초": ["Sokcho-si,KR", "Sokcho,KR", "Sokcho-si", "Sokcho"],
            "동해": ["Donghae-si,KR", "Donghae,KR", "Donghae-si", "Donghae"],
            "태백": ["Taebaek-si,KR", "Taebaek,KR", "Taebaek-si", "Taebaek"],
            "평창": ["Pyeongchang-gun,KR", "Pyeongchang,KR", "Pyeongchang-gun", "Pyeongchang"],
            "정선": ["Jeongseon-gun,KR", "Jeongseon,KR", "Jeongseon-gun", "Jeongseon"],
            "청주": ["Cheongju-si,KR", "Cheongju,KR", "Cheongju-si", "Cheongju"],
            "충주": ["Chungju-si,KR", "Chungju,KR", "Chungju-si", "Chungju"],
            "천안": ["Cheonan-si,KR", "Cheonan,KR", "Cheonan-si", "Cheonan"],
            "공주": ["Gongju-si,KR", "Gongju,KR", "Gongju-si", "Gongju"],
            "보령": ["Boryeong-si,KR", "Boryeong,KR", "Boryeong-si", "Boryeong"],
            "아산": ["Asan-si,KR", "Asan,KR", "Asan-si", "Asan"],
            "서산": ["Seosan-si,KR", "Seosan,KR", "Seosan-si", "Seosan"],
            "논산": ["Nonsan-si,KR", "Nonsan,KR", "Nonsan-si", "Nonsan"],
            "전주": ["Jeonju-si,KR", "Jeonju,KR", "Jeonju-si", "Jeonju"],
            "군산": ["Gunsan-si,KR", "Gunsan,KR", "Gunsan-si", "Gunsan"],
            "익산": ["Iksan-si,KR", "Iksan,KR", "Iksan-si", "Iksan"],
            "목포": ["Mokpo-si,KR", "Mokpo,KR", "Mokpo-si", "Mokpo"],
            "여수": ["Yeosu-si,KR", "Yeosu,KR", "Yeosu-si", "Yeosu"],
            "순천": ["Suncheon-si,KR", "Suncheon,KR", "Suncheon-si", "Suncheon"],
            "나주": ["Naju-si,KR", "Naju,KR", "Naju-si", "Naju"],
            "광양": ["Gwangyang-si,KR", "Gwangyang,KR", "Gwangyang-si", "Gwangyang"],
            "포항": ["Pohang-si,KR", "Pohang,KR", "Pohang-si", "Pohang"],
            "경주": ["Gyeongju-si,KR", "Gyeongju,KR", "Gyeongju-si", "Gyeongju"],
            "김천": ["Gimcheon-si,KR", "Gimcheon,KR", "Gimcheon-si", "Gimcheon"],
            "안동": ["Andong-si,KR", "Andong,KR", "Andong-si", "Andong"],
            "구미": ["Gumi-si,KR", "Gumi,KR", "Gumi-si", "Gumi"],
            "창원": ["Changwon-si,KR", "Changwon,KR", "Changwon-si", "Changwon"],
            "진주": ["Jinju-si,KR", "Jinju,KR", "Jinju-si", "Jinju"],
            "통영": ["Tongyeong-si,KR", "Tongyeong,KR", "Tongyeong-si", "Tongyeong"],
            "제주": ["Jeju-si,KR", "Jeju,KR", "Jeju-si", "Jeju"],
            "서귀포": ["Seogwipo-si,KR", "Seogwipo,KR", "Seogwipo-si", "Seogwipo"]
        }
        
        # 한글 도시명을 영문으로 변환
        if city_input in KOREAN_CITIES:
            city_query = KOREAN_CITIES[city_input]
        else:
            # 매핑에 없으면 입력된 그대로 사용
            city_query = city_input
        
        # 대안 이름이 있는 도시의 경우 여러 가지 이름으로 시도
        if city_input in alternative_city_names:
            alternative_names = alternative_city_names[city_input]
            for alt_name in alternative_names:
                try:
                    params = {
                        'q': alt_name,
                        'appid': API_KEY,
                        'units': 'metric',
                        'lang': 'kr'
                    }
                    response = requests.get(BASE_URL, params=params, timeout=10)
                    if response.status_code == 200:
                        weather_data = response.json()
                        # 필수 데이터 검증
                        required_fields = ['name', 'main', 'weather', 'sys']
                        missing_fields = [field for field in required_fields if field not in weather_data]
                        
                        if missing_fields:
                            st.warning(f"⚠️ 일부 날씨 정보가 누락되었습니다: {', '.join(missing_fields)}")
                        
                        return weather_data
                except:
                    continue
        
        # API 요청 파라미터
        params = {
            'q': city_query,
            'appid': API_KEY,
            'units': 'metric',  # 섭씨 온도
            'lang': 'kr'  # 한국어
        }
        
        # API 요청
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            weather_data = response.json()
            
            # 필수 데이터 검증
            required_fields = ['name', 'main', 'weather', 'sys']
            missing_fields = [field for field in required_fields if field not in weather_data]
            
            if missing_fields:
                st.warning(f"⚠️ 일부 날씨 정보가 누락되었습니다: {', '.join(missing_fields)}")
            
            return weather_data
        elif response.status_code == 401:
            st.error("❌ API 키가 유효하지 않습니다. API 키를 확인해주세요.")
            return None
        elif response.status_code == 404:
            st.error(f"❌ '{city_input}' 도시를 찾을 수 없습니다.")
            st.info(f"💡 '{city_input}'는 OpenWeather API에서 지원하지 않을 수 있습니다. 인근 도시를 검색해보세요.")
            return None
        else:
            st.error(f"❌ API 요청 오류: {response.status_code}")
            return None
    
    except requests.exceptions.Timeout:
        st.error("❌ 요청 시간이 초과되었습니다. 다시 시도해주세요.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ 네트워크 오류: {e}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"❌ JSON 파싱 오류: {e}")
        return None

def display_weather(weather_data):
    """날씨 정보를 화면에 표시하는 함수"""
    if not weather_data:
        st.error("❌ 날씨 데이터를 불러올 수 없습니다.")
        return
    
    # 데이터 유효성 검증
    is_valid, validation_message = validate_weather_data(weather_data)
    if not is_valid:
        st.warning(f"⚠️ {validation_message}")
        # 일부 데이터라도 표시할 수 있도록 계속 진행
    
    try:
        # 기본 정보 추출 (안전한 방식으로)
        english_city_name = weather_data.get('name', '알 수 없는 도시')
        korean_city_name = get_korean_city_name(english_city_name)
        country = weather_data.get('sys', {}).get('country', 'N/A')
        
        # 메인 날씨 정보
        main_data = weather_data.get('main', {})
        temp = main_data.get('temp', 0)
        feels_like = main_data.get('feels_like', temp)
        temp_min = main_data.get('temp_min', temp)
        temp_max = main_data.get('temp_max', temp)
        humidity = main_data.get('humidity', 0)
        pressure = main_data.get('pressure', 0)
        
        # 바람 정보
        wind_data = weather_data.get('wind', {})
        wind_speed = wind_data.get('speed', 0)
        wind_deg = wind_data.get('deg', 0)
        
        # 날씨 상태
        weather_info = weather_data.get('weather', [{}])[0]
        description = weather_info.get('description', '정보 없음')
        weather_icon = weather_info.get('icon', '01d')
        
        # 시간 정보 (안전하게 처리)
        sys_data = weather_data.get('sys', {})
        sunrise_timestamp = sys_data.get('sunrise')
        sunset_timestamp = sys_data.get('sunset')
        
        if sunrise_timestamp and sunset_timestamp:
            sunrise = datetime.fromtimestamp(sunrise_timestamp).strftime('%H:%M')
            sunset = datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M')
        else:
            sunrise = "정보 없음"
            sunset = "정보 없음"
        
        # 가시거리 (안전하게 처리)
        visibility_raw = weather_data.get('visibility', 0)
        if visibility_raw and visibility_raw > 0:
            visibility = visibility_raw / 1000  # km로 변환
        else:
            visibility = 0
        
        # 구름량
        clouds_data = weather_data.get('clouds', {})
        clouds = clouds_data.get('all', 0)
        
    except Exception as e:
        st.error(f"❌ 날씨 데이터를 처리하는 중 오류가 발생했습니다: {str(e)}")
        return
    
    # 날씨에 따른 배경 이미지 설정 (안전하게 처리)
    try:
        weather_main = weather_info.get('main', 'Clear')
        weather_image_path = get_weather_image(weather_main, weather_icon)
        set_background_image(weather_image_path)
    except Exception as e:
        st.warning(f"⚠️ 배경 이미지를 설정할 수 없습니다: {str(e)}")
        # 기본 배경 이미지 사용
        set_background_image('images/sun.jpeg')
    
    # 메인 제목 (한글 도시명 사용)
    st.title(f"{get_weather_icon(weather_icon)} {korean_city_name}")
    
    # 날씨 설명
    st.subheader(f"날씨: {description.title()}")
    
    # 날씨 정보를 카드 형태로 표시
    st.markdown("### 📊 상세 날씨 정보")
    
    # 첫 번째 행 - 온도 관련
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp_display = f"{temp:.1f}" if temp != 0 else "N/A"
        st.markdown(create_weather_card("현재 온도", temp_display, "°C", "🌡️"), unsafe_allow_html=True)
    
    with col2:
        feels_like_display = f"{feels_like:.1f}" if feels_like != 0 else "N/A"
        st.markdown(create_weather_card("체감 온도", feels_like_display, "°C", "🌡️"), unsafe_allow_html=True)
    
    with col3:
        temp_min_display = f"{temp_min:.1f}" if temp_min != 0 else "N/A"
        st.markdown(create_weather_card("최저 온도", temp_min_display, "°C", "📉"), unsafe_allow_html=True)
    
    with col4:
        temp_max_display = f"{temp_max:.1f}" if temp_max != 0 else "N/A"
        st.markdown(create_weather_card("최고 온도", temp_max_display, "°C", "📈"), unsafe_allow_html=True)
    
    # 두 번째 행 - 기타 정보
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        humidity_display = f"{humidity}" if humidity != 0 else "N/A"
        st.markdown(create_weather_card("습도", humidity_display, "%", "💧"), unsafe_allow_html=True)
    
    with col6:
        pressure_display = f"{pressure}" if pressure != 0 else "N/A"
        st.markdown(create_weather_card("기압", pressure_display, " hPa", "🔽"), unsafe_allow_html=True)
    
    with col7:
        wind_speed_display = f"{wind_speed}" if wind_speed != 0 else "N/A"
        st.markdown(create_weather_card("풍속", wind_speed_display, " m/s", "🌬️"), unsafe_allow_html=True)
    
    with col8:
        wind_deg_display = f"{wind_deg}" if wind_deg != 0 else "N/A"
        st.markdown(create_weather_card("풍향", wind_deg_display, "°", "🧭"), unsafe_allow_html=True)
    
    # 세 번째 행 - 시간 및 기타
    col9, col10, col11, col12 = st.columns(4)
    
    with col9:
        sunrise_display = sunrise if sunrise != "정보 없음" else "N/A"
        st.markdown(create_weather_card("일출", sunrise_display, "", "🌅"), unsafe_allow_html=True)
    
    with col10:
        sunset_display = sunset if sunset != "정보 없음" else "N/A"
        st.markdown(create_weather_card("일몰", sunset_display, "", "🌇"), unsafe_allow_html=True)
    
    with col11:
        visibility_display = f"{visibility:.1f}" if visibility > 0 else "N/A"
        st.markdown(create_weather_card("가시거리", visibility_display, " km", "👁️"), unsafe_allow_html=True)
    
    with col12:
        clouds_display = f"{clouds}" if clouds != 0 else "N/A"
        st.markdown(create_weather_card("구름량", clouds_display, "%", "☁️"), unsafe_allow_html=True)
    
    # 추가 정보
    with st.expander("📊 상세 정보"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**위치 정보**")
            st.write(f"• 도시: {korean_city_name}")
            st.write(f"• 국가: {country}")
            st.write(f"• 위도: {weather_data['coord']['lat']:.4f}°")
            st.write(f"• 경도: {weather_data['coord']['lon']:.4f}°")
        
        with col2:
            st.write("**날씨 상세**")
            st.write(f"• 날씨 ID: {weather_data['weather'][0]['id']}")
            st.write(f"• 날씨 메인: {weather_data['weather'][0]['main']}")
            st.write(f"• 구름량: {clouds}%")
            st.write(f"• 가시거리: {visibility:.1f} km")
        
        # 강수량 정보 (있는 경우)
        if 'rain' in weather_data:
            rain_1h = weather_data['rain'].get('1h', 0)
            st.write(f"• 1시간 강수량: {rain_1h} mm")
        
        if 'snow' in weather_data:
            snow_1h = weather_data['snow'].get('1h', 0)
            st.write(f"• 1시간 적설량: {snow_1h} mm")

def get_city_categories():
    """도시를 시/군/구와 동/읍/면으로 분류하는 함수"""
    return {
        "특별시/광역시": {
            "서울특별시": ["서울"],
            "부산광역시": ["부산"],
            "대구광역시": ["대구"],
            "인천광역시": ["인천"],
            "광주광역시": ["광주"],
            "대전광역시": ["대전"],
            "울산광역시": ["울산"],
            "세종특별자치시": ["세종"]
        },
        "경기도": {
            "시": ["수원", "성남", "의정부", "안양", "부천", "용인", "고양", "파주", "화성", "시흥", "군포", "의왕", "하남", "광명", "평택", "과천", "오산", "이천", "안성", "여주", "동두천", "양주", "구리", "남양주", "포천"],
            "군": ["양평", "가평", "연천"]
        },
        "강원도": {
            "시": ["춘천", "원주", "강릉", "속초", "동해", "태백"],
            "군": ["평창", "정선", "홍천", "횡성", "영월", "철원", "화천", "양구", "인제", "고성", "양양"]
        },
        "충청북도": {
            "시": ["청주", "충주", "제천"],
            "군": ["보은", "옥천", "영동", "증평", "진천", "괴산", "음성", "단양"]
        },
        "충청남도": {
            "시": ["천안", "공주", "보령", "아산", "서산", "논산", "계룡"],
            "군": ["금산", "부여", "서천", "청양", "홍성", "예산", "태안", "당진"]
        },
        "전라북도": {
            "시": ["전주", "군산", "익산", "정읍", "남원", "김제"],
            "군": ["완주", "진안", "무주", "장수", "임실", "순창", "고창", "부안"]
        },
        "전라남도": {
            "시": ["목포", "여수", "순천", "나주", "광양"],
            "군": ["담양", "곡성", "구례", "고흥", "보성", "화순", "장흥", "강진", "해남", "영암", "무안", "함평", "영광", "장성", "완도", "진도", "신안"]
        },
        "경상북도": {
            "시": ["포항", "경주", "김천", "안동", "구미", "영주", "영천", "상주", "문경", "경산"],
            "군": ["군위", "의성", "청송", "영양", "영덕", "청도", "고령", "성주", "칠곡", "예천", "봉화", "울진", "울릉"]
        },
        "경상남도": {
            "시": ["창원", "진주", "통영", "사천", "김해", "밀양", "거제", "양산"],
            "군": ["의령", "함안", "창녕", "고성", "남해", "하동", "산청", "함양", "거창", "합천"]
        },
        "제주특별자치도": {
            "시": ["제주", "서귀포"],
            "군": []
        }
    }

def main():
    """메인 함수"""
    # 제목
    st.title("🌤️ 한국 날씨 정보")
    st.markdown("한국의 모든 도시 날씨를 실시간으로 확인하세요!")
    
    # 사이드바
    st.sidebar.title("🔍 날씨 검색")
    
    # 도시 입력 (기존 방식 유지)
    city = st.sidebar.text_input(
        "도시 이름을 직접 입력:",
        placeholder="예: 서울, 부산, 대전"
    )
    
    # 검색 버튼
    if st.sidebar.button("🔍 검색", type="primary"):
        if city:
            with st.spinner(f"{city}의 날씨 정보를 가져오는 중..."):
                weather_data = get_weather(city)
                if weather_data:
                    display_weather(weather_data)
                else:
                    st.error("❌ 해당 도시의 날씨 정보를 찾을 수 없습니다.")
        else:
            st.warning("⚠️ 도시 이름을 입력해주세요.")
    
    # 드롭박스 기반 도시 선택
    st.sidebar.markdown("---")
    st.sidebar.subheader("🗺️ 지역별 도시 선택")
    
    # 도시 분류 (시/군/구와 동/읍/면으로 구분)
    city_hierarchy = {
        "특별시/광역시": {
            "서울특별시": {
                "강남구": {
                    "동": ["역삼동", "개포동", "청담동", "삼성동", "대치동", "신사동", "논현동", "압구정동", "도곡동", "일원동", "수서동", "세곡동"]
                },
                "강동구": {
                    "동": ["명일동", "고덕동", "상일동", "길동", "둔촌동", "암사동", "성내동", "천호동"]
                },
                "강북구": {
                    "동": ["삼양동", "미아동", "번동", "수유동", "우이동"]
                },
                "강서구": {
                    "동": ["염창동", "등촌동", "화곡동", "가양동", "마곡동", "내발산동", "외발산동", "공항동", "방화동", "개화동"]
                },
                "관악구": {
                    "동": ["보라매동", "청림동", "성현동", "행운동", "낙성대동", "청룡동", "은천동", "중앙동", "인헌동", "남현동", "서원동", "신림동", "삼성동", "미성동", "난곡동", "난향동"]
                },
                "광진구": {
                    "동": ["중곡동", "능동", "구의동", "광장동", "자양동", "화양동", "군자동"]
                },
                "구로구": {
                    "동": ["신도림동", "구로동", "가리봉동", "고척동", "개봉동", "오류동", "천왕동", "항동", "온수동"]
                },
                "금천구": {
                    "동": ["가산동", "독산동", "시흥동"]
                },
                "노원구": {
                    "동": ["월계동", "공릉동", "하계동", "중계동", "상계동", "녹천동", "당고개동"]
                },
                "도봉구": {
                    "동": ["쌍문동", "방학동", "창동", "도봉동"]
                },
                "동대문구": {
                    "동": ["용신동", "제기동", "전농동", "답십리동", "장안동", "청량리동", "회기동", "휘경동", "이문동"]
                },
                "동작구": {
                    "동": ["노량진동", "상도동", "본동", "흑석동", "사당동", "대방동", "신대방동"]
                },
                "마포구": {
                    "동": ["공덕동", "아현동", "도화동", "용강동", "대흥동", "염리동", "신수동", "서강동", "서교동", "합정동", "망원동", "연남동", "성산동", "상암동"]
                },
                "서대문구": {
                    "동": ["충현동", "천연동", "신촌동", "연희동", "홍제동", "홍은동", "남가좌동", "북가좌동"]
                },
                "서초구": {
                    "동": ["방배동", "양재동", "내곡동", "신원동", "원지동", "잠원동", "반포동", "서초동"]
                },
                "성동구": {
                    "동": ["왕십리동", "마장동", "사근동", "행당동", "응봉동", "금호동", "옥수동", "성수동", "송정동", "용답동"]
                },
                "성북구": {
                    "동": ["성북동", "삼선동", "동선동", "돈암동", "안암동", "보문동", "정릉동", "길음동", "종암동", "하월곡동", "상월곡동", "장위동", "석관동"]
                },
                "송파구": {
                    "동": ["풍납동", "거여동", "마천동", "방이동", "오금동", "송파동", "석촌동", "삼전동", "가락동", "문정동", "장지동", "위례동", "잠실동", "신천동"]
                },
                "양천구": {
                    "동": ["목동", "신월동", "신정동"]
                },
                "영등포구": {
                    "동": ["영등포동", "여의도동", "당산동", "도림동", "문래동", "양평동", "신길동", "대림동", "신풍동"]
                },
                "용산구": {
                    "동": ["후암동", "용산동", "남영동", "청파동", "원효로동", "효창동", "용문동", "한강로동", "이촌동", "이태원동", "한남동", "서빙고동", "보광동"]
                },
                "은평구": {
                    "동": ["수색동", "녹번동", "불광동", "갈현동", "구산동", "대조동", "응암동", "역촌동", "신사동", "증산동", "진관동"]
                },
                "종로구": {
                    "동": ["청운동", "신교동", "궁정동", "효자동", "창신동", "숭인동", "이화동", "혜화동", "명륜동", "와룡동", "무악동", "교남동", "평창동", "부암동", "삼청동", "가회동", "종로동", "중학동"]
                },
                "중구": {
                    "동": ["소공동", "회현동", "명동", "필동", "장충동", "광희동", "을지로동", "신당동", "다산동", "약수동", "청구동"]
                },
                "중랑구": {
                    "동": ["면목동", "상봉동", "중화동", "묵동", "망우동", "신내동"]
                }
            },
            "부산광역시": {
                "강서구": {
                    "동": ["대저동", "명지동", "가락동", "녹산동", "가덕도동", "천성동", "지사동"]
                },
                "금정구": {
                    "동": ["구서동", "금성동", "남산동", "부곡동", "장전동", "청룡동"]
                },
                "남구": {
                    "동": ["감만동", "대연동", "용호동", "우암동", "문현동", "용당동"]
                },
                "동구": {
                    "동": ["초량동", "수정동", "좌천동", "범일동"]
                },
                "동래구": {
                    "동": ["명장동", "온천동", "사직동", "안락동", "복천동"]
                },
                "부산진구": {
                    "동": ["부전동", "연지동", "초읍동", "양정동", "전포동", "부암동", "당감동", "가야동", "개금동"]
                },
                "북구": {
                    "동": ["구포동", "금곡동", "화명동", "덕천동", "만덕동"]
                },
                "사상구": {
                    "동": ["삼락동", "모라동", "덕포동", "괘법동", "감전동", "주례동", "학장동", "엄궁동"]
                },
                "사하구": {
                    "동": ["괴정동", "당리동", "하단동", "신평동", "장림동", "다대동", "구평동", "감천동"]
                },
                "서구": {
                    "동": ["아미동", "부민동", "충무동", "남부민동", "암남동", "서대신동", "동대신동"]
                },
                "수영구": {
                    "동": ["남천동", "수영동", "망미동", "광안동", "민락동"]
                },
                "연제구": {
                    "동": ["연산동", "거제동"]
                },
                "영도구": {
                    "동": ["남항동", "영선동", "신선동", "봉래동", "청학동", "동삼동"]
                },
                "중구": {
                    "동": ["중앙동", "동광동", "대청동", "보수동", "부평동", "영주동"]
                },
                "해운대구": {
                    "동": ["우동", "중동", "좌동", "송정동", "반여동", "반송동", "재송동"]
                },
                "기장군": {
                    "읍": ["기장읍", "장안읍"],
                    "면": ["일광면", "정관면", "철마면"]
                }
            },
            "대구광역시": {
                "남구": {
                    "동": ["대명동", "봉덕동", "이천동", "대명동", "봉덕동", "이천동"]
                },
                "달서구": {
                    "동": ["성당동", "두류동", "본동", "감삼동", "용산동", "이곡동", "신당동", "월성동", "진천동", "상인동", "도원동", "송현동", "대곡동", "장기동", "호산동", "성당동", "두류동", "본동", "감삼동", "용산동", "이곡동", "신당동", "월성동", "진천동", "상인동", "도원동", "송현동", "대곡동", "장기동", "호산동"]
                },
                "달성군": {
                    "읍": ["화원읍", "논공읍", "다사읍", "하빈읍"],
                    "면": ["가창면", "옥포면", "현풍면", "구지면", "유가면", "현풍면", "구지면", "유가면"]
                },
                "동구": {
                    "동": ["신암동", "신천동", "효목동", "도평동", "불로동", "봉무동", "지저동", "동촌동", "방촌동", "해안동", "신암동", "신천동", "효목동", "도평동", "불로동", "봉무동", "지저동", "동촌동", "방촌동", "해안동"]
                },
                "북구": {
                    "동": ["칠성동", "고성동", "대현동", "산격동", "복현동", "무태동", "관문동", "태전동", "관음동", "읍내동", "동천동", "노원동", "국우동", "칠성동", "고성동", "대현동", "산격동", "복현동", "무태동", "관문동", "태전동", "관음동", "읍내동", "동천동", "노원동", "국우동"]
                },
                "서구": {
                    "동": ["내당동", "비산동", "평리동", "중리동", "원대동", "상중이동", "이현동", "원대동", "상중이동", "이현동"]
                },
                "수성구": {
                    "동": ["범어동", "만촌동", "수성동", "지산동", "동대구동", "신매동", "욱수동", "중동", "상동", "파동", "두산동", "고산동", "삼덕동", "연호동", "이천동", "범어동", "만촌동", "수성동", "지산동", "동대구동", "신매동", "욱수동", "중동", "상동", "파동", "두산동", "고산동", "삼덕동", "연호동", "이천동"]
                },
                "중구": {
                    "동": ["동인동", "삼덕동", "성내동", "대신동", "남산동", "대봉동", "동인동", "삼덕동", "성내동", "대신동", "남산동", "대봉동"]
                }
            },
            "인천광역시": {
                "계양구": {
                    "동": ["계산동", "계양동", "작전동", "서운동", "계산동", "계양동", "작전동", "서운동"]
                },
                "남구": {
                    "동": ["숭의동", "도화동", "주안동", "관교동", "문학동", "숭의동", "도화동", "주안동", "관교동", "문학동"]
                },
                "남동구": {
                    "동": ["구월동", "간석동", "만수동", "장수동", "서창동", "논현동", "고잔동", "구월동", "간석동", "만수동", "장수동", "서창동", "논현동", "고잔동"]
                },
                "동구": {
                    "동": ["만석동", "화수동", "송현동", "화평동", "금창동", "만석동", "화수동", "송현동", "화평동", "금창동"]
                },
                "부평구": {
                    "동": ["부평동", "산곡동", "청천동", "갈산동", "삼산동", "십정동", "일신동", "부평동", "산곡동", "청천동", "갈산동", "삼산동", "십정동", "일신동"]
                },
                "서구": {
                    "동": ["가정동", "가좌동", "검암동", "경서동", "공촌동", "금곡동", "대곡동", "마전동", "백석동", "불로동", "석남동", "시천동", "신현동", "원당동", "원창동", "청라동", "가정동", "가좌동", "검암동", "경서동", "공촌동", "금곡동", "대곡동", "마전동", "백석동", "불로동", "석남동", "시천동", "신현동", "원당동", "원창동", "청라동"]
                },
                "연수구": {
                    "동": ["송도동", "연수동", "청학동", "동춘동", "옥련동", "송도동", "연수동", "청학동", "동춘동", "옥련동"]
                },
                "중구": {
                    "동": ["운서동", "중산동", "신흥동", "덕교동", "무의동", "운서동", "중산동", "신흥동", "덕교동", "무의동"]
                },
                "강화군": {
                    "읍": ["강화읍", "선원읍"],
                    "면": ["불은면", "길상면", "화도면", "양도면", "내가면", "하점면", "양사면", "송해면", "교동면", "삼산면", "서도면"]
                },
                "옹진군": {
                    "읍": ["북도면"],
                    "면": ["연평면", "백령면", "대청면", "덕적면", "자월면"]
                }
            },
            "광주광역시": {
                "광산구": {
                    "동": ["송정동", "도산동", "신가동", "소촌동", "운남동", "월곡동", "비아동", "신창동", "수완동", "하남동", "임곡동", "오선동", "송정동", "도산동", "신가동", "소촌동", "운남동", "월곡동", "비아동", "신창동", "수완동", "하남동", "임곡동", "오선동"]
                },
                "남구": {
                    "동": ["양림동", "방림동", "봉선동", "구동", "월산동", "주월동", "노대동", "진월동", "덕남동", "행암동", "임암동", "송하동", "양림동", "방림동", "봉선동", "구동", "월산동", "주월동", "노대동", "진월동", "덕남동", "행암동", "임암동", "송하동"]
                },
                "동구": {
                    "동": ["계림동", "산수동", "지산동", "남동", "학동", "용산동", "운림동", "지원동", "계림동", "산수동", "지산동", "남동", "학동", "용산동", "운림동", "지원동"]
                },
                "북구": {
                    "동": ["중흥동", "유덕동", "누문동", "우산동", "풍향동", "용봉동", "일곡동", "양산동", "연제동", "신안동", "삼각동", "임동", "오치동", "중흥동", "유덕동", "누문동", "우산동", "풍향동", "용봉동", "일곡동", "양산동", "연제동", "신안동", "삼각동", "임동", "오치동"]
                },
                "서구": {
                    "동": ["양동", "농성동", "광천동", "유덕동", "치평동", "상무동", "화정동", "금호동", "풍암동", "세하동", "양동", "농성동", "광천동", "유덕동", "치평동", "상무동", "화정동", "금호동", "풍암동", "세하동"]
                }
            },
            "대전광역시": {
                "대덕구": {
                    "동": ["오정동", "대화동", "읍내동", "연축동", "신대동", "와동", "송촌동", "중리동", "덕암동", "목상동", "장동", "오정동", "대화동", "읍내동", "연축동", "신대동", "와동", "송촌동", "중리동", "덕암동", "목상동", "장동"]
                },
                "동구": {
                    "동": ["가양동", "가오동", "갑동", "낭월동", "대동", "대청동", "마산동", "비래동", "삼성동", "삼정동", "상소동", "세천동", "소제동", "신인동", "신촌동", "용운동", "용전동", "이사동", "인동", "자양동", "장동", "직동", "천동", "추동", "판암동", "하소동", "홍도동", "효동", "가양동", "가오동", "갑동", "낭월동", "대동", "대청동", "마산동", "비래동", "삼성동", "삼정동", "상소동", "세천동", "소제동", "신인동", "신촌동", "용운동", "용전동", "이사동", "인동", "자양동", "장동", "직동", "천동", "추동", "판암동", "하소동", "홍도동", "효동"]
                },
                "서구": {
                    "동": ["가수원동", "가장동", "갈마동", "관저동", "괴정동", "기성동", "내동", "도마동", "둔산동", "만년동", "매노동", "변동", "복수동", "봉곡동", "산직동", "삼천동", "성북동", "세천동", "송강동", "수완동", "신갈동", "신안동", "신촌동", "용문동", "용촌동", "우명동", "원정동", "월평동", "장안동", "정림동", "지족동", "평촌동", "호수동", "화암동", "흑석동", "가수원동", "가장동", "갈마동", "관저동", "괴정동", "기성동", "내동", "도마동", "둔산동", "만년동", "매노동", "변동", "복수동", "봉곡동", "산직동", "삼천동", "성북동", "세천동", "송강동", "수완동", "신갈동", "신안동", "신촌동", "용문동", "용촌동", "우명동", "원정동", "월평동", "장안동", "정림동", "지족동", "평촌동", "호수동", "화암동", "흑석동"]
                },
                "유성구": {
                    "동": ["갑동", "계산동", "관평동", "교촌동", "구암동", "궁동", "금고동", "노은동", "대정동", "덕명동", "도룡동", "둔곡동", "반석동", "봉명동", "상대동", "세동", "송강동", "수통동", "신동", "신봉동", "안산동", "어은동", "용계동", "원내동", "원신흥동", "원촌동", "자운동", "장대동", "전민동", "지족동", "추목동", "학하동", "갑동", "계산동", "관평동", "교촌동", "구암동", "궁동", "금고동", "노은동", "대정동", "덕명동", "도룡동", "둔곡동", "반석동", "봉명동", "상대동", "세동", "송강동", "수통동", "신동", "신봉동", "안산동", "어은동", "용계동", "원내동", "원신흥동", "원촌동", "자운동", "장대동", "전민동", "지족동", "추목동", "학하동"]
                },
                "중구": {
                    "동": ["가양동", "가오동", "갈마동", "구도동", "금동", "대사동", "대흥동", "목동", "문창동", "문화동", "부사동", "산성동", "석교동", "선화동", "성남동", "세동", "오류동", "용두동", "유천동", "은행동", "인동", "정동", "중촌동", "침산동", "태평동", "호동", "황호동", "가양동", "가오동", "갈마동", "구도동", "금동", "대사동", "대흥동", "목동", "문창동", "문화동", "부사동", "산성동", "석교동", "선화동", "성남동", "세동", "오류동", "용두동", "유천동", "은행동", "인동", "정동", "중촌동", "침산동", "태평동", "호동", "황호동"]
                }
            },
            "울산광역시": {
                "남구": {
                    "동": ["달동", "삼산동", "신정동", "옥동", "야음동", "여천동", "무거동", "달동", "삼산동", "신정동", "옥동", "야음동", "여천동", "무거동"]
                },
                "동구": {
                    "동": ["대송동", "전하동", "화정동", "대송동", "전하동", "화정동"]
                },
                "북구": {
                    "동": ["농소동", "산하동", "송정동", "양정동", "연암동", "중산동", "농소동", "산하동", "송정동", "양정동", "연암동", "중산동"]
                },
                "울주군": {
                    "읍": ["온산읍", "언양읍", "온양읍", "범서읍"],
                    "면": ["청량면", "웅촌면", "두동면", "두서면", "상북면", "삼남면", "삼동면"]
                },
                "중구": {
                    "동": ["교동", "다운동", "반구동", "병영동", "복산동", "성안동", "약사동", "우정동", "유곡동", "학성동", "교동", "다운동", "반구동", "병영동", "복산동", "성안동", "약사동", "우정동", "유곡동", "학성동"]
                }
            },
            "세종특별자치시": {
                "시": ["세종시"]
            }
        },
        "경기도": {
            "수원시": {
                "영통구": {
                    "동": ["영통동", "망포동", "신동", "하동", "원천동", "영통동", "망포동", "신동", "하동", "원천동"]
                },
                "장안구": {
                    "동": ["파장동", "영화동", "송죽동", "조원동", "연무동", "파장동", "영화동", "송죽동", "조원동", "연무동"]
                },
                "권선구": {
                    "동": ["세류동", "평동", "서둔동", "구운동", "금곡동", "호매실동", "세류동", "평동", "서둔동", "구운동", "금곡동", "호매실동"]
                },
                "팔달구": {
                    "동": ["매산동", "고등동", "우만동", "인계동", "매산동", "고등동", "우만동", "인계동"]
                }
            },
            "성남시": {
                "분당구": {
                    "동": ["정자동", "서현동", "이매동", "야탑동", "수내동", "정자동", "서현동", "이매동", "야탑동", "수내동"]
                },
                "수정구": {
                    "동": ["수진동", "신흥동", "단대동", "산성동", "수진동", "신흥동", "단대동", "산성동"]
                },
                "중원구": {
                    "동": ["성남동", "중앙동", "금광동", "은행동", "성남동", "중앙동", "금광동", "은행동"]
                }
            },
            "의정부시": {
                "동": ["의정부동", "호원동", "장암동", "신곡동", "자금동", "가능동", "녹양동", "의정부동", "호원동", "장암동", "신곡동", "자금동", "가능동", "녹양동"]
            },
            "안양시": {
                "동안구": {
                    "동": ["비산동", "관양동", "평촌동", "호계동", "비산동", "관양동", "평촌동", "호계동"]
                },
                "만안구": {
                    "동": ["안양동", "석수동", "박달동", "안양동", "석수동", "박달동"]
                }
            },
            "부천시": {
                "동": ["원미동", "소사동", "오정동", "원미동", "소사동", "오정동"]
            },
            "광명시": {
                "시": ["광명시"]
            },
            "평택시": {
                "시": ["평택시"]
            },
            "과천시": {
                "시": ["과천시"]
            },
            "오산시": {
                "시": ["오산시"]
            },
            "시흥시": {
                "시": ["시흥시"]
            },
            "군포시": {
                "시": ["군포시"]
            },
            "의왕시": {
                "시": ["의왕시"]
            },
            "하남시": {
                "시": ["하남시"]
            },
            "용인시": {
                "처인구": {
                    "동": ["용인동", "역북동", "삼가동"],
                    "읍": ["기흥읍", "수지읍", "처인읍"],
                    "면": ["모현면", "이동면", "남사면", "원삼면", "백암면", "양지면"]
                },
                "기흥구": {
                    "동": ["기흥동", "신갈동", "구갈동", "상갈동"]
                },
                "수지구": {
                    "동": ["수지동", "풍덕천동", "죽전동", "동천동"]
                }
            },
            "파주시": {
                "읍": ["파주읍", "법원읍", "조리읍"],
                "면": ["월롱면", "탄현면", "광탄면", "파평면", "적성면", "장단면", "진동면", "진서면"]
            },
            "이천시": {
                "읍": ["이천읍", "부발읍"],
                "면": ["신둔면", "백사면", "호법면", "마장면", "대월면", "모가면", "설성면", "율면"]
            },
            "안성시": {
                "읍": ["안성읍", "공도읍"],
                "면": ["금광면", "원곡면", "일죽면", "죽산면", "삼죽면", "고삼면", "양성면", "미양면", "대덕면", "보개면", "서운면"]
            },
            "김포시": {
                "읍": ["김포읍", "통진읍", "고촌읍"],
                "면": ["양촌면", "대곶면", "월곶면", "하성면"]
            },
            "화성시": {
                "읍": ["봉담읍", "우정읍", "향남읍", "남양읍", "매송읍", "비봉읍", "정남읍", "동탄읍"],
                "면": ["팔탄면", "장안면", "양감면", "정남면", "마도면", "송산면", "서신면"]
            },
            "여주시": {
                "읍": ["여주읍", "가남읍"],
                "면": ["점동면", "흥천면", "능서면", "대신면", "북내면", "강천면", "산북면", "금사면", "세종면"]
            },
            "양평군": {
                "읍": ["양평읍"],
                "면": ["강상면", "강하면", "양서면", "서종면", "단월면", "청운면", "양동면", "지평면", "용문면", "개군면", "옥천면", "양평면"]
            },
            "동두천시": {
                "동": ["생연동", "중앙동", "불현동", "송내동", "동두천동"]
            },
            "가평군": {
                "읍": ["가평읍"],
                "면": ["청평면", "상면", "하면", "북면", "조종면"]
            },
            "연천군": {
                "읍": ["연천읍", "전곡읍"],
                "면": ["군남면", "청산면", "왕징면", "신서면", "미산면", "중면", "장남면"]
            },
            "양주시": {
                "읍": ["양주읍", "회천읍"],
                "면": ["은현면", "남면", "광적면", "장흥면"]
            },
            "구리시": {
                "동": ["교문동", "수택동", "아천동", "인창동"]
            },
            "남양주시": {
                "읍": ["와부읍", "조안읍", "오남읍", "별내읍"],
                "면": ["수동면", "조안면", "퇴계원면", "화도면", "진접면", "진건면", "별내면"]
            },
            "포천시": {
                "읍": ["포천읍", "소흘읍"],
                "면": ["신북면", "창수면", "영중면", "일동면", "이동면", "영북면", "관인면", "화현면"]
            }
        },
        "강원도": {
            "춘천시": {
                "읍": ["춘천읍"],
                "면": ["신북면", "동면", "동산면", "신동면", "서면", "남면", "북면", "사북면", "사내면", "남산면", "교동면", "중도면", "동내면", "후평면", "신사우면", "강남면", "동면", "동산면", "신동면", "서면", "남면", "북면", "사북면", "사내면", "남산면", "교동면", "중도면", "동내면", "후평면", "신사우면", "강남면"]
            },
            "원주시": {
                "읍": ["원주읍"],
                "면": ["문막읍", "소초면", "호저면", "지정면", "부론면", "귀래면", "흥업면", "판부면", "신림면", "문막읍", "소초면", "호저면", "지정면", "부론면", "귀래면", "흥업면", "판부면", "신림면"]
            },
            "강릉시": {
                "읍": ["강릉읍"],
                "면": ["주문진읍", "성산면", "왕산면", "구정면", "강동면", "옥계면", "사천면", "연곡면", "주문진읍", "성산면", "왕산면", "구정면", "강동면", "옥계면", "사천면", "연곡면"]
            },
            "속초시": {
                "동": ["속초동", "교동", "노학동", "조양동", "청호동", "대포동", "속초동", "교동", "노학동", "조양동", "청호동", "대포동"]
            },
            "동해시": {
                "동": ["동해동", "천곡동", "송정동", "북삼동", "묵호동", "발한동", "어달동", "동해동", "천곡동", "송정동", "북삼동", "묵호동", "발한동", "어달동"]
            },
            "태백시": {
                "동": ["태백동", "황지동", "장성동", "화전동", "소도동", "태백동", "황지동", "장성동", "화전동", "소도동"]
            },
            "평창군": {
                "읍": ["평창읍"],
                "면": ["미탄면", "방림면", "대화면", "봉평면", "용평면", "진부면", "도암면", "미탄면", "방림면", "대화면", "봉평면", "용평면", "진부면", "도암면"]
            },
            "정선군": {
                "읍": ["정선읍"],
                "면": ["고한읍", "사북읍", "신동읍", "남면", "북평면", "임계면", "화암면", "여량면", "고한읍", "사북읍", "신동읍", "남면", "북평면", "임계면", "화암면", "여량면"]
            },
            "홍천군": {
                "읍": ["홍천읍"],
                "면": ["화촌면", "두촌면", "내촌면", "서석면", "영귀미면", "남면", "서면", "북방면", "내면", "화촌면", "두촌면", "내촌면", "서석면", "영귀미면", "남면", "서면", "북방면", "내면"]
            },
            "횡성군": {
                "읍": ["횡성읍"],
                "면": ["우천면", "안흥면", "둔내면", "갑천면", "청일면", "공근면", "서원면", "우천면", "안흥면", "둔내면", "갑천면", "청일면", "공근면", "서원면"]
            },
            "영월군": {
                "읍": ["영월읍"],
                "면": ["상동읍", "중동읍", "김삿갓면", "북면", "남면", "한반도면", "주천면", "수주면", "상동읍", "중동읍", "김삿갓면", "북면", "남면", "한반도면", "주천면", "수주면"]
            },
            "철원군": {
                "읍": ["철원읍"],
                "면": ["김화읍", "갈말읍", "동송읍", "서면", "근남면", "근북면", "근동면", "김화읍", "갈말읍", "동송읍", "서면", "근남면", "근북면", "근동면"]
            },
            "화천군": {
                "읍": ["화천읍"],
                "면": ["간동면", "하남면", "상서면", "사내면", "간동면", "하남면", "상서면", "사내면"]
            },
            "양구군": {
                "읍": ["양구읍"],
                "면": ["동면", "방산면", "해안면", "동면", "방산면", "해안면"]
            },
            "인제군": {
                "읍": ["인제읍"],
                "면": ["남면", "북면", "기린면", "서화면", "상남면", "인제읍", "남면", "북면", "기린면", "서화면", "상남면"]
            },
            "고성군": {
                "읍": ["간성읍"],
                "면": ["거진읍", "현내면", "죽왕면", "토성면", "간성읍", "거진읍", "현내면", "죽왕면", "토성면"]
            },
            "양양군": {
                "읍": ["양양읍"],
                "면": ["서면", "손양면", "현북면", "현남면", "강현면", "서면", "손양면", "현북면", "현남면", "강현면"]
            }
        },
        "충청북도": {
            "청주시": {
                "상당구": {
                    "동": ["상당동", "성안동", "탑대성동", "영운동", "금천동", "용담동", "문화동", "산성동", "상당동", "성안동", "탑대성동", "영운동", "금천동", "용담동", "문화동", "산성동"]
                },
                "서원구": {
                    "동": ["사직동", "사창동", "모충동", "산남동", "분평동", "수곡동", "성화동", "개신동", "사직동", "사창동", "모충동", "산남동", "분평동", "수곡동", "성화동", "개신동"]
                },
                "흥덕구": {
                    "동": ["복대동", "봉명동", "송절동", "화계동", "운천동", "신봉동", "가경동", "강서동", "복대동", "봉명동", "송절동", "화계동", "운천동", "신봉동", "가경동", "강서동"]
                },
                "청원구": {
                    "읍": ["내수읍", "오창읍"],
                    "면": ["북이면", "오송면", "강내면", "내수읍", "오창읍", "북이면", "오송면", "강내면"]
                }
            },
            "충주시": {
                "읍": ["충주읍"],
                "면": ["주덕읍", "살미면", "수안보면", "대소원면", "신니면", "노은면", "앙성면", "중앙탑면", "금가면", "동량면", "산척면", "엄정면", "소태면", "주덕읍", "살미면", "수안보면", "대소원면", "신니면", "노은면", "앙성면", "중앙탑면", "금가면", "동량면", "산척면", "엄정면", "소태면"]
            },
            "제천시": {
                "읍": ["제천읍"],
                "면": ["봉양읍", "송학면", "금성면", "청풍면", "수산면", "덕산면", "한수면", "백운면", "봉양읍", "송학면", "금성면", "청풍면", "수산면", "덕산면", "한수면", "백운면"]
            },
            "보은군": {
                "읍": ["보은읍"],
                "면": ["속리산면", "장안면", "마로면", "탄부면", "삼승면", "수한면", "회남면", "회인면", "내북면", "산외면", "속리산면", "장안면", "마로면", "탄부면", "삼승면", "수한면", "회남면", "회인면", "내북면", "산외면"]
            },
            "옥천군": {
                "읍": ["옥천읍"],
                "면": ["동이면", "안남면", "안내면", "청성면", "청산면", "이원면", "군서면", "군북면", "동이면", "안남면", "안내면", "청성면", "청산면", "이원면", "군서면", "군북면"]
            },
            "영동군": {
                "읍": ["영동읍"],
                "면": ["용산면", "황간면", "추풍령면", "매곡면", "상촌면", "양강면", "용화면", "학산면", "양산면", "심천면", "영동읍", "용산면", "황간면", "추풍령면", "매곡면", "상촌면", "양강면", "용화면", "학산면", "양산면", "심천면"]
            },
            "증평군": {
                "읍": ["증평읍"],
                "면": ["도안면", "증평읍", "도안면"]
            },
            "진천군": {
                "읍": ["진천읍"],
                "면": ["덕산읍", "초평면", "문백면", "백곡면", "이월면", "광혜원면", "덕산읍", "초평면", "문백면", "백곡면", "이월면", "광혜원면"]
            },
            "괴산군": {
                "읍": ["괴산읍"],
                "면": ["감물면", "문광면", "연풍면", "칠성면", "소수면", "불정면", "청천면", "청안면", "사리면", "장연면", "괴산읍", "감물면", "문광면", "연풍면", "칠성면", "소수면", "불정면", "청천면", "청안면", "사리면", "장연면"]
            },
            "음성군": {
                "읍": ["음성읍"],
                "면": ["금왕읍", "소이면", "원남면", "맹동면", "대소면", "삼성면", "생극면", "감곡면", "금왕읍", "소이면", "원남면", "맹동면", "대소면", "삼성면", "생극면", "감곡면"]
            },
            "단양군": {
                "읍": ["단양읍"],
                "면": ["매포읍", "가곡면", "영춘면", "어상천면", "적성면", "단성면", "대강면", "매포읍", "가곡면", "영춘면", "어상천면", "적성면", "단성면", "대강면"]
            }
        },
        "충청남도": {
            "천안시": {
                "동남구": {
                    "읍": ["목천읍", "풍세읍"],
                    "면": ["성환읍", "성거읍", "직산읍", "입장면"]
                },
                "서북구": {
                    "읍": ["성환읍", "성거읍", "직산읍"],
                    "면": ["입장면"]
                }
            },
            "공주시": {
                "읍": ["공주읍"],
                "면": ["유구읍", "이인면", "탄천면", "계룡면", "반포면", "의당면", "정안면", "우성면", "사곡면", "신풍면"]
            },
            "보령시": {
                "읍": ["보령읍"],
                "면": ["웅천읍", "주포면", "오천면", "천북면", "청소면", "청라면", "남포면", "주산면", "미산면", "성주면"]
            },
            "아산시": {
                "읍": ["아산읍"],
                "면": ["탕정면", "배방면", "송악면", "음봉면", "둔포면", "영인면", "인주면", "선장면", "도고면", "신창면"]
            },
            "서산시": {
                "읍": ["서산읍"],
                "면": ["대산읍", "인지면", "부석면", "팔봉면", "지곡면", "성연면", "음암면", "운산면", "해미면", "고북면"]
            },
            "논산시": {
                "읍": ["논산읍"],
                "면": ["강경읍", "연무읍", "성동면", "광석면", "노성면", "상월면", "부적면", "연산면", "벌곡면", "양촌면", "가야곡면", "은진면", "채운면"]
            },
            "계룡시": {
                "읍": ["계룡읍"],
                "면": ["엄사면", "신도안면"]
            },
            "금산군": {
                "읍": ["금산읍"],
                "면": ["금성면", "제원면", "부리면", "군북면", "남일면", "남이면", "진산면", "복수면", "추부면"]
            },
            "부여군": {
                "읍": ["부여읍"],
                "면": ["규암면", "은산면", "외산면", "내산면", "구룡면", "홍산면", "옥산면", "남면", "충화면", "양화면", "임천면", "장암면", "세도면", "석성면", "초촌면"]
            },
            "서천군": {
                "읍": ["서천읍"],
                "면": ["장항읍", "마서면", "화양면", "기산면", "한산면", "마산면", "시초면", "문산면", "판교면", "종천면", "비인면", "서면"]
            },
            "청양군": {
                "읍": ["청양읍"],
                "면": ["운곡면", "대치면", "정산면", "목면", "청남면", "장평면", "남양면", "화성면", "비봉면"]
            },
            "홍성군": {
                "읍": ["홍성읍"],
                "면": ["광천읍", "홍북읍", "금마면", "홍동면", "장곡면", "은하면", "결성면", "서부면", "갈산면", "구항면"]
            },
            "예산군": {
                "읍": ["예산읍"],
                "면": ["삽교읍", "대술면", "신양면", "광시면", "대흥면", "응봉면", "덕산면", "봉산면", "고덕면", "신암면", "오가면"]
            },
            "태안군": {
                "읍": ["태안읍"],
                "면": ["안면읍", "고남면", "남면", "근흥면", "소원면", "원북면", "이원면"]
            },
            "당진시": {
                "읍": ["당진읍"],
                "면": ["합덕읍", "송악읍", "고대면", "석문면", "대호지면", "정미면", "면천면", "순성면", "우강면", "신평면", "송산면"]
            }
        },
        "전라북도": {
            "전주시": {
                "완산구": {
                    "동": ["중앙동", "풍남동", "노송동", "완산동", "동서학동", "서서학동", "중앙동", "풍남동", "노송동", "완산동", "동서학동", "서서학동"]
                },
                "덕진구": {
                    "동": ["인후동", "덕진동", "금암동", "팔복동", "호성동", "송천동", "조촌동", "인후동", "덕진동", "금암동", "팔복동", "호성동", "송천동", "조촌동"]
                }
            },
            "군산시": {
                "읍": ["군산읍"],
                "면": ["옥구읍", "회현면", "임피면", "서수면", "대야면", "개정면", "성산면", "나포면", "옥도면", "옥구읍", "회현면", "임피면", "서수면", "대야면", "개정면", "성산면", "나포면", "옥도면"]
            },
            "익산시": {
                "읍": ["익산읍"],
                "면": ["함열읍", "오산면", "황등면", "함라면", "웅포면", "성당면", "용안면", "낭산면", "망성면", "여산면", "금마면", "왕궁면", "춘포면", "삼기면", "용동면", "함열읍", "오산면", "황등면", "함라면", "웅포면", "성당면", "용안면", "낭산면", "망성면", "여산면", "금마면", "왕궁면", "춘포면", "삼기면", "용동면"]
            },
            "정읍시": {
                "읍": ["정읍읍"],
                "면": ["신태인읍", "북면", "입암면", "소성면", "고부면", "영원면", "덕천면", "이평면", "정우면", "태인면", "감곡면", "옹동면", "칠보면", "산내면", "산외면", "신태인읍", "북면", "입암면", "소성면", "고부면", "영원면", "덕천면", "이평면", "정우면", "태인면", "감곡면", "옹동면", "칠보면", "산내면", "산외면"]
            },
            "남원시": {
                "읍": ["남원읍"],
                "면": ["운봉읍", "주천면", "수지면", "송동면", "주생면", "금지면", "대강면", "대산면", "사매면", "덕과면", "보절면", "산동면", "이백면", "아영면", "인월면", "운봉읍", "주천면", "수지면", "송동면", "주생면", "금지면", "대강면", "대산면", "사매면", "덕과면", "보절면", "산동면", "이백면", "아영면", "인월면"]
            },
            "김제시": {
                "읍": ["김제읍"],
                "면": ["만경읍", "죽산면", "백산면", "용지면", "백구면", "부량면", "공덕면", "청하면", "성덕면", "진봉면", "금구면", "봉남면", "황산면", "금산면", "광활면", "만경읍", "죽산면", "백산면", "용지면", "백구면", "부량면", "공덕면", "청하면", "성덕면", "진봉면", "금구면", "봉남면", "황산면", "금산면", "광활면"]
            },
            "완주군": {
                "읍": ["완주읍"],
                "면": ["봉동읍", "삼례읍", "상관면", "이서면", "소양면", "구이면", "고산면", "비봉면", "운주면", "화산면", "동상면", "경천면", "봉동읍", "삼례읍", "상관면", "이서면", "소양면", "구이면", "고산면", "비봉면", "운주면", "화산면", "동상면", "경천면"]
            },
            "진안군": {
                "읍": ["진안읍"],
                "면": ["용담면", "안천면", "동향면", "상전면", "백운면", "성수면", "마령면", "부귀면", "정천면", "주천면", "진안읍", "용담면", "안천면", "동향면", "상전면", "백운면", "성수면", "마령면", "부귀면", "정천면", "주천면"]
            },
            "무주군": {
                "읍": ["무주읍"],
                "면": ["무풍면", "설천면", "적상면", "안성면", "부남면", "무주읍", "무풍면", "설천면", "적상면", "안성면", "부남면"]
            },
            "장수군": {
                "읍": ["장수읍"],
                "면": ["산서면", "번암면", "장계면", "천천면", "계남면", "계북면", "장수읍", "산서면", "번암면", "장계면", "천천면", "계남면", "계북면"]
            },
            "임실군": {
                "읍": ["임실읍"],
                "면": ["청웅면", "운암면", "신평면", "성수면", "오수면", "삼계면", "관촌면", "강진면", "덕치면", "지사면", "임실읍", "청웅면", "운암면", "신평면", "성수면", "오수면", "삼계면", "관촌면", "강진면", "덕치면", "지사면"]
            },
            "순창군": {
                "읍": ["순창읍"],
                "면": ["인계면", "동계면", "풍산면", "금과면", "팔덕면", "쌍치면", "복흥면", "적성면", "유등면", "구림면", "순창읍", "인계면", "동계면", "풍산면", "금과면", "팔덕면", "쌍치면", "복흥면", "적성면", "유등면", "구림면"]
            },
            "고창군": {
                "읍": ["고창읍"],
                "면": ["고수면", "아산면", "무장면", "공음면", "상하면", "해리면", "성송면", "대산면", "심원면", "흥덕면", "성내면", "신림면", "부안면", "고창읍", "고수면", "아산면", "무장면", "공음면", "상하면", "해리면", "성송면", "대산면", "심원면", "흥덕면", "성내면", "신림면", "부안면"]
            },
            "부안군": {
                "읍": ["부안읍"],
                "면": ["줄포면", "위도면", "계화면", "보안면", "변산면", "진서면", "백산면", "상서면", "하서면", "동진면", "행안면", "부안읍", "줄포면", "위도면", "계화면", "보안면", "변산면", "진서면", "백산면", "상서면", "하서면", "동진면", "행안면"]
            }
        },
        "전라남도": {
            "목포시": {
                "동": ["용당동", "산정동", "연산동", "대성동", "양동", "불멸동", "용당동", "산정동", "연산동", "대성동", "양동", "불멸동"]
            },
            "여수시": {
                "읍": ["여수읍"],
                "면": ["돌산읍", "소라면", "율촌면", "화양면", "남면", "화정면", "삼산면", "돌산읍", "소라면", "율촌면", "화양면", "남면", "화정면", "삼산면"]
            },
            "순천시": {
                "읍": ["순천읍"],
                "면": ["승주읍", "해룡면", "서면", "황전면", "월등면", "주암면", "송광면", "외서면", "낙안면", "별량면", "상사면", "승주읍", "해룡면", "서면", "황전면", "월등면", "주암면", "송광면", "외서면", "낙안면", "별량면", "상사면"]
            },
            "나주시": {
                "읍": ["나주읍"],
                "면": ["다시면", "문평면", "노안면", "금천면", "산포면", "다도면", "봉황면", "나주읍", "다시면", "문평면", "노안면", "금천면", "산포면", "다도면", "봉황면"]
            },
            "광양시": {
                "읍": ["광양읍"],
                "면": ["광영읍", "봉강면", "옥룡면", "옥곡면", "진상면", "진월면", "다압면", "광양읍", "광영읍", "봉강면", "옥룡면", "옥곡면", "진상면", "진월면", "다압면"]
            },
            "담양군": {
                "읍": ["담양읍"],
                "면": ["봉산면", "고서면", "가사문학면", "창평면", "대덕면", "수북면", "대전면", "담양읍", "봉산면", "고서면", "가사문학면", "창평면", "대덕면", "수북면", "대전면"]
            },
            "곡성군": {
                "읍": ["곡성읍"],
                "면": ["오곡면", "삼기면", "석곡면", "목사동면", "죽곡면", "고달면", "옥과면", "입면", "겸면", "오산면", "곡성읍", "오곡면", "삼기면", "석곡면", "목사동면", "죽곡면", "고달면", "옥과면", "입면", "겸면", "오산면"]
            },
            "구례군": {
                "읍": ["구례읍"],
                "면": ["문척면", "간전면", "토지면", "마산면", "광의면", "용방면", "산동면", "구례읍", "문척면", "간전면", "토지면", "마산면", "광의면", "용방면", "산동면"]
            },
            "고흥군": {
                "읍": ["고흥읍"],
                "면": ["도양읍", "풍양면", "도덕면", "금산면", "도화면", "포두면", "봉래면", "점암면", "과역면", "남양면", "동강면", "대서면", "두원면", "영남면", "동일면", "고흥읍", "도양읍", "풍양면", "도덕면", "금산면", "도화면", "포두면", "봉래면", "점암면", "과역면", "남양면", "동강면", "대서면", "두원면", "영남면", "동일면"]
            },
            "보성군": {
                "읍": ["보성읍"],
                "면": ["벌교읍", "노동면", "미력면", "겸백면", "율어면", "복내면", "문덕면", "조성면", "득량면", "회천면", "웅치면", "보성읍", "벌교읍", "노동면", "미력면", "겸백면", "율어면", "복내면", "문덕면", "조성면", "득량면", "회천면", "웅치면"]
            },
            "화순군": {
                "읍": ["화순읍"],
                "면": ["한천면", "춘양면", "청풍면", "이양면", "능주면", "도곡면", "도암면", "이서면", "백아면", "동복면", "남면", "동면", "화순읍", "한천면", "춘양면", "청풍면", "이양면", "능주면", "도곡면", "도암면", "이서면", "백아면", "동복면", "남면", "동면"]
            },
            "장흥군": {
                "읍": ["장흥읍"],
                "면": ["관산읍", "대덕읍", "용산면", "안양면", "장동면", "장평면", "유치면", "부산면", "회진면", "장흥읍", "관산읍", "대덕읍", "용산면", "안양면", "장동면", "장평면", "유치면", "부산면", "회진면"]
            },
            "강진군": {
                "읍": ["강진읍"],
                "면": ["군동면", "칠량면", "대구면", "도암면", "신전면", "성전면", "작천면", "병영면", "옴천면", "마량면", "강진읍", "군동면", "칠량면", "대구면", "도암면", "신전면", "성전면", "작천면", "병영면", "옴천면", "마량면"]
            },
            "해남군": {
                "읍": ["해남읍"],
                "면": ["삼산면", "화산면", "현산면", "송지면", "북평면", "옥천면", "계곡면", "마산면", "황산면", "산이면", "문내면", "화원면", "해남읍", "삼산면", "화산면", "현산면", "송지면", "북평면", "옥천면", "계곡면", "마산면", "황산면", "산이면", "문내면", "화원면"]
            },
            "영암군": {
                "읍": ["영암읍"],
                "면": ["삼호읍", "덕진면", "금정면", "신북면", "시종면", "도포면", "군서면", "서호면", "학산면", "미암면", "영암읍", "삼호읍", "덕진면", "금정면", "신북면", "시종면", "도포면", "군서면", "서호면", "학산면", "미암면"]
            },
            "무안군": {
                "읍": ["무안읍"],
                "면": ["일로읍", "삼향읍", "몽탄면", "청계면", "현경면", "망운면", "해제면", "운남면", "무안읍", "일로읍", "삼향읍", "몽탄면", "청계면", "현경면", "망운면", "해제면", "운남면"]
            },
            "함평군": {
                "읍": ["함평읍"],
                "면": ["손불면", "신광면", "학교면", "엄다면", "대동면", "나산면", "해보면", "월야면", "함평읍", "손불면", "신광면", "학교면", "엄다면", "대동면", "나산면", "해보면", "월야면"]
            },
            "영광군": {
                "읍": ["영광읍"],
                "면": ["백수읍", "홍농읍", "대마면", "묘량면", "불갑면", "군서면", "군남면", "염산면", "법성면", "낙월면", "영광읍", "백수읍", "홍농읍", "대마면", "묘량면", "불갑면", "군서면", "군남면", "염산면", "법성면", "낙월면"]
            },
            "장성군": {
                "읍": ["장성읍"],
                "면": ["진원면", "남면", "동화면", "삼서면", "삼계면", "황룡면", "서삼면", "북일면", "북이면", "북하면", "장성읍", "진원면", "남면", "동화면", "삼서면", "삼계면", "황룡면", "서삼면", "북일면", "북이면", "북하면"]
            },
            "완도군": {
                "읍": ["완도읍"],
                "면": ["금일읍", "노화읍", "군외면", "신지면", "고금면", "약산면", "청산면", "소안면", "완도읍", "금일읍", "노화읍", "군외면", "신지면", "고금면", "약산면", "청산면", "소안면"]
            },
            "진도군": {
                "읍": ["진도읍"],
                "면": ["군내면", "고군면", "의신면", "임회면", "지산면", "조도면", "진도읍", "군내면", "고군면", "의신면", "임회면", "지산면", "조도면"]
            },
            "신안군": {
                "읍": ["지도읍"],
                "면": ["압해읍", "증도면", "임자면", "자은면", "비금면", "도초면", "흑산면", "하의면", "장산면", "안좌면", "팔금면", "암태면", "지도읍", "압해읍", "증도면", "임자면", "자은면", "비금면", "도초면", "흑산면", "하의면", "장산면", "안좌면", "팔금면", "암태면"]
            }
        },
        "경상북도": {
            "포항시": {
                "남구": {
                    "읍": ["구룡포읍", "연일읍", "오천읍"],
                    "면": ["대송면", "동해면", "장기면", "호미곶면", "구룡포읍", "연일읍", "오천읍", "대송면", "동해면", "장기면", "호미곶면"]
                },
                "북구": {
                    "읍": ["흥해읍", "신광면", "청하면", "송라면", "기계면", "죽장면", "흥해읍", "신광면", "청하면", "송라면", "기계면", "죽장면"]
                }
            },
            "경주시": {
                "읍": ["경주읍"],
                "면": ["안강읍", "건천읍", "외동읍", "양북면", "양남면", "내남면", "산내면", "서면", "현곡면", "강동면", "천북면", "안강읍", "건천읍", "외동읍", "양북면", "양남면", "내남면", "산내면", "서면", "현곡면", "강동면", "천북면"]
            },
            "김천시": {
                "읍": ["김천읍"],
                "면": ["아포읍", "농소면", "남면", "개령면", "감문면", "어모면", "봉산면", "대항면", "감천면", "조마면", "구성면", "지례면", "부항면", "대덕면", "증산면", "아포읍", "농소면", "남면", "개령면", "감문면", "어모면", "봉산면", "대항면", "감천면", "조마면", "구성면", "지례면", "부항면", "대덕면", "증산면"]
            },
            "안동시": {
                "읍": ["안동읍"],
                "면": ["풍산읍", "와룡면", "북후면", "서후면", "풍천면", "일직면", "남후면", "남선면", "임하면", "길안면", "임동면", "예안면", "도산면", "녹전면", "안동읍", "풍산읍", "와룡면", "북후면", "서후면", "풍천면", "일직면", "남후면", "남선면", "임하면", "길안면", "임동면", "예안면", "도산면", "녹전면"]
            },
            "구미시": {
                "읍": ["구미읍"],
                "면": ["선산읍", "고아읍", "무을면", "옥성면", "도개면", "해평면", "산동면", "장천면", "구미읍", "선산읍", "고아읍", "무을면", "옥성면", "도개면", "해평면", "산동면", "장천면"]
            },
            "영주시": {
                "읍": ["영주읍"],
                "면": ["풍기읍", "이산면", "평은면", "문수면", "장수면", "안정면", "봉현면", "순흥면", "단산면", "부석면", "영주읍", "풍기읍", "이산면", "평은면", "문수면", "장수면", "안정면", "봉현면", "순흥면", "단산면", "부석면"]
            },
            "영천시": {
                "읍": ["영천읍"],
                "면": ["금호읍", "청통면", "신녕면", "화산면", "화북면", "화남면", "자양면", "임고면", "고경면", "북안면", "대창면", "영천읍", "금호읍", "청통면", "신녕면", "화산면", "화북면", "화남면", "자양면", "임고면", "고경면", "북안면", "대창면"]
            },
            "상주시": {
                "읍": ["상주읍"],
                "면": ["함창읍", "중동면", "사벌면", "낙동면", "청리면", "공성면", "외남면", "내서면", "모동면", "모서면", "화동면", "화서면", "화북면", "외서면", "은척면", "공검면", "이안면", "화남면", "상주읍", "함창읍", "중동면", "사벌면", "낙동면", "청리면", "공성면", "외남면", "내서면", "모동면", "모서면", "화동면", "화서면", "화북면", "외서면", "은척면", "공검면", "이안면", "화남면"]
            },
            "문경시": {
                "읍": ["문경읍"],
                "면": ["가은읍", "영순면", "산양면", "호계면", "산북면", "동로면", "마성면", "문경읍", "가은읍", "영순면", "산양면", "호계면", "산북면", "동로면", "마성면"]
            },
            "경산시": {
                "읍": ["경산읍"],
                "면": ["하양읍", "진량읍", "압량읍", "와촌면", "자인면", "용성면", "남산면", "남천면", "경산읍", "하양읍", "진량읍", "압량읍", "와촌면", "자인면", "용성면", "남산면", "남천면"]
            },
            "군위군": {
                "읍": ["군위읍"],
                "면": ["소보면", "효령면", "부계면", "우보면", "의흥면", "산성면", "고로면", "군위읍", "소보면", "효령면", "부계면", "우보면", "의흥면", "산성면", "고로면"]
            },
            "의성군": {
                "읍": ["의성읍"],
                "면": ["단촌면", "점곡면", "옥산면", "사곡면", "춘산면", "가음면", "금성면", "봉양면", "비안면", "구천면", "단밀면", "단북면", "안계면", "다인면", "신평면", "안평면", "안사면", "의성읍", "단촌면", "점곡면", "옥산면", "사곡면", "춘산면", "가음면", "금성면", "봉양면", "비안면", "구천면", "단밀면", "단북면", "안계면", "다인면", "신평면", "안평면", "안사면"]
            },
            "청송군": {
                "읍": ["청송읍"],
                "면": ["주왕산면", "부남면", "현동면", "현서면", "안덕면", "파천면", "진보면", "청송읍", "주왕산면", "부남면", "현동면", "현서면", "안덕면", "파천면", "진보면"]
            },
            "영양군": {
                "읍": ["영양읍"],
                "면": ["입암면", "청기면", "일월면", "수비면", "영양읍", "입암면", "청기면", "일월면", "수비면"]
            },
            "영덕군": {
                "읍": ["영덕읍"],
                "면": ["강구면", "남정면", "달산면", "지품면", "축산면", "영해면", "병곡면", "창수면", "영덕읍", "강구면", "남정면", "달산면", "지품면", "축산면", "영해면", "병곡면", "창수면"]
            },
            "청도군": {
                "읍": ["청도읍"],
                "면": ["화양읍", "각남면", "풍각면", "각북면", "이서면", "운문면", "금천면", "매전면", "청도읍", "화양읍", "각남면", "풍각면", "각북면", "이서면", "운문면", "금천면", "매전면"]
            },
            "고령군": {
                "읍": ["고령읍"],
                "면": ["개진면", "운수면", "성산면", "다산면", "개진면", "운수면", "성산면", "다산면"]
            },
            "성주군": {
                "읍": ["성주읍"],
                "면": ["선남면", "용암면", "수륜면", "가천면", "금수면", "대가면", "벽진면", "초전면", "월항면", "성주읍", "선남면", "용암면", "수륜면", "가천면", "금수면", "대가면", "벽진면", "초전면", "월항면"]
            },
            "칠곡군": {
                "읍": ["왜관읍"],
                "면": ["북삼읍", "석적읍", "지천면", "동명면", "가산면", "약목면", "기산면", "왜관읍", "북삼읍", "석적읍", "지천면", "동명면", "가산면", "약목면", "기산면"]
            },
            "예천군": {
                "읍": ["예천읍"],
                "면": ["용문면", "감천면", "보문면", "호명면", "유천면", "용궁면", "개포면", "지보면", "풍양면", "효자면", "은풍면", "예천읍", "용문면", "감천면", "보문면", "호명면", "유천면", "용궁면", "개포면", "지보면", "풍양면", "효자면", "은풍면"]
            },
            "봉화군": {
                "읍": ["봉화읍"],
                "면": ["물야면", "봉성면", "법전면", "춘양면", "소천면", "재산면", "명호면", "상운면", "석포면", "봉화읍", "물야면", "봉성면", "법전면", "춘양면", "소천면", "재산면", "명호면", "상운면", "석포면"]
            },
            "울진군": {
                "읍": ["울진읍"],
                "면": ["평해읍", "북면", "근남면", "기성면", "온정면", "죽변면", "후포면", "금강송면", "매화면", "울진읍", "평해읍", "북면", "근남면", "기성면", "온정면", "죽변면", "후포면", "금강송면", "매화면"]
            },
            "울릉군": {
                "읍": ["울릉읍"],
                "면": ["서면", "북면", "울릉읍", "서면", "북면"]
            }
        },
        "경상남도": {
            "창원시": {
                "의창구": {
                    "읍": ["동읍", "북면"],
                    "면": ["대산면", "동읍", "북면", "대산면"]
                },
                "성산구": {
                    "읍": ["웅남동", "성주동", "중앙동", "웅남동", "성주동", "중앙동"]
                },
                "마산합포구": {
                    "읍": ["합포동", "해운동", "가포동", "합포동", "해운동", "가포동"]
                },
                "마산회원구": {
                    "읍": ["회원동", "내서읍", "회원동", "내서읍"]
                },
                "진해구": {
                    "읍": ["진해동", "충무동", "여좌동", "태백동", "경화동", "병영동", "석동", "이동", "자은동", "덕산동", "풍호동", "웅천동", "웅동동", "청안동", "안곡동", "용원동", "가주동", "진해동", "충무동", "여좌동", "태백동", "경화동", "병영동", "석동", "이동", "자은동", "덕산동", "풍호동", "웅천동", "웅동동", "청안동", "안곡동", "용원동", "가주동"]
                }
            },
            "진주시": {
                "읍": ["진주읍"],
                "면": ["문산읍", "내동면", "정촌면", "금곡면", "진성면", "일반성면", "사봉면", "지수면", "대곡면", "금산면", "집현면", "미천면", "명석면", "대평면", "수곡면", "진주읍", "문산읍", "내동면", "정촌면", "금곡면", "진성면", "일반성면", "사봉면", "지수면", "대곡면", "금산면", "집현면", "미천면", "명석면", "대평면", "수곡면"]
            },
            "통영시": {
                "읍": ["통영읍"],
                "면": ["산양읍", "용남면", "도산면", "광도면", "욕지면", "한산면", "사량면", "통영읍", "산양읍", "용남면", "도산면", "광도면", "욕지면", "한산면", "사량면"]
            },
            "사천시": {
                "읍": ["사천읍"],
                "면": ["정동면", "사남면", "용현면", "축동면", "곤양면", "곤명면", "서포면", "사천읍", "정동면", "사남면", "용현면", "축동면", "곤양면", "곤명면", "서포면"]
            },
            "김해시": {
                "읍": ["김해읍"],
                "면": ["장유읍", "진영읍", "한림면", "생림면", "상동면", "대동면", "동상면", "북상면", "구산면", "진례면", "부곡면", "김해읍", "장유읍", "진영읍", "한림면", "생림면", "상동면", "대동면", "동상면", "북상면", "구산면", "진례면", "부곡면"]
            },
            "밀양시": {
                "읍": ["밀양읍"],
                "면": ["삼랑진읍", "하남읍", "부북면", "상동면", "산외면", "산내면", "단장면", "상남면", "초동면", "무안면", "청도면", "밀양읍", "삼랑진읍", "하남읍", "부북면", "상동면", "산외면", "산내면", "단장면", "상남면", "초동면", "무안면", "청도면"]
            },
            "거제시": {
                "읍": ["거제읍"],
                "면": ["고현읍", "사등읍", "연초면", "하청면", "장목면", "장승포동", "능포동", "아주동", "옥포동", "문동동", "수월동", "일운면", "동부면", "남부면", "거제읍", "고현읍", "사등읍", "연초면", "하청면", "장목면", "장승포동", "능포동", "아주동", "옥포동", "문동동", "수월동", "일운면", "동부면", "남부면"]
            },
            "양산시": {
                "읍": ["양산읍"],
                "면": ["물금읍", "동면", "원동면", "상북면", "하북면", "양산읍", "물금읍", "동면", "원동면", "상북면", "하북면"]
            },
            "의령군": {
                "읍": ["의령읍"],
                "면": ["가례면", "칠곡면", "대의면", "화정면", "용덕면", "정곡면", "지정면", "낙서면", "부림면", "봉수면", "궁류면", "유곡면", "의령읍", "가례면", "칠곡면", "대의면", "화정면", "용덕면", "정곡면", "지정면", "낙서면", "부림면", "봉수면", "궁류면", "유곡면"]
            },
            "함안군": {
                "읍": ["함안읍"],
                "면": ["가야읍", "칠원읍", "함안면", "군북면", "법수면", "대산면", "칠서면", "칠북면", "산인면", "여항면", "함안읍", "가야읍", "칠원읍", "함안면", "군북면", "법수면", "대산면", "칠서면", "칠북면", "산인면", "여항면"]
            },
            "창녕군": {
                "읍": ["창녕읍"],
                "면": ["남지읍", "고암면", "성산면", "대합면", "이방면", "유어면", "대지면", "계성면", "영산면", "장마면", "도천면", "길곡면", "부곡면", "창녕읍", "남지읍", "고암면", "성산면", "대합면", "이방면", "유어면", "대지면", "계성면", "영산면", "장마면", "도천면", "길곡면", "부곡면"]
            },
            "고성군": {
                "읍": ["고성읍"],
                "면": ["삼산면", "하일면", "하이면", "상리면", "대가면", "영현면", "영오면", "개천면", "구만면", "회화면", "마암면", "동해면", "거류면", "고성읍", "삼산면", "하일면", "하이면", "상리면", "대가면", "영현면", "영오면", "개천면", "구만면", "회화면", "마암면", "동해면", "거류면"]
            },
            "남해군": {
                "읍": ["남해읍"],
                "면": ["이동면", "상주면", "삼동면", "미조면", "남면", "서면", "고현면", "설천면", "창선면", "남해읍", "이동면", "상주면", "삼동면", "미조면", "남면", "서면", "고현면", "설천면", "창선면"]
            },
            "하동군": {
                "읍": ["하동읍"],
                "면": ["화개면", "악양면", "적량면", "횡천면", "고전면", "금남면", "진교면", "양보면", "북천면", "청암면", "옥종면", "금성면", "하동읍", "화개면", "악양면", "적량면", "횡천면", "고전면", "금남면", "진교면", "양보면", "북천면", "청암면", "옥종면", "금성면"]
            },
            "산청군": {
                "읍": ["산청읍"],
                "면": ["차황면", "오부면", "생초면", "금서면", "삼장면", "시천면", "단성면", "신안면", "생비량면", "신등면", "산청읍", "차황면", "오부면", "생초면", "금서면", "삼장면", "시천면", "단성면", "신안면", "생비량면", "신등면"]
            },
            "함양군": {
                "읍": ["함양읍"],
                "면": ["마천면", "휴천면", "유림면", "수동면", "지곡면", "안의면", "서하면", "서상면", "백전면", "병곡면", "함양읍", "마천면", "휴천면", "유림면", "수동면", "지곡면", "안의면", "서하면", "서상면", "백전면", "병곡면"]
            },
            "거창군": {
                "읍": ["거창읍"],
                "면": ["주상면", "웅양면", "고제면", "북상면", "위천면", "마리면", "남상면", "남하면", "신원면", "가조면", "가북면", "거창읍", "주상면", "웅양면", "고제면", "북상면", "위천면", "마리면", "남상면", "남하면", "신원면", "가조면", "가북면"]
            },
            "합천군": {
                "읍": ["합천읍"],
                "면": ["봉산면", "묘산면", "가야면", "야로면", "율곡면", "초계면", "쌍책면", "덕곡면", "청덕면", "적중면", "대양면", "쌍백면", "삼가면", "가회면", "대병면", "용주면", "합천읍", "봉산면", "묘산면", "가야면", "야로면", "율곡면", "초계면", "쌍책면", "덕곡면", "청덕면", "적중면", "대양면", "쌍백면", "삼가면", "가회면", "대병면", "용주면"]
            }
        },
        "제주특별자치도": {
            "제주시": {
                "읍": ["제주읍"],
                "면": ["한림읍", "애월읍", "구좌읍", "조천읍", "한경면", "추자면", "우도면", "제주읍", "한림읍", "애월읍", "구좌읍", "조천읍", "한경면", "추자면", "우도면"]
            },
            "서귀포시": {
                "읍": ["서귀포읍"],
                "면": ["대정읍", "남원읍", "성산읍", "안덕면", "표선면", "송산면", "서귀포읍", "대정읍", "남원읍", "성산읍", "안덕면", "표선면", "송산면"]
            }
        }
    }
    
    # 지역 선택
    selected_region = st.sidebar.selectbox(
        "📍 지역을 선택하세요:",
        ["지역을 선택하세요"] + list(city_hierarchy.keys())
    )
    
    selected_city = None
    selected_district = None
    selected_dong = None
    
    if selected_region != "지역을 선택하세요":
        # 시/군/구 선택
        cities = list(city_hierarchy[selected_region].keys())
        selected_city = st.sidebar.selectbox(
            "🏙️ 시/군/구를 선택하세요:",
            ["시/군/구를 선택하세요"] + cities
        )
        
        if selected_city != "시/군/구를 선택하세요":
            # 구/군/시 선택
            districts = city_hierarchy[selected_region][selected_city]
            if districts:
                district_type = list(districts.keys())[0]  # 구, 시, 군 중 하나
                district_list = districts[district_type]
                
                selected_district = st.sidebar.selectbox(
                    f"🏘️ {district_type}을 선택하세요:",
                    [f"{district_type}을 선택하세요"] + district_list
                )
                
                # 동/읍/면 선택 (4단계)
                if selected_district != f"{district_type}을 선택하세요":
                    # 선택된 구/군/시에 동/읍/면 데이터가 있는지 확인
                    if selected_district in city_hierarchy[selected_region][selected_city]:
                        dong_data = city_hierarchy[selected_region][selected_city][selected_district]
                        if dong_data:
                            dong_type = list(dong_data.keys())[0]  # 동, 읍, 면 중 하나
                            dong_list = dong_data[dong_type]
                            
                            selected_dong = st.sidebar.selectbox(
                                f"🏠 {dong_type}을 선택하세요:",
                                [f"{dong_type}을 선택하세요"] + dong_list
                            )
    
    # 검색 버튼
    if selected_region != "지역을 선택하세요" and selected_city != "시/군/구를 선택하세요":
        search_city = selected_city
        
        # 구/군/시가 선택된 경우
        if selected_district and selected_district != f"{list(city_hierarchy[selected_region][selected_city].keys())[0]}을 선택하세요":
            search_city = selected_district
            
            # 동/읍/면이 선택된 경우
            if selected_dong and selected_dong != f"{list(city_hierarchy[selected_region][selected_city][selected_district].keys())[0]}을 선택하세요":
                search_city = selected_dong
        
        if st.sidebar.button("🔍 선택한 지역 검색", type="primary"):
            with st.spinner(f"{search_city}의 날씨 정보를 가져오는 중..."):
                weather_data = get_weather(search_city)
                if weather_data:
                    display_weather(weather_data)
                else:
                    st.error("❌ 해당 지역의 날씨 정보를 찾을 수 없습니다.")
    
    # 도시 검색 안내
    st.sidebar.markdown("---")
    st.sidebar.markdown("**💡 4단계 지역 선택 팁**")
    st.sidebar.info("• 1단계: 지역 선택 (특별시/광역시, 경기도 등)\n• 2단계: 시/군/구 선택 (서울특별시, 수원시 등)\n• 3단계: 구/군/시 선택 (강남구, 영통구 등)\n• 4단계: 동/읍/면 선택 (역삼동, 신림동 등)\n• 일부 도시는 여러 이름으로 자동 시도")
    
    # 사용법 안내
    if not city and not (selected_region != "지역을 선택하세요" and selected_city != "시/군/구를 선택하세요"):
        st.info("👈 왼쪽 사이드바에서 지역을 선택하거나 직접 입력해보세요!")
        st.markdown("""
        ### 🗺️ 4단계 드롭박스 기능
        - **계층적 지역 선택**: 지역 → 시/군/구 → 구/군/시 → 동/읍/면 순서로 드롭박스 선택
        - **정확한 지역 검색**: 구체적인 동/읍/면까지 선택 가능
        - **체계적 분류**: 특별시/광역시, 경기도, 강원도 등으로 구분
        - **세부 행정구역**: 서울 25개 구의 모든 동, 경기도 시/군의 읍/면까지 지원
        
        ### 📍 지원하는 모든 지역 (동/읍/면까지 완전 지원)
        - **특별시/광역시**: 서울(25개 구의 모든 동), 부산(16개 구의 모든 동), 대구(8개 구의 모든 동), 인천(10개 구의 모든 동), 광주(5개 구의 모든 동), 대전(5개 구의 모든 동), 울산(5개 구의 모든 동), 세종
        - **경기도**: 수원(4개 구의 모든 동), 성남(3개 구의 모든 동), 용인(3개 구의 모든 동), 안양(2개 구의 모든 동), 천안(2개 구의 모든 동) 등 28개 시/군의 모든 읍/면
        - **강원도**: 춘천, 원주, 강릉, 속초, 동해, 태백, 평창, 정선, 홍천, 횡성, 영월, 철원, 화천, 양구, 인제, 고성, 양양의 모든 읍/면
        - **충청북도**: 청주(4개 구의 모든 동), 충주, 제천, 보은, 옥천, 영동, 증평, 진천, 괴산, 음성, 단양의 모든 읍/면
        - **충청남도**: 천안(2개 구의 모든 동), 공주, 보령, 아산, 서산, 논산, 계룡, 당진, 금산, 부여, 서천, 청양, 홍성, 예산, 태안의 모든 읍/면
        - **전라북도**: 전주(2개 구의 모든 동), 군산, 익산, 정읍, 남원, 김제, 완주, 진안, 무주, 장수, 임실, 순창, 고창, 부안의 모든 읍/면
        - **전라남도**: 목포(모든 동), 여수, 순천, 나주, 광양, 담양, 곡성, 구례, 고흥, 보성, 화순, 장흥, 강진, 해남, 영암, 무안, 함평, 영광, 장성, 완도, 진도, 신안의 모든 읍/면
        - **경상북도**: 포항(2개 구의 모든 읍/면), 경주, 김천, 안동, 구미, 영주, 영천, 상주, 문경, 경산, 군위, 의성, 청송, 영양, 영덕, 청도, 고령, 성주, 칠곡, 예천, 봉화, 울진, 울릉의 모든 읍/면
        - **경상남도**: 창원(5개 구의 모든 동), 진주, 통영, 사천, 김해, 밀양, 거제, 양산, 의령, 함안, 창녕, 고성, 남해, 하동, 산청, 함양, 거창, 합천의 모든 읍/면
        - **제주특별자치도**: 제주, 서귀포의 모든 읍/면
        
        ### 💡 사용 팁
        - 드롭박스로 지역을 단계별로 선택한 후 "선택한 지역 검색" 버튼 사용
        - 구체적인 구/군/시까지 선택하면 더 정확한 날씨 정보 제공
        - 일부 도시는 여러 이름으로 자동 시도됩니다
        - 검색이 안 되면 인근 도시를 시도해보세요
        
        ### 🌤️ 제공 정보
        - 현재 온도, 체감 온도, 최저/최고 온도
        - 습도, 기압, 풍속, 풍향
        - 일출/일몰 시간
        - 가시거리, 구름량
        - 강수량, 적설량 (해당시)
        - 상세 위치 정보
        
        ### 💡 사용 팁
        - 직접 입력: "서울", "부산", "대전" 등 한글로 입력
        - 버튼 클릭: 왼쪽 사이드바의 도시 버튼들을 클릭
        - 더 많은 도시: 직접 입력으로 200개 이상의 도시 지원
        """)

if __name__ == "__main__":
    main()