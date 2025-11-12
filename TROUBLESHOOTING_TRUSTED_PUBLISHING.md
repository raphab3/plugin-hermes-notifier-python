# 🔧 Troubleshooting: Trusted Publishing Error

> Resolvendo o erro "invalid-publisher: valid token, but no corresponding publisher"

---

## ❌ **Erro Recebido**

```
Error: Trusted publishing exchange failure
Token request failed: the server refused the request for the following reasons:
* `invalid-publisher`: valid token, but no corresponding publisher
```

---

## ✅ **Soluções (Tente Nesta Ordem)**

### **Solução 1: Remover e Recriar o Pending Publisher**

1. **Acesse**: https://pypi.org/manage/account/publishing/

2. **Remova** o pending publisher existente (se houver):
   - Clique em "Remove" ao lado de "hermes-notifier"

3. **Adicione novamente** com estes valores EXATOS:

```
Nome do Projeto PyPI:
hermes-notifier

Proprietário:
raphab3

Nome de repositório:
plugin-hermes-notifier-python

Nome do fluxo de trabalho:
publish.yml

Nome do ambiente:
[DEIXE EM BRANCO - campo opcional]
```

4. **Clique em "Adicionar"**

5. **Aguarde 1-2 minutos** (o PyPI pode levar um tempo para processar)

---

### **Solução 2: Atualizar Workflows no Repositório**

Os workflows foram atualizados para **NÃO usar environment**.

**Você precisa copiar os novos workflows para o repositório GitHub!**

```bash
cd ~/Documents/projetos/EM2/plugin-hermes-notifier-python

# Copiar workflows atualizados
cp ~/Documents/projetos/EM2/hermes-notifications/plugins/python/.github/workflows/publish.yml .github/workflows/
cp ~/Documents/projetos/EM2/hermes-notifications/plugins/python/.github/workflows/test-publish.yml .github/workflows/

# Commit e push
git add .github/workflows/
git commit -m "fix: remove environment from workflows"
git push origin main
```

---

### **Solução 3: Re-executar o Workflow**

Depois de atualizar:

1. **Acesse**: https://github.com/raphab3/plugin-hermes-notifier-python/actions

2. **Clique** no workflow que falhou

3. **Clique** em "Re-run all jobs"

4. **Aguarde** a execução

---

### **Solução 4: Criar Nova Release**

Se ainda não funcionar, delete a tag e crie novamente:

```bash
cd ~/Documents/projetos/EM2/plugin-hermes-notifier-python

# Deletar tag local e remota
git tag -d v1.1.0
git push origin :refs/tags/v1.1.0

# Criar novamente
git tag -a v1.1.0 -m "v1.1.0 - Initial Release"
git push origin v1.1.0
```

Depois crie a release no GitHub novamente.

---

## 🔍 **Verificações Importantes**

### **1. Verificar Pending Publisher no PyPI**

Acesse: https://pypi.org/manage/account/publishing/

Deve aparecer:

```
Pending publishers
┌─────────────────────────────────────────────────────────┐
│ hermes-notifier                                         │
│ Owner: raphab3                                          │
│ Repository: plugin-hermes-notifier-python               │
│ Workflow: publish.yml                                   │
│ Environment: (none)                                     │
│ [Remove]                                                │
└─────────────────────────────────────────────────────────┘
```

**Se não aparecer nada**: O pending publisher não foi criado!

---

### **2. Verificar Workflows no GitHub**

Acesse: https://github.com/raphab3/plugin-hermes-notifier-python/blob/main/.github/workflows/publish.yml

Deve ter este conteúdo (SEM a seção `environment:`):

```yaml
jobs:
  pypi-publish:
    name: Upload release to PyPI
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # IMPORTANT: mandatory for trusted publishing
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      # ... resto do workflow
```

**Se ainda tiver `environment:`**: Atualize o workflow!

---

### **3. Verificar se o Projeto Já Existe no PyPI**

