# WineNow - 와인 시음 노트 관리

![Django](https://img.shields.io/badge/Django-v5.1.4-green) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![License](https://img.shields.io/badge/license-MIT-green)

와인 애호가들을 위한 시음 노트 관리 웹 애플리케이션입니다. 와인 정보를 기록하고, 시음 노트를 작성하며, 개인화된 와인 취향을 관리할 수 있습니다.

---

## 주요 기능

1. **회원 관리**
   - 회원가입, 로그인 및 프로필 관리
   - 소셜 로그인(Google, Kakao) 지원

2. **시음 노트**
   - 와인 시음 노트 작성, 수정 및 삭제
   - 와인 이름, 종류, 빈티지, 평가 및 이미지 업로드 지원
   - 시음 노트 검색 및 필터링 (와인 종류, 국가 등)

3. **캘린더 기능**
   - 시음 날짜별로 노트를 관리
   - 달력에 기록된 노트 개수와 간략 정보 표시

4. **와인 취향 관리**
   - 개인화된 선호 와인 정보 및 가격대 관리

5. **알림 기능**
   - 이벤트나 시음 스케줄 알림

---

## 기술 스택

- **백엔드**: Django, Django REST Framework
- **데이터베이스**: SQLite3 (개발, 배포)
- **기타 도구**:
  - Python Poetry (패키지 관리)
  - GitHub Actions (CI/CD)
  - AWS EC2 (배포)
  - Taggit (태그 관리)

---
