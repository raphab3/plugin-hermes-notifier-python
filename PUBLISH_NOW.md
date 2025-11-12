# 🚀 Publicar Plugin Python no PyPI - AGORA!

> Build já está pronto! Arquivos gerados em `dist/`

---

## ✅ Status Atual

- ✅ Build concluído com sucesso
- ✅ Arquivos gerados:
  - `hermes_notifier-1.1.0-py3-none-any.whl` (21K)
  - `hermes_notifier-1.1.0.tar.gz` (23K)
- ✅ Verificação twine: **PASSED**

---

## 📦 Próximos Passos

### **Opção 1: Publicar no PyPI (Produção)** 🚀

```bash
# 1. Fazer upload
twine upload dist/*

# Vai pedir:
# Username: __token__
# Password: seu-token-do-pypi
```

**Como obter o token do PyPI**:
1. Acesse: https://pypi.org/manage/account/token/
2. Clique em "Add API token"
3. Nome: `hermes-notifier-upload`
4. Scope: "Entire account" (ou específico para o projeto)
5. Copie o token (começa com `pypi-AgE...`)

---

### **Opção 2: Testar no TestPyPI Primeiro** 🧪

```bash
# 1. Upload para TestPyPI
twine upload --repository testpypi dist/*

# Vai pedir:
# Username: __token__
# Password: seu-token-do-testpypi

# 2. Testar instalação
pip install --index-url https://test.pypi.org/simple/ hermes-notifier

# 3. Se funcionar, publicar no PyPI de verdade
twine upload dist/*
```

**Como obter o token do TestPyPI**:
1. Acesse: https://test.pypi.org/manage/account/token/
2. Siga os mesmos passos acima

---

## 🔐 Configurar Credenciais (Opcional)

Para não precisar digitar toda vez, crie `~/.pypirc`:

```bash
cat > ~/.pypirc << 'EOF'
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...SEU-TOKEN-AQUI...

[testpypi]
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZwI...SEU-TOKEN-AQUI...
EOF

chmod 600 ~/.pypirc
```

---

## 📝 Comandos Prontos

### **Publicar no PyPI**
```bash
twine upload dist/*
```

### **Publicar no TestPyPI**
```bash
twine upload --repository testpypi dist/*
```

### **Verificar publicação**
```bash
# PyPI
pip search hermes-notifier
# ou
curl https://pypi.org/pypi/hermes-notifier/json | jq .info.version

# TestPyPI
curl https://test.pypi.org/pypi/hermes-notifier/json | jq .info.version
```

### **Instalar após publicar**
```bash
# Do PyPI
pip install hermes-notifier

# Do TestPyPI
pip install --index-url https://test.pypi.org/simple/ hermes-notifier
```

---

## ⚠️ Importante

1. **Versão única**: Não é possível sobrescrever uma versão já publicada
2. **Token seguro**: Nunca compartilhe seu token do PyPI
3. **Teste primeiro**: Recomendo testar no TestPyPI antes
4. **README**: Certifique-se que o README.md está atualizado

---

## 🎯 Checklist Final

Antes de publicar:

- [x] Build concluído
- [x] Twine check passou
- [ ] Token do PyPI obtido
- [ ] README.md revisado
- [ ] CHANGELOG.md atualizado
- [ ] Versão correta (1.1.0)
- [ ] Decidir: TestPyPI ou PyPI direto?

---

## 🚀 Publicar AGORA!

**Recomendação**: Teste no TestPyPI primeiro

```bash
# 1. TestPyPI
twine upload --repository testpypi dist/*

# 2. Testar instalação
pip install --index-url https://test.pypi.org/simple/ hermes-notifier

# 3. Se OK, publicar no PyPI
twine upload dist/*
```

**Ou direto no PyPI** (se tiver certeza):

```bash
twine upload dist/*
```

---

## 📊 Após Publicação

1. **Verificar no PyPI**:
   - https://pypi.org/project/hermes-notifier/

2. **Testar instalação**:
   ```bash
   pip install hermes-notifier
   python -c "from hermes_notifier import HermesUnifiedClient; print('✅ OK')"
   ```

3. **Adicionar badge no README**:
   ```markdown
   [![PyPI version](https://badge.fury.io/py/hermes-notifier.svg)](https://pypi.org/project/hermes-notifier/)
   ```

4. **Criar release no GitHub**:
   - Tag: `v1.1.0`
   - Title: `v1.1.0 - Initial Release`
   - Anexar arquivos do `dist/`

---

## 🐛 Troubleshooting

### **Erro: "Invalid or non-existent authentication"**
- Verifique se está usando `__token__` como username
- Verifique se o token está correto

### **Erro: "File already exists"**
- Versão já foi publicada
- Incremente a versão no `setup.py` e faça novo build

### **Erro: "403 Forbidden"**
- Token sem permissões
- Crie um novo token com permissões corretas

---

**Pronto para publicar! 🎉**

Execute:
```bash
twine upload dist/*
```