Acesse: https://pypi.org/project/hermes-notifier/

**Se retornar 404 (Not Found)**: ✅ Correto! Use "pending publisher"

**Se o projeto JÁ EXISTIR**: ❌ Problema!
- Você precisa ser owner do projeto
- Adicione trusted publisher nas configurações do projeto
- Não use "pending publisher"

---

## 🎯 **Checklist de Verificação**

Antes de tentar novamente:

- [ ] Pending publisher criado no PyPI
- [ ] Campo "Nome do ambiente" está em BRANCO
- [ ] Workflows atualizados no GitHub (sem `environment:`)
- [ ] Aguardou 1-2 minutos após criar pending publisher
- [ ] Projeto NÃO existe no PyPI (ou você é owner)
- [ ] Tag v1.1.0 existe no GitHub

---

## 📝 **Passo a Passo Completo (Do Zero)**

### **1. Limpar Tudo**

```bash
# No PyPI
# Acesse: https://pypi.org/manage/account/publishing/
# Remova todos os pending publishers de "hermes-notifier"

# No GitHub
cd ~/Documents/projetos/EM2/plugin-hermes-notifier-python
git tag -d v1.1.0
git push origin :refs/tags/v1.1.0
```

### **2. Atualizar Workflows**

```bash
# Copiar workflows atualizados
cp ~/Documents/projetos/EM2/hermes-notifications/plugins/python/.github/workflows/*.yml .github/workflows/

# Commit
git add .github/workflows/
git commit -m "fix: update workflows for trusted publishing"
git push origin main
```

### **3. Criar Pending Publisher no PyPI**

1. Acesse: https://pypi.org/manage/account/publishing/
2. Clique em "Add a new pending publisher"
3. Preencha:
   - Nome do Projeto PyPI: `hermes-notifier`
   - Proprietário: `raphab3`
   - Nome de repositório: `plugin-hermes-notifier-python`
   - Nome do fluxo de trabalho: `publish.yml`
   - Nome do ambiente: **[DEIXE EM BRANCO]**
4. Clique em "Adicionar"
5. **Aguarde 2 minutos**

### **4. Criar Release**

```bash
# Criar tag
git tag -a v1.1.0 -m "v1.1.0 - Initial Release"
git push origin v1.1.0

# Ou via GitHub interface:
# https://github.com/raphab3/plugin-hermes-notifier-python/releases/new
```

### **5. Verificar**

1. GitHub Actions: https://github.com/raphab3/plugin-hermes-notifier-python/actions
2. Deve aparecer "Publish Python Package" rodando
3. Aguarde completar
4. Verifique: https://pypi.org/project/hermes-notifier/

---

## 🐛 **Outros Erros Possíveis**

### **"Workflow file not found"**

**Causa**: Arquivo `.github/workflows/publish.yml` não existe

**Solução**: Copie os workflows para o repositório

### **"Environment not found"**

**Causa**: Workflow usa `environment: pypi` mas não existe no GitHub

**Solução**: Use os workflows atualizados (sem environment)

### **"Project already exists"**

**Causa**: Projeto já foi publicado no PyPI

**Solução**: 
- Se você é owner: Configure trusted publisher nas settings do projeto
- Se não é owner: Use outro nome de projeto

---

## 📞 **Ainda Não Funcionou?**

Se após todas as soluções ainda não funcionar:

1. **Verifique os logs completos** do GitHub Actions
2. **Tire screenshot** do erro
3. **Verifique** se o pending publisher aparece no PyPI
4. **Aguarde** alguns minutos (o PyPI pode ter delay)

---

## ✅ **Quando Funcionar**

Você verá:

```
✅ Successfully uploaded hermes_notifier-1.1.0.tar.gz
✅ Successfully uploaded hermes_notifier-1.1.0-py3-none-any.whl
```

E o pacote estará disponível em: https://pypi.org/project/hermes-notifier/

---

**Boa sorte! 🚀**

