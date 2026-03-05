# Image to PDF Converter

Um conversor de imagens para PDF com interface gráfica (GUI), desenvolvido em Python.

## 📋 Descrição

Esta aplicação permite converter imagens (PNG, JPG, JPEG, TIF, TIFF, BMP, WEBP, GIF) em arquivos PDF. Possui uma interface gráfica amigável com suporte a drag-and-drop e operações em lote.

## ✨ Recursos

- ✅ Suporte a múltiplos formatos de imagem (PNG, JPG, JPEG, TIF, TIFF, BMP, WEBP, GIF)
- ✅ Interface gráfica com Tkinter
- ✅ Drag-and-drop para facilitar o uso
- ✅ Conversão em lote
- ✅ Manipulação e fusão de PDFs

## 🛠️ Requisitos

- Python 3.x
- Dependências listadas em `requirements.txt`

## 📦 Instalação

1. Clone ou baixe este repositório

2. Crie um ambiente virtual (venv):

**No Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**No Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**No Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🚀 Uso

Execute o programa:

```bash
python img_to_pdf.py
```

A interface gráfica se abrirá e você poderá:
- Arrastar e soltar imagens
- Selecionar arquivos manualmente
- Converter para PDF

## 📚 Dependências

- **img2pdf**: Conversão de imagens para PDF
- **pillow**: Processamento de imagens
- **pypdf**: Manipulação de arquivos PDF
- **tkinterdnd2**: Suporte a drag-and-drop na interface gráfica

## 📄 Licença

Este projeto está disponível para uso pessoal e educacional.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para abrir issues ou pull requests.
