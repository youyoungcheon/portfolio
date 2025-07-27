pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'cicd-demo-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_REGISTRY = 'your-registry.com'  // 실제 레지스트리로 변경
        SLACK_CHANNEL = '#deployments'
        DEPLOY_SERVER = 'your-server.com'      // 실제 서버로 변경
        DEPLOY_USER = 'deploy'
    }
    
    tools {
        // Jenkins에 설정된 도구들
        python 'Python-3.9'
        docker 'Docker'
    }
    
    stages {
        stage('🔍 Checkout') {
            steps {
                echo '📥 소스코드 체크아웃 시작'
                checkout scm
                
                script {
                    // Git 정보 수집
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.GIT_AUTHOR = sh(
                        script: 'git log -1 --pretty=format:"%an"',
                        returnStdout: true
                    ).trim()
                    env.GIT_MESSAGE = sh(
                        script: 'git log -1 --pretty=format:"%s"',
                        returnStdout: true
                    ).trim()
                }
                
                echo "✅ 커밋: ${env.GIT_COMMIT_SHORT}"
                echo "✅ 작성자: ${env.GIT_AUTHOR}"
                echo "✅ 메시지: ${env.GIT_MESSAGE}"
            }
        }
        
        stage('🏗️ Setup Environment') {
            steps {
                echo '🔧 Python 환경 설정'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('🧪 Run Tests') {
            steps {
                echo '🧪 테스트 실행 시작'
                sh '''
                    . venv/bin/activate
                    
                    # 테스트 실행 및 커버리지 리포트 생성
                    pytest test_app.py -v --junitxml=test-results.xml --cov=app --cov-report=xml --cov-report=html
                    
                    echo "✅ 테스트 완료"
                '''
            }
            
            post {
                always {
                    // 테스트 결과 아카이브
                    junit 'test-results.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('🐳 Build Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                    branch 'release/*'
                }
            }
            steps {
                echo '🐳 Docker 이미지 빌드 시작'
                script {
                    // Docker 이미지 빌드
                    def image = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    
                    // latest 태그도 추가
                    if (env.BRANCH_NAME == 'main') {
                        image.tag('latest')
                    }
                    
                    // 이미지 정보 출력
                    sh "docker images ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
        
        stage('🔍 Security Scan') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                echo '🔍 보안 스캔 실행'
                sh '''
                    # Docker 이미지 보안 스캔 (예시)
                    echo "보안 스캔 시뮬레이션..."
                    sleep 2
                    echo "✅ 보안 스캔 완료 - 취약점 없음"
                '''
            }
        }
        
        stage('📤 Push to Registry') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                echo '📤 Docker 레지스트리에 이미지 푸시'
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                        def image = docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}")
                        image.push()
                        
                        if (env.BRANCH_NAME == 'main') {
                            image.push('latest')
                        }
                    }
                }
            }
        }
        
        stage('🚀 Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo '🚀 스테이징 환경 배포'
                sh '''
                    # 스테이징 서버에 배포
                    ./scripts/deploy.sh staging ${DOCKER_TAG}
                '''
            }
        }
        
        stage('🎯 Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                echo '🎯 프로덕션 배포 승인 대기'
                
                // 수동 승인 단계
                input message: '프로덕션에 배포하시겠습니까?', 
                      ok: '배포 진행',
                      parameters: [
                          choice(name: 'DEPLOYMENT_STRATEGY', 
                                 choices: ['rolling', 'blue-green'], 
                                 description: '배포 전략 선택')
                      ]
                
                echo '🎯 프로덕션 환경 배포 시작'
                sh '''
                    ./scripts/deploy.sh production ${DOCKER_TAG} ${DEPLOYMENT_STRATEGY}
                '''
            }
        }
        
        stage('✅ Health Check') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                echo '✅ 배포된 애플리케이션 헬스체크'
                sh '''
                    # 헬스체크 스크립트 실행
                    ./scripts/health-check.sh ${DEPLOY_SERVER}
                '''
            }
        }
    }
    
    post {
        always {
            echo '🧹 워크스페이스 정리'
            
            // Docker 이미지 정리 (로컬)
            sh '''
                docker image prune -f
                docker container prune -f
            '''
        }
        
        success {
            echo '🎉 파이프라인 성공!'
            
            // Slack 알림 - 성공
            slackSend(
                channel: "${SLACK_CHANNEL}",
                color: 'good',
                message: """
✅ *배포 성공* 
• *프로젝트*: ${env.JOB_NAME}
• *브랜치*: ${env.BRANCH_NAME}
• *빌드*: #${env.BUILD_NUMBER}
• *커밋*: ${env.GIT_COMMIT_SHORT}
• *작성자*: ${env.GIT_AUTHOR}
• *메시지*: ${env.GIT_MESSAGE}
• *소요시간*: ${currentBuild.durationString}
                """.stripIndent()
            )
        }
        
        failure {
            echo '❌ 파이프라인 실패!'
            
            // Slack 알림 - 실패
            slackSend(
                channel: "${SLACK_CHANNEL}",
                color: 'danger',
                message: """
❌ *배포 실패*
• *프로젝트*: ${env.JOB_NAME}
• *브랜치*: ${env.BRANCH_NAME}
• *빌드*: #${env.BUILD_NUMBER}
• *커밋*: ${env.GIT_COMMIT_SHORT}
• *작성자*: ${env.GIT_AUTHOR}
• *실패 단계*: ${env.STAGE_NAME}
• *로그*: ${env.BUILD_URL}console
                """.stripIndent()
            )
        }
        
        unstable {
            echo '⚠️ 파이프라인 불안정!'
            
            // Slack 알림 - 불안정
            slackSend(
                channel: "${SLACK_CHANNEL}",
                color: 'warning',
                message: """
⚠️ *빌드 불안정*
• *프로젝트*: ${env.JOB_NAME}
• *브랜치*: ${env.BRANCH_NAME}
• *빌드*: #${env.BUILD_NUMBER}
• *테스트 결과를 확인해주세요*: ${env.BUILD_URL}
                """.stripIndent()
            )
        }
    }
} 