# 🚗 AI Used Car Recommender

사용자의 예산과 희망 옵션을 기반으로 AI가 중고차 데이터를 분석하여 최적의 차량을 추천하는 서비스입니다.

---

## 📌 프로젝트 개요

- 사용자 조건(예산, 연식, 옵션 등)을 입력받아 크롤링한 중고차 데이터를 분석
- RAG 기반 AI 추천 로직을 통해 가장 적합한 차량을 점수화하여 반환

🪄 단순 필터링이 아닌, 데이터 기반 AI 추천을 목표로 설계되었습니다.

---

## 🏗️ 시스템 아키텍처

[ User ]
   ↓
FastAPI Backend
   ↓
Recommendation Engine (LangChain + RAG)
   ↓
PostgreSQL / Elasticsearch / Redis
   ↓
Crawler Pipeline

---

## 🛠️ 기술 스택

### Backend
- FastAPI

**선택 이유**
- 비동기 지원이 뛰어나 AI/ML 서비스에 적합

---

### AI / Recommendation
- LangChain
- LangGraph
- RAG (Retrieval-Augmented Generation)

**선택 이유**
- 단순 규칙 기반 추천이 아닌 문맥 기반 추론 가능
- 확장 가능한 AI 파이프라인 설계 가능

---

### Search & Retrieval
- Elasticsearch

**선택 이유**
- 차량 옵션, 설명, 성능기록부 등 비정형 데이터 검색 최적화
- RAG와 자연스럽게 연결 가능

---

### Database
- PostgreSQL
- Redis

**선택 이유**
- PostgreSQL: 정형 데이터 관리
- Redis: 캐싱 및 추천 응답 속도 개선

---

### Data Processing
- Pandas

**선택 이유**
- 차량 스펙 및 가격 데이터 전처리에 적합

---

### Infrastructure
- Docker
- AWS
- GitHub Actions

**선택 이유**
- 재현 가능한 개발 환경
- CI/CD 자동화
- 확장 가능한 배포 구조

---

## 📂 프로젝트 구조

backend/
├─ api/
├─ services/
├─ models/
crawler/
rag/
docker/

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

### 📈 향후 개선 방향

- 사용자 피드백 기반 추천 개선
- 실시간 가격 변동 반영
- 개인화 추천 모델 고도화
- 추천 설명(Explainable AI) 추가