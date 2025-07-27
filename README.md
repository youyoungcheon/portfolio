# 🚀 Jenkins 기반 CI/CD 자동화 파이프라인

완전한 CI/CD 파이프라인을 Jenkins로 구현한 포트폴리오 프로젝트입니다.

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Jenkins-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Python](https://img.shields.io/badge/Python-3.9-green)
![Testing](https://img.shields.io/badge/Testing-Pytest-yellow)

## 📋 프로젝트 개요

### 🎯 목적
개발자가 코드 변경(push) 시 자동으로 테스트, 빌드, 배포가 일어나는 완전한 CI/CD 파이프라인을 구축합니다.

### 🛠️ 사용 기술 스택
- **CI/CD**: Jenkins
- **언어**: Python 3.9
- **프레임워크**: Flask
- **테스팅**: Pytest, Coverage
- **컨테이너**: Docker, Docker Compose
- **웹서버**: Nginx (리버스 프록시)
- **알림**: Slack
- **배포**: SSH, systemd

## 🏗️ 아키텍처

```
GitHub Repository
        ↓
    Jenkins Webhook
        ↓
┌─────────────────────┐
│   Jenkins Pipeline  │
│ ┌─────────────────┐ │
│ │ 1. Checkout     │ │
│ │ 2. Test         │ │
│ │ 3. Build Docker │ │
│ │ 4. Security Scan│ │
│ │ 5. Push Registry│ │
│ │ 6. Deploy       │ │
│ │ 7. Health Check │ │
│ └─────────────────┘ │
└─────────────────────┘
        ↓
    Production Server
        ↓
      Slack 알림
```

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/jenkins-cicd-pipeline.git
cd jenkins-cicd-pipeline
```

### 2. 로컬 개발 환경 실행
```bash
# Docker Compose로 실행
docker-compose up -d

# 또는 Python 가상환경으로 실행
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 3. 애플리케이션 확인
- **웹 애플리케이션**: http://localhost:5001
- **헬스체크**: http://localhost:5001/health
- **API 상태**: http://localhost:5001/api/status

## 🧪 테스트 실행

```bash
# 가상환경 활성화
source venv/bin/activate

# 테스트 실행
pytest test_app.py -v

# 커버리지 포함 테스트
pytest test_app.py -v --cov=app --cov-report=html
```

## 🐳 Docker 빌드 및 실행

```bash
# Docker 이미지 빌드
docker build -t cicd-demo-app:latest .

# 컨테이너 실행
docker run -d \
  --name demo-app \
  -p 5001:5001 \
  -e ENVIRONMENT=production \
  cicd-demo-app:latest

# 헬스체크
curl http://localhost:5001/health
```

## 🔧 Jenkins 설정

### 1. 필수 플러그인 설치
- Pipeline
- Docker Pipeline
- GitHub Integration
- Slack Notification
- HTML Publisher

### 2. Jenkins Pipeline 설정
1. **New Item** → **Pipeline** 선택
2. **Pipeline** → **Pipeline script from SCM** 선택
3. **Repository URL** 입력
4. **Script Path**: `Jenkinsfile`

### 3. 환경 변수 설정
Jenkins 시스템 설정에서 다음 환경 변수들을 설정하세요:

```
DOCKER_REGISTRY=your-registry.com
SLACK_CHANNEL=#deployments
DEPLOY_SERVER=your-server.com
```

### 4. 필수 Credentials 추가
- `docker-registry-credentials`: Docker 레지스트리 접근
- `ssh-credentials`: 배포 서버 SSH 키
- `slack-token`: Slack 봇 토큰

## 🚢 배포 설정

### 1. 배포 서버 준비
```bash
# deploy 사용자 생성
sudo useradd -m -s /bin/bash deploy
sudo usermod -aG docker deploy

# SSH 키 설정
mkdir -p /home/deploy/.ssh
cat >> /home/deploy/.ssh/authorized_keys << EOF
# Jenkins 공개키 추가
EOF

# 권한 설정
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /home/deploy/.ssh
```

### 2. 배포 스크립트 권한 설정
```bash
# 스크립트 실행 권한 부여
chmod +x scripts/*.sh
```

### 3. 수동 배포 실행
```bash
# 스테이징 환경 배포
./scripts/deploy.sh staging 123

# 프로덕션 환경 배포 (Blue-Green)
./scripts/deploy.sh production 123 blue-green
```

## 📊 CI/CD 파이프라인 상세

### Stage 1: 🔍 Checkout
- Git 저장소에서 소스코드 체크아웃
- Git 커밋 정보 수집 (작성자, 메시지, 해시)

### Stage 2: 🏗️ Setup Environment
- Python 가상환경 생성
- 의존성 패키지 설치

### Stage 3: 🧪 Run Tests
- Pytest로 단위 테스트 실행
- 코드 커버리지 측정
- 테스트 결과 및 커버리지 리포트 생성

### Stage 4: 🐳 Build Docker Image
- Docker 이미지 빌드
- 태그 관리 (latest, build-number)
- 이미지 정보 출력

### Stage 5: 🔍 Security Scan
- Docker 이미지 보안 스캔
- 취약점 검사

### Stage 6: 📤 Push to Registry
- Docker 레지스트리에 이미지 푸시
- 버전별 태그 관리

### Stage 7: 🚀 Deploy
- **Staging**: develop 브랜치 자동 배포
- **Production**: main 브랜치 수동 승인 후 배포
- 배포 전략 선택 (Rolling/Blue-Green)

### Stage 8: ✅ Health Check
- 배포된 애플리케이션 헬스체크
- API 엔드포인트 검증
- 응답 시간 측정

## 📱 Slack 알림

파이프라인 실행 결과를 Slack으로 알림받을 수 있습니다:

### 성공 알림 📢
```
✅ 배포 성공
• 프로젝트: demo-app
• 브랜치: main
• 빌드: #123
• 커밋: abc123
• 작성자: developer
• 소요시간: 5m 30s
```

### 실패 알림 ⚠️
```
❌ 배포 실패
• 프로젝트: demo-app
• 브랜치: main
• 빌드: #124
• 실패 단계: Run Tests
• 로그: [링크]
```

## 📈 모니터링 및 로깅

### Jenkins 빌드 로그
- 각 단계별 상세 실행 로그
- 테스트 결과 및 커버리지 리포트
- Docker 빌드 로그

### 애플리케이션 로그
```bash
# 컨테이너 로그 확인
docker logs demo-app

# nginx 로그 확인
docker-compose logs nginx
```

### 헬스체크 모니터링
```bash
# 헬스체크 실행
./scripts/health-check.sh localhost 5000

# 지속적인 모니터링
watch -n 30 "curl -s http://localhost:5000/health | jq"
```

## 🔒 보안 고려사항

### Docker 보안
- 비특권 사용자로 컨테이너 실행
- 최소한의 권한으로 이미지 빌드
- 보안 스캔 단계 포함

### SSH 보안
- SSH 키 기반 인증
- 포트 제한 및 방화벽 설정

### Nginx 보안
- 보안 헤더 설정
- 레이트 리미팅
- 접근 로그 모니터링

## 🛠️ 트러블슈팅

### 일반적인 문제들

#### 1. Docker 권한 에러
```bash
sudo usermod -aG docker $USER
newgrp docker
```

#### 2. Jenkins Pipeline 실패
- 플러그인 설치 확인
- Credentials 설정 확인
- 환경 변수 설정 확인

#### 3. 배포 실패
```bash
# SSH 연결 테스트
ssh deploy@your-server.com

# Docker 이미지 확인
docker images | grep cicd-demo-app

# 헬스체크 수동 실행
./scripts/health-check.sh your-server.com
```

## 📚 추가 학습 자료

- [Jenkins 공식 문서](https://www.jenkins.io/doc/)
- [Docker 가이드](https://docs.docker.com/)
- [Flask 문서](https://flask.palletsprojects.com/)
- [Pytest 가이드](https://docs.pytest.org/)

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 제작자

**당신의 이름**
- GitHub: [@your-username](https://github.com/your-username)
- Email: your.email@example.com

---

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요! 