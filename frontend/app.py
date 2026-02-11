import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/v1/recommend"

st.set_page_config(page_title="AI Used Car Recommender", layout="centered")

st.title("🚗 AI Used Car Recommender")

st.markdown("조건을 입력하면 AI가 적합한 차량을 추천합니다.")

# 입력 폼
budget = st.number_input("예산 (만원)", min_value=500, max_value=10000, value=2000)
min_year = st.number_input("최소 연식", min_value=2000, max_value=2025, value=2020)
preferred_options = st.text_input("선호 옵션 (쉼표로 구분)", "navigation")

if st.button("추천 받기"):
    option_list = [opt.strip() for opt in preferred_options.split(",") if opt.strip()]

    payload = {
        "budget": budget,
        "min_year": min_year,
        "preferred_options": option_list,
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            results = response.json()["results"]

            st.success("추천 결과")

            for car in results:
                with st.container():
                    st.subheader(car["model"])
                    st.write(f"💰 가격: {car['price']} 만원")
                    st.write(f"📅 연식: {car['year']}")
                    st.write(f"⭐ 점수: {car['score']}")
                    st.write(f"옵션: {', '.join(car['options'])}")
                    st.divider()

        else:
            st.error("API 호출 실패")

    except Exception as e:
        st.error(f"서버 연결 실패: {e}")
