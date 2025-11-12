# 🔐 Guia: Criar Conta e Token no PyPI

> Passo a passo completo para criar conta e obter token de API

---

## 📋 Resumo

Sim, você precisa criar conta no PyPI (similar ao NPM para JavaScript)!

- **TestPyPI**: Para testes (https://test.pypi.org)
- **PyPI**: Para produção (https://pypi.org)

---

## 🚀 Passo a Passo - TestPyPI (Recomendado Primeiro)

### **1. Criar Conta**

1. Abra: https://test.pypi.org/account/register/
2. Preencha:
   - **Username**: `raphab3` (ou outro)
   - **Email**: `raphab33@hotmail.com`
   - **Password**: Escolha uma senha forte
3. Marque "I agree to the Terms of Use"
4. Clique em "Create account"
5. **Verifique seu email** e clique no link de confirmação

### **2. Fazer Login**

1. Acesse: https://test.pypi.org/account/login/
2. Digite username e password
3. Faça login

### **3. Criar Token de API**

1. Após login, acesse: https://test.pypi.org/manage/account/token/
2. Clique em **"Add API token"**
3. Preencha:
   - **Token name**: `hermes-notifier-upload`
   - **Scope**: Selecione "Entire account (all projects)"
4. Clique em **"Add token"**
5. **⚠️ IMPORTANTE**: Copie o token AGORA!
   - Formato: `pypi-AgENdGVzdC5weXBpLm9yZwI...`
   - Ele só aparece uma vez!
   - Salve em um lugar seguro

### **4. Usar o Token**

Quando executar:
```bash
twine upload --repository testpypi dist/*
```

Vai pedir:
```
Enter your API token: 
```

**Cole o token completo** que você copiou.

---

## 🎯 Passo a Passo - PyPI (Produção)

### **1. Criar Conta**

1. Abra: https://pypi.org/account/register/
2. Mesmo processo do TestPyPI
3. **Use o mesmo username** para facilitar

### **2. Criar Token**

1. Após login, acesse: https://pypi.org/manage/account/token/
2. Mesmo processo do TestPyPI
3. **Copie e salve o token**

---

## 💾 Configurar Credenciais (Opcional)

Para não precisar digitar o token toda vez:

### **Opção 1: Script Automático**

```bash
./setup-pypirc.sh
```

Vai pedir os tokens e criar o arquivo `~/.pypirc` automaticamente.

### **Opção 2: Manual**

Criar arquivo `~/.pypirc`:

```bash
nano ~/.pypirc
```

Conteúdo:
```ini
[testpypi]
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZwI...SEU-TOKEN-TESTPYPI...

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...SEU-TOKEN-PYPI...
```

Salvar e definir permissões:
```bash
chmod 600 ~/.pypirc
```

---

## 🧪 Testar Publicação

### **1. Publicar no TestPyPI**

```bash
twine upload --repository testpypi dist/*
```

Se configurou `~/.pypirc`, não vai pedir token.
Senão, cole o token quando pedir.

### **2. Verificar Publicação**

Abra: https://test.pypi.org/project/hermes-notifier/

### **3. Testar Instalação**

```bash
pip install --index-url https://test.pypi.org/simple/ hermes-notifier
```

### **4. Testar Importação**

```bash
python3 -c "from hermes_notifier import HermesUnifiedClient; print('✅ Funcionou!')"
```

---

## 🚀 Publicar no PyPI (Produção)

Se tudo funcionou no TestPyPI:

```bash
twine upload dist/*
```

Verificar: https://pypi.org/project/hermes-notifier/

Instalar:
```bash
pip install hermes-notifier
```

---

## 📝 Checklist Completo

### **TestPyPI**
- [ ] Conta criada em https://test.pypi.org
- [ ] Email verificado
- [ ] Token criado
- [ ] Token salvo em lugar seguro
- [ ] (Opcional) `~/.pypirc` configurado
- [ ] Publicação testada
- [ ] Instalação testada

### **PyPI**
- [ ] Conta criada em https://pypi.org
- [ ] Email verificado
- [ ] Token criado
- [ ] Token salvo em lugar seguro
- [ ] (Opcional) `~/.pypirc` configurado
- [ ] Pronto para publicar!

---

## 🔒 Segurança

### **Boas Práticas**

1. ✅ **Nunca compartilhe seu token**
2. ✅ **Use tokens específicos por projeto** (quando possível)
3. ✅ **Revogue tokens antigos** se não usar mais
4. ✅ **Mantenha `~/.pypirc` com permissões 600**
5. ✅ **Não commite tokens no git**

### **Revogar Token**

Se precisar revogar:
1. Acesse: https://pypi.org/manage/account/token/
2. Clique em "Remove" no token que quer revogar
3. Crie um novo token se necessário

---

## 🐛 Troubleshooting

### **Erro: "Invalid or non-existent authentication"**

**Causa**: Token incorreto ou expirado

**Solução**:
1. Verifique se copiou o token completo
2. Crie um novo token
3. Atualize `~/.pypirc` se estiver usando

### **Erro: "403 Forbidden"**

**Causa**: Token sem permissões ou projeto já existe

**Solução**:
1. Verifique se o token tem permissões corretas
2. Se o projeto já existe, você precisa ser owner/maintainer

### **Erro: "Package already exists"**

**Causa**: Versão já foi publicada

**Solução**:
1. Incremente a versão no `setup.py`
2. Faça novo build: `python3 -m build`
3. Publique novamente

---

## 📚 Links Úteis

- **TestPyPI**: https://test.pypi.org
- **PyPI**: https://pypi.org
- **Documentação**: https://packaging.python.org/
- **Twine Docs**: https://twine.readthedocs.io/

---

## 🎯 Resumo Rápido

```bash
# 1. Criar conta
# Acesse: https://test.pypi.org/account/register/

# 2. Criar token
# Acesse: https://test.pypi.org/manage/account/token/

# 3. Publicar
twine upload --repository testpypi dist/*
# Cole o token quando pedir

# 4. Verificar
pip install --index-url https://test.pypi.org/simple/ hermes-notifier

# 5. Se OK, publicar no PyPI
# Criar conta e token em https://pypi.org
twine upload dist/*
```

---

**Pronto! Agora você pode publicar seu pacote Python! 🎉**

