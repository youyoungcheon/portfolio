from flask import Flask, jsonify
import os
import datetime

app = Flask(__name__)

# 환경 변수에서 설정 가져오기
PORT = int(os.environ.get('PORT', 5001))
ENV = os.environ.get('ENVIRONMENT', 'development')
VERSION = os.environ.get('APP_VERSION', '1.0.0')

@app.route('/')
def home():
    return jsonify({
        'message': 'Simple CI/CD Demo App',
        'environment': ENV,
        'version': VERSION,
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """헬스체크 엔드포인트"""
    return jsonify({
        'status': 'healthy',
        'environment': ENV,
        'timestamp': datetime.datetime.now().isoformat(),
        'version': VERSION
    })

@app.route('/api/status')
def api_status():
    """API 상태 확인"""
    return jsonify({
        'message': 'API is running successfully!',
        'environment': ENV,
        'port': PORT,
        'version': VERSION,
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    print(f"🚀 Starting simple app on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True) 