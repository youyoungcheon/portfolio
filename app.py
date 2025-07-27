from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
import os
import datetime
import logging
import secrets
from werkzeug.middleware.proxy_fix import ProxyFix

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 보안 설정
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_urlsafe(32))
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# CORS 설정 (필요한 도메인만 허용)
CORS(app, origins=os.environ.get('ALLOWED_ORIGINS', 'http://localhost:*').split(','))

# 프록시 헤더 처리 (nginx 뒤에서 실행될 때)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

# 환경 변수에서 설정 가져오기
PORT = int(os.environ.get('PORT', 5001))  # macOS AirPlay 충돌 방지
ENV = os.environ.get('ENVIRONMENT', 'development')
VERSION = os.environ.get('APP_VERSION', '1.0.0')

# 요청 로깅 미들웨어
@app.before_request
def log_request_info():
    if request.endpoint != 'health_check':  # 헬스체크는 로그에서 제외
        logger.info(f"Request: {request.method} {request.url} - IP: {request.remote_addr}")

@app.after_request
def after_request(response):
    # 보안 헤더 추가
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/')
def home():
    try:
        html_template = """
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CI/CD Demo App</title>
            <style>
                body { 
                    font-family: 'Arial', sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; 
                    text-align: center; 
                    padding: 50px;
                    margin: 0;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background: rgba(255,255,255,0.1);
                    padding: 40px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                }
                .status { 
                    background: #4CAF50; 
                    padding: 20px; 
                    border-radius: 10px; 
                    margin: 20px 0;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                }
                .info {
                    background: rgba(255,255,255,0.2);
                    padding: 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                }
                h1 { margin-bottom: 30px; font-size: 2.5em; }
                .badge {
                    display: inline-block;
                    background: #FF6B6B;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 0.8em;
                    margin: 5px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Jenkins CI/CD Demo</h1>
                <div class="status">
                    <h2>✅ 애플리케이션 정상 실행 중</h2>
                </div>
                <div class="info">
                    <p><strong>환경:</strong> <span class="badge">{{ environment }}</span></p>
                    <p><strong>배포 시간:</strong> {{ deploy_time }}</p>
                    <p><strong>버전:</strong> {{ version }}</p>
                </div>
                <div class="info">
                    <h3>🔧 CI/CD 파이프라인 기능</h3>
                    <ul style="text-align: left; max-width: 400px; margin: 0 auto;">
                        <li>GitHub 웹훅 자동 트리거</li>
                        <li>자동 테스트 실행</li>
                        <li>Docker 이미지 빌드</li>
                        <li>무중단 배포</li>
                        <li>Slack 알림 연동</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template, 
                                    environment=ENV,
                                    deploy_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    version=VERSION)
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    """헬스체크 엔드포인트"""
    try:
        # 추가 헬스체크 로직 (DB 연결, 외부 서비스 등)
        health_status = {
            'status': 'healthy',
            'environment': ENV,
            'timestamp': datetime.datetime.now().isoformat(),
            'version': VERSION,
            'uptime': 'N/A',  # 실제로는 시작 시간부터 계산
            'checks': {
                'database': 'healthy',  # 실제 DB 체크 로직 추가
                'external_api': 'healthy'  # 외부 API 체크 로직 추가
            }
        }
        return jsonify(health_status)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }), 503

@app.route('/api/status')
def api_status():
    """API 상태 확인"""
    try:
        return jsonify({
            'message': 'API is running successfully!',
            'environment': ENV,
            'port': PORT,
            'version': VERSION,
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"API status error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/test')
def test_endpoint():
    """테스트용 엔드포인트"""
    try:
        return jsonify({
            'test': 'success',
            'data': [1, 2, 3, 4, 5],
            'environment': ENV,
            'version': VERSION
        })
    except Exception as e:
        logger.error(f"Test endpoint error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(error):
    """404 에러 핸들러"""
    logger.warning(f"404 error: {request.url}")
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """500 에러 핸들러"""
    logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info(f"🚀 Starting application on port {PORT} in {ENV} environment")
    logger.info(f"Version: {VERSION}")
    
    # 개발 환경에서만 debug 모드 활성화
    debug_mode = (ENV == 'development')
    app.run(host='0.0.0.0', port=PORT, debug=debug_mode) 