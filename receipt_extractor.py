"""
iFood Receipt Extractor - Extrator de Recibos do iFood via OCR
===============================================================

Este programa automatiza a extração de informações de screenshots de recibos do iFood
usando reconhecimento óptico de caracteres (OCR). Realiza a leitura de imagens,
extrai texto e valores monetários, salvando os dados em um arquivo CSV.

Autor: Emerson
Data: 2026
Requisitos:
    - tesseract-ocr
    - Python 3.7+
    - Bibliotecas: Pillow, pandas, pytesseract

Uso:
    python receipt_extractor.py
"""

import os
import re
import pandas as pd
from PIL import Image
import pytesseract


# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

# Caminho do Tesseract OCR (padrão Windows)
# Tente encontrar o tesseract automaticamente ou use o caminho padrão
CAMINHO_TESSERACT = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

if os.path.exists(CAMINHO_TESSERACT):
    pytesseract.pytesseract.tesseract_cmd = CAMINHO_TESSERACT
    print(f"✓ Tesseract encontrado em: {CAMINHO_TESSERACT}")
else:
    print("⚠ AVISO: Tesseract não encontrado no caminho padrão. Tentando pelo sistema...")

# Diretório contendo as imagens de recibos
DIRETORIO_IMAGENS = 'prints_ifood'

# Arquivo CSV de saída com os dados extraídos
ARQUIVO_SAIDA = 'dados_ifood_extraidos.csv'


# ============================================================================
# FUNÇÕES PRINCIPAIS
# ============================================================================

def extrair_valor_monetario(texto):
    """
    Extrai valores monetários em Real (R$) do texto da imagem.
    
    Procura por padrões como "R$ XX,XX" ou "R$ XX.XXX,XX" e converte
    para float considerando a formatação brasileira (vírgula como separador decimal).
    
    Args:
        texto (str): Texto extraído da imagem via OCR
    
    Returns:
        float: Valor em reais encontrado, ou 0.0 se não houver valor válido
    
    Exemplos:
        >>> extrair_valor_monetario("Total: R$ 45,50")
        45.5
        >>> extrair_valor_monetario("Sem valor aqui")
        0.0
    """
    # Procura padrão R$ seguido de dígitos, pontos e vírgulas
    match = re.search(r'R\$\s*([\d.,]+)', texto, re.IGNORECASE)
    
    if match:
        try:
            # Remove pontos (separadores de milhar) e substitui vírgula por ponto (decimal)
            valor_limpo = match.group(1).replace('.', '').replace(',', '.')
            return float(valor_limpo)
        except ValueError:
            return 0.0
    
    return 0.0


def processar_imagens():
    """
    Processa todas as imagens do diretório e extrai informações via OCR.
    
    Realiza as seguintes operações:
    1. Valida a existência do diretório de imagens
    2. Lista arquivos de imagem (.png, .jpg, .jpeg)
    3. Para cada imagem:
       - Carrega a imagem
       - Executa OCR (português, com fallback para idioma padrão)
       - Extrai valores monetários
       - Registra os dados
    4. Salva os resultados em CSV
    
    A função imprime mensagens de progresso e erros durante a execução.
    """
    # Verifica se o diretório existe
    if not os.path.exists(DIRETORIO_IMAGENS):
        print(f"✗ Pasta '{DIRETORIO_IMAGENS}' não encontrada!")
        return

    # Lista apenas arquivos de imagem
    arquivos = [
        f for f in os.listdir(DIRETORIO_IMAGENS) 
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    
    print(f"📸 Encontradas {len(arquivos)} imagens. Iniciando processamento...\n")

    # Lista para armazenar dados extraídos
    dados = []

    # Processa cada imagem
    for arq in arquivos:
        print(f"{'='*60}")
        print(f"Processando: {arq}")
        print(f"{'='*60}")
        
        try:
            # Abre a imagem
            caminho_imagem = os.path.join(DIRETORIO_IMAGENS, arq)
            img = Image.open(caminho_imagem)
            
            # Tenta OCR em Português primeiro (mais preciso para recibos brasileiros)
            # Se falhar, tenta sem idioma específico (padrão: Inglês)
            try:
                texto = pytesseract.image_to_string(img, lang='por')
            except Exception as e:
                print(f"   ⚠ Erro com idioma Português: {e}")
                print(f"   → Tentando sem idioma específico...")
                texto = pytesseract.image_to_string(img)

            # Exibe preview do texto extraído (para verificação)
            preview = texto[:100].replace('\n', ' ')
            print(f"   📄 Texto (preview): {preview}...")
            
            # Extrai valor monetário
            valor = extrair_valor_monetario(texto)
            print(f"   💵 Valor identificado: R$ {valor:.2f}")
            
            # Armazena dados
            dados.append({
                'Arquivo': arq,
                'Texto': texto,
                'Valor': valor
            })

        except Exception as e:
            print(f"   ✗ [ERRO] Falha ao processar imagem: {e}")

    print(f"\n{'='*60}")
    
    # Salva resultados em CSV se houver dados
    if dados:
        df = pd.DataFrame(dados)
        df.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8-sig')
        print(f"✓ Conclusão com sucesso!")
        print(f"   📊 {len(dados)} imagem(ns) processada(s)")
        print(f"   💾 Dados salvos em: {ARQUIVO_SAIDA}")
        print(f"   💰 Valor total extraído: R$ {df['Valor'].sum():.2f}")
    else:
        print(f"✗ Nenhum dado foi extraído com sucesso.")


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    processar_imagens()