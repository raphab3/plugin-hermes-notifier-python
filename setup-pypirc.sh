#!/bin/bash
# Script para configurar ~/.pypirc com tokens do PyPI

echo "🔐 Configurar credenciais do PyPI"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Você precisa ter os tokens do PyPI e TestPyPI${NC}"
echo ""
echo "1. TestPyPI: https://test.pypi.org/manage/account/token/"
echo "2. PyPI: https://pypi.org/manage/account/token/"
echo ""

# Pedir token do TestPyPI
echo "Cole o token do TestPyPI (ou deixe em branco para pular):"
read -r TESTPYPI_TOKEN

# Pedir token do PyPI
echo ""
echo "Cole o token do PyPI (ou deixe em branco para pular):"
read -r PYPI_TOKEN

# Criar arquivo .pypirc
PYPIRC_FILE="$HOME/.pypirc"

echo "" > "$PYPIRC_FILE"

if [ -n "$PYPI_TOKEN" ]; then
    cat >> "$PYPIRC_FILE" << EOF
[pypi]
username = __token__
password = $PYPI_TOKEN

EOF
    echo -e "${GREEN}✅ Token do PyPI configurado${NC}"
fi

if [ -n "$TESTPYPI_TOKEN" ]; then
    cat >> "$PYPIRC_FILE" << EOF
[testpypi]
username = __token__
password = $TESTPYPI_TOKEN

EOF
    echo -e "${GREEN}✅ Token do TestPyPI configurado${NC}"
fi

# Definir permissões
chmod 600 "$PYPIRC_FILE"

echo ""
echo -e "${GREEN}✅ Arquivo ~/.pypirc criado com sucesso!${NC}"
echo ""
echo "Agora você pode usar:"
echo "  twine upload --repository testpypi dist/*"
echo "  twine upload dist/*"
echo ""
echo "Sem precisar digitar o token toda vez!"

