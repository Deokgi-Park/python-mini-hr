# Python Mini HR

파이썬 기반 개인용 인사 관리 시스템

## 기능

- ✅ 직원 목록 조회
- ✅ 직원 추가
- ✅ 직원 정보 수정
- ✅ 직원 상세 정보 조회
- ✅ 직원 삭제
- ✅ JSON 파일 기반 데이터 저장

## 기술 스택

- Python 3.x
- Flask 3.0.0 (웹 프레임워크)
- HTML/CSS (프론트엔드)

## 설치 및 실행

### 1. 가상환경 생성 (권장)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

```bash
# 일반 실행 (프로덕션 모드)
python app.py

# 개발 모드 (디버그 모드)
FLASK_DEBUG=1 python app.py
```

### 4. 브라우저에서 접속

웹 브라우저를 열고 다음 주소로 접속:
```
http://localhost:5000
```

## 프로젝트 구조

```
python-mini-hr/
├── app.py                 # 메인 애플리케이션 파일
├── requirements.txt       # Python 패키지 의존성
├── employees.json         # 직원 데이터 저장 파일 (자동 생성)
├── templates/             # HTML 템플릿
│   ├── base.html         # 기본 레이아웃
│   ├── index.html        # 직원 목록 페이지
│   ├── add_employee.html # 직원 추가 페이지
│   ├── edit_employee.html # 직원 수정 페이지
│   └── employee_detail.html # 직원 상세 페이지
└── static/               # 정적 파일
    └── css/
        └── style.css     # 스타일시트
```

## 사용 방법

1. **직원 추가**: 홈페이지에서 "직원 추가" 버튼 클릭
2. **직원 조회**: 직원 이름을 클릭하여 상세 정보 확인
3. **직원 수정**: 상세 페이지 또는 목록에서 "수정" 버튼 클릭
4. **직원 삭제**: 상세 페이지 또는 목록에서 "삭제" 버튼 클릭

## 주의사항

- 이 프로그램은 개인용/학습용으로 제작되었습니다.
- 데이터는 JSON 파일(`employees.json`)에 저장됩니다.
- 실제 운영 환경에서는 데이터베이스 사용을 권장합니다.
- `app.secret_key`는 실제 운영시 변경해야 합니다.

## 라이센스

개인용/학습용 프로젝트
