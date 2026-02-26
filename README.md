# iFood Receipt Extractor 📸💵

Extrator automático de informações de recibos do iFood usando Reconhecimento Óptico de Caracteres (OCR).

## Sobre o Projeto

Este programa automatiza a extração de dados de screenshots de recibos do iFood. Lê as imagens, identifica texto e valores monetários via OCR, e exporta os dados em um arquivo CSV para análise.

**Caso de uso:** Análise de despesas, integração com planilhas de controle financeiro, auditoria de pedidos, etc.

---

## Funcionalidades

- ✅ Processamento em lote de múltiplas imagens
- ✅ Reconhecimento óptico de caracteres (OCR) em português
- ✅ Extração automática de valores monetários (R$)
- ✅ Exportação de dados em CSV
- ✅ Tratamento robusto de erros
- ✅ Fallback automático para English se português não funcionar
- ✅ Mensagens informativas durante processamento

---

## 📋 Requisitos

### Sistema Operacional

- Windows 10+

### Dependências

- **Tesseract OCR** (obrigatório)
- **Python 3.7+**
- **Bibliotecas Python:**
  - `Pillow` (processamento de imagens)
  - `pandas` (manipulação de dados)
  - `pytesseract` (interface com Tesseract)

---

## 📦 Instalação

### 1. Instalar Tesseract OCR

**Windows:**

1. Baixar o instalador em: https://github.com/UB-Mannheim/tesseract/wiki
2. Executar o instalador (padrão: `C:\Program Files\Tesseract-OCR\`)
3. Marcar a opção de instalar idiomas portugueses durante a instalação

### 2. Instalar Dependências Python

```bash
pip install Pillow pandas pytesseract
```

Ou usando `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🔧 Como Usar

### Passo 1: Preparar as Imagens

1. Crie uma pasta `prints_ifood/` no mesmo diretório do script
2. Coloque as imagens de recibos dentro dela (formatos: `.png`, `.jpg`, `.jpeg`)

### Passo 2: Executar o Script

```bash
python receipt_extractor.py
```

### Passo 3: Verificar Resultados

Os dados extraídos serão salvos em `dados_ifood_extraidos.csv` com as colunas:

- **Arquivo:** Nome do arquivo da imagem
- **Texto:** Texto completo extraído pela OCR
- **Valor:** Valor monetário identificado (em reais)

---

## 📊 Exemplo de Saída

| Arquivo        | Texto                                   | Valor |
| -------------- | --------------------------------------- | ----- |
| pedido_001.png | iFood - Seu Pedido... Total: R$ 45,50   | 45.5  |
| pedido_002.jpg | iFood - Confirme seu Pedido... R$ 78,90 | 78.9  |

---

## ⚙️ Configuração

Edite as variáveis no início do script conforme necessário:

```python
CAMINHO_TESSERACT = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ajuste se diferente
DIRETORIO_IMAGENS = 'prints_ifood'  # Pasta com as imagens
ARQUIVO_SAIDA = 'dados_ifood_extraidos.csv'  # Nome do arquivo de saída
```

---

## 🐛 Troubleshooting

### "Tesseract não encontrado"

- Verifique se Tesseract está instalado em `C:\Program Files\Tesseract-OCR\`
- Se em local diferente, atualize `CAMINHO_TESSERACT`

### Texto extraído está ruim

- OCR não é 100% preciso; imagens de baixa qualidade afetam resultados
- Tente melhorar a qualidade do screenshot (foco, contraste)
- Certifique-se de que o idioma português foi instalado com Tesseract

### "Nenhum valor foi extraído"

- Verifique se as imagens contêm texto de "R$"
- O programa busca por padrão `R$ XX,XX`

---

## 📄 Licença

Este projeto está disponível sob licença MIT.

---

## 👨‍💻 Autor

Emerson

---

## 🙏 Agradecimentos

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pytesseract](https://github.com/madmaze/pytesseract)
- [Pandas](https://pandas.pydata.org/)
- [Pillow](https://python-pillow.org/)

---

## 📧 Sugestões e Contribuições

Sinta-se à vontade para fazer fork, abrir issues e submeter pull requests!
