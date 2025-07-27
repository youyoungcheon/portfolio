import pytest
import json
import os
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    """테스트 클라이언트 생성"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """홈페이지 테스트"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Jenkins CI/CD Demo' in response.data
    assert 'text/html' in response.content_type

def test_health_check(client):
    """헬스체크 엔드포인트 테스트"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'version' in data
    assert 'uptime' in data
    assert 'checks' in data
    assert data['checks']['database'] == 'healthy'
    assert data['checks']['external_api'] == 'healthy'

def test_api_status(client):
    """API 상태 엔드포인트 테스트"""
    response = client.get('/api/status')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['message'] == 'API is running successfully!'
    assert 'environment' in data
    assert 'port' in data
    assert 'timestamp' in data
    assert 'version' in data

def test_api_test_endpoint(client):
    """테스트 엔드포인트 검증"""
    response = client.get('/api/test')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['test'] == 'success'
    assert data['data'] == [1, 2, 3, 4, 5]
    assert 'environment' in data
    assert 'version' in data

def test_invalid_endpoint(client):
    """존재하지 않는 엔드포인트 테스트"""
    response = client.get('/invalid-endpoint')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['error'] == 'Not found'

def test_json_response_format(client):
    """JSON 응답 형식 검증"""
    endpoints = ['/health', '/api/status', '/api/test']
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        # JSON 파싱이 정상적으로 되는지 확인
        try:
            json.loads(response.data)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON response from {endpoint}")

def test_security_headers(client):
    """보안 헤더 테스트"""
    response = client.get('/')
    
    # 보안 헤더 확인
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('X-Frame-Options') == 'DENY'
    assert response.headers.get('X-XSS-Protection') == '1; mode=block'
    assert 'Strict-Transport-Security' in response.headers
    assert 'Content-Security-Policy' in response.headers

def test_cors_headers(client):
    """CORS 헤더 테스트"""
    response = client.options('/api/status')
    # CORS 설정이 제대로 되어있는지 확인
    assert response.status_code in [200, 204]

@patch('app.logger')
def test_error_logging(mock_logger, client):
    """에러 로깅 테스트"""
    # 존재하지 않는 엔드포인트 호출
    client.get('/invalid-endpoint')
    
    # 로거가 호출되었는지 확인
    mock_logger.warning.assert_called()

def test_health_check_unhealthy_scenario(client):
    """헬스체크 실패 시나리오 테스트"""
    with patch('app.datetime') as mock_datetime:
        # datetime에서 예외 발생시키기
        mock_datetime.datetime.now.side_effect = Exception("Time service unavailable")
        
        response = client.get('/health')
        assert response.status_code == 503
        
        data = json.loads(response.data)
        assert data['status'] == 'unhealthy'
        assert 'error' in data

class TestApplicationConfiguration:
    """애플리케이션 설정 테스트"""
    
    def test_app_exists(self):
        """앱 인스턴스 존재 확인"""
        assert app is not None
    
    def test_app_is_flask_instance(self):
        """Flask 인스턴스 확인"""
        from flask import Flask
        assert isinstance(app, Flask)
    
    def test_secret_key_configured(self):
        """SECRET_KEY 설정 확인"""
        assert app.config.get('SECRET_KEY') is not None
    
    def test_security_config(self):
        """보안 설정 확인"""
        assert app.config.get('SESSION_COOKIE_SECURE') is True
        assert app.config.get('SESSION_COOKIE_HTTPONLY') is True
        assert app.config.get('SESSION_COOKIE_SAMESITE') == 'Lax'

class TestEnvironmentVariables:
    """환경 변수 테스트"""
    
    def test_environment_variable_handling(self, client, monkeypatch):
        """환경 변수 처리 테스트"""
        # 환경 변수 설정
        monkeypatch.setenv('ENVIRONMENT', 'testing')
        monkeypatch.setenv('APP_VERSION', '2.0.0')
        
        response = client.get('/api/status')
        data = json.loads(response.data)
        
        # 환경 변수가 제대로 반영되는지 확인
        assert 'environment' in data
        assert 'version' in data
    
    def test_default_port_configuration(self, monkeypatch):
        """기본 포트 설정 테스트"""
        monkeypatch.delenv('PORT', raising=False)
        
        # app 모듈을 다시 임포트해서 기본값 확인
        import importlib
        import app as app_module
        importlib.reload(app_module)
        
        assert app_module.PORT == 5001  # macOS AirPlay 충돌 방지

class TestRateLimiting:
    """레이트 리미팅 테스트 (향후 구현 시)"""
    
    def test_api_rate_limiting(self, client):
        """API 레이트 리미팅 테스트"""
        # 현재는 구현되지 않았지만, 향후 구현 시 테스트 추가
        pass

class TestPerformance:
    """성능 테스트"""
    
    def test_response_time(self, client):
        """응답 시간 테스트"""
        import time
        
        start_time = time.time()
        response = client.get('/health')
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 1.0  # 1초 이내 응답
        assert response.status_code == 200 