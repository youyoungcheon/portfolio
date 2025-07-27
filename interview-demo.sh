#!/bin/bash

# 🎯 면접 시연 메인 메뉴
# 사용법: ./interview-demo.sh

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# 헤더
clear
echo -e "${PURPLE}${BOLD}"
echo "🎯 =================================================="
echo "    Jenkins CI/CD 포트폴리오 면접 시연"
echo "=================================================="
echo -e "${NC}"

echo -e "${CYAN}"
echo "📋 프로젝트 개요:"
echo "  🚀 Jenkins 기반 완전 자동화 CI/CD 파이프라인"
echo "  🐳 Docker 컨테이너 기반 배포"
echo "  🧪 94% 커버리지 자동화 테스트"
echo "  🔒 프로덕션급 보안 구현"
echo "  📊 실시간 모니터링 & 로깅"
echo -e "${NC}"

echo
echo -e "${YELLOW}어떤 시연을 진행하시겠습니까?${NC}"
echo

echo -e "${GREEN}1.${NC} 🚀 빠른 시연 (5분) - 전체 기능 개요"
echo -e "${GREEN}2.${NC} 🎨 상세 시연 (10분) - 기술적 깊이"
echo -e "${GREEN}3.${NC} 🛠️ 문제 해결 시연 - 트러블슈팅 능력"
echo -e "${GREEN}4.${NC} ⚙️ 환경 준비 - 시연 전 사전 셋업"
echo -e "${GREEN}5.${NC} 🧹 환경 정리 - 시연 후 클린업"
echo
echo -e "${BLUE}0.${NC} 📚 도움말 - 각 시연별 상세 설명"
echo -e "${RED}q.${NC} 종료"

echo
echo -n -e "${BOLD}선택하세요 (1-5, 0, q): ${NC}"
read choice

case $choice in
    1)
        echo -e "${GREEN}🚀 5분 빠른 시연을 시작합니다!${NC}"
        echo -e "${YELLOW}💡 팁: 면접관에게 전체적인 시스템 개요를 보여주는 시연입니다${NC}"
        echo
        read -p "계속하려면 Enter를 누르세요..."
        ./scripts/demo-quick.sh
        ;;
    2)
        echo -e "${CYAN}🎨 상세 기술 시연을 시작합니다!${NC}"
        echo -e "${YELLOW}💡 팁: 기술적 깊이와 실력을 어필하는 시연입니다${NC}"
        echo
        read -p "계속하려면 Enter를 누르세요..."
        ./scripts/demo-detailed.sh
        ;;
    3)
        echo -e "${RED}🛠️ 문제 해결 시연을 시작합니다!${NC}"
        echo -e "${YELLOW}💡 팁: 실무 능력과 문제 해결 역량을 보여주는 시연입니다${NC}"
        echo
        read -p "계속하려면 Enter를 누르세요..."
        ./scripts/demo-troubleshoot.sh
        ;;
    4)
        echo -e "${BLUE}⚙️ 환경 준비를 시작합니다!${NC}"
        echo -e "${YELLOW}💡 팁: 시연 전에 반드시 실행해주세요${NC}"
        echo
        ./scripts/demo-setup.sh
        ;;
    5)
        echo -e "${PURPLE}🧹 환경 정리를 시작합니다!${NC}"
        echo -e "${YELLOW}💡 팁: 시연 후 시스템을 깨끗하게 정리합니다${NC}"
        echo
        ./scripts/demo-cleanup.sh
        ;;
    0)
        echo -e "${BLUE}📚 시연별 상세 설명${NC}"
        echo
        echo -e "${GREEN}🚀 5분 빠른 시연:${NC}"
        echo "  - 전체 CI/CD 파이프라인 개요"
        echo "  - 웹 앱 실행 → 테스트 → Docker 빌드 → 배포"
        echo "  - 면접 초반에 전체적인 인상을 주고 싶을 때 사용"
        echo
        echo -e "${CYAN}🎨 상세 기술 시연:${NC}"
        echo "  - 보안, 모니터링, API 설계 등 기술적 깊이"
        echo "  - docker-compose, nginx, 성능 테스트 포함"
        echo "  - 기술 면접에서 깊이 있는 토론을 원할 때 사용"
        echo
        echo -e "${RED}🛠️ 문제 해결 시연:${NC}"
        echo "  - 테스트 실패, 서비스 다운, 포트 충돌 등"
        echo "  - 실제 운영 경험과 문제 해결 능력 어필"
        echo "  - 실무 경험에 대한 질문이 나올 때 사용"
        echo
        echo -e "${YELLOW}📋 추천 시연 순서:${NC}"
        echo "  1. 환경 준비 (demo-setup.sh)"
        echo "  2. 빠른 시연 (5분) 또는 상세 시연 (10분)"
        echo "  3. 질문에 따라 문제 해결 시연 추가"
        echo "  4. 환경 정리 (demo-cleanup.sh)"
        echo
        read -p "메인 메뉴로 돌아가려면 Enter를 누르세요..."
        exec $0
        ;;
    q|Q)
        echo -e "${GREEN}면접 성공을 기원합니다! 🍀${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}잘못된 선택입니다. 다시 선택해주세요.${NC}"
        sleep 2
        exec $0
        ;;
esac

echo
echo -e "${PURPLE}시연이 완료되었습니다!${NC}"
echo -e "${YELLOW}다른 시연을 하려면: ./interview-demo.sh${NC}"
echo -e "${GREEN}환경 정리가 필요하면: ./scripts/demo-cleanup.sh${NC}" 