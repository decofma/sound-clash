#!/bin/bash

# 1. Atualiza o pip
pip install --upgrade pip

# 2. Instala as dependências normalmente
pip install -r requirements.txt

# 3. Inicia a limpeza para reduzir o tamanho final
echo "Starting cleanup to reduce slug size..."

# Remove caches do pip e do poetry
rm -rf /root/.cache/pip
rm -rf /root/.pypoetry/cache

# Encontra a pasta onde os pacotes foram instalados e entra nela
# O caminho pode variar, mas geralmente é algo como /var/lang/lib/python3.9/site-packages
# Usamos um truque para encontrar o caminho do streamlit e usar como base
SITE_PACKAGES=$(python -c 'import os, streamlit; print(os.path.dirname(streamlit.__file__))')
echo "Site-packages found at: $SITE_PACKAGES"

# Apaga as pastas __pycache__ e arquivos .pyc
find $SITE_PACKAGES -type d -name "__pycache__" -exec rm -rf {} +
find $SITE_PACKAGES -type f -name "*.pyc" -delete

# Apaga pastas de testes, que são pesadas e desnecessárias para rodar o app
find $SITE_PACKAGES -type d -name "tests" -exec rm -rf {} +
find $SITE_PACKAGES -type d -name "test" -exec rm -rf {} +

# Apaga arquivos de documentação e exemplos que não são código
find $SITE_PACKAGES -type f -name "*.md" -delete
find $SITE_PACKAGES -type f -name "*.rst" -delete
find $SITE_PACKAGES -type f -name "*.txt" -delete

echo "Cleanup finished."