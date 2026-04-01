# 🚗 AI Used Car Recommender

사용자의 예산과 희망 옵션을 기반으로 AI가 중고차 데이터를 분석하여 최적의 차량을 추천하는 서비스입니다.

---

## 📌 프로젝트 개요

- 사용자 조건(예산, 연식, 옵션 등)을 입력받아 크롤링한 중고차 데이터를 분석
- RAG 기반 AI 추천 로직을 통해 가장 적합한 차량을 점수화하여 반환

🪄 단순 필터링이 아닌, 데이터 기반 AI 추천을 목표로 설계되었습니다.

---

## 🏗️ 시스템 아키텍처

<img width="665" height="584" alt="image" src="https://github.com/user-attachments/assets/ea676292-c672-4491-95ff-7877f3764598" />


---

## 🛠️ 기술 스택

- FastAPI
- LangChain
- LangGraph
- RAG (Retrieval-Augmented Generation)
- Elasticsearch
- PostgreSQL
- Redis
- Pandas
- Docker
- AWS
- GitHub Actions

---

## 📂 프로젝트 구조

app/<br/>
├── api/<br/>
│     └── recommend.py        # Router (Entry Point)<br/>
│<br/>
├── services/<br/>
│     ├── recommendation_service.py<br/>
│     ├── car_logic.py<br/>
│     └── llm_service.py<br/>
│<br/>
├── repositories/<br/>
│     └── car_repository.py<br/>
│<br/>
├── schemas/<br/>
│     ├── request.py<br/>
│     └── response.py<br/>
│<br/>
├── db/<br/>
│     └── dummy_data.py<br/>
│<br/>
└── main.py<br/>
docker/<br/>
frontend/

---

## 🚀 실행 방법

### 1. 로컬 실행

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Docker 실행

```bash
docker-compose up --build
```

---

### 📊 핵심 기능

- 조건 기반 차량 추천
- AI 점수 기반 정렬
- Elasticsearch 기반 검색
- 추천 결과 캐싱
- 크롤링 자동화 파이프라인

---

### 🎯 기술적 도전 과제

- 차량 옵션 텍스트 정규화
- 성능기록부 데이터 해석
- 정형/비정형 데이터 결합 추천
- 추천 점수 설계

---
