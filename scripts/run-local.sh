#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  ガス料金管理システム - ローカル開発${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check Python
echo -e "${YELLOW}[1/5] Python 環境を確認中...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 が見つかりません"
    exit 1
fi
echo -e "${GREEN}✓ Python3 OK${NC}"
echo ""

# Create venv
echo -e "${YELLOW}[2/5] 仮想環境を作成中...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ 仮想環境作成完了${NC}"
else
    echo -e "${GREEN}✓ 仮想環境は既に存在${NC}"
fi
source .venv/bin/activate
echo ""

# Install dependencies
echo -e "${YELLOW}[3/5] 依存パッケージをインストール中...${NC}"
pip install -q -r requirements.txt
echo -e "${GREEN}✓ インストール完了${NC}"
echo ""

# Database migration
echo -e "${YELLOW}[4/5] データベースをセットアップ中...${NC}"
python manage.py migrate --no-input > /dev/null 2>&1
python manage.py create_demo > /dev/null 2>&1
echo -e "${GREEN}✓ DB セットアップ完了${NC}"
echo ""

# Start server
echo -e "${YELLOW}[5/5] サーバーを起動中...${NC}"
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  起動完了！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📱 http://localhost:8000${NC}"
echo ""
echo -e "ログイン情報（デモユーザー）:"
echo -e "  ${BLUE}ユーザー: demo${NC}"
echo -e "  ${BLUE}パスワード: demo123${NC}"
echo ""
echo -e "停止: ${YELLOW}Ctrl+C${NC}"
echo ""

python manage.py runserver
