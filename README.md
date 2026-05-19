# Ferramentas PDF com Python e Tkinter

Aplicação desktop simples para **criar PDFs a partir de imagens** e **juntar vários PDFs em um único arquivo**, usando uma interface gráfica feita com Python e Tkinter.

O app foi pensado para tarefas rápidas do dia a dia: arrastar imagens, organizar a ordem, gerar um PDF único, criar um PDF separado para cada imagem ou juntar vários PDFs já existentes.

---

## O que o aplicativo faz

### 1. Converter imagens para PDF

Na aba **Imagem → PDF**, você pode adicionar imagens e gerar arquivos PDF.

Funções disponíveis:

- Adicionar imagens manualmente pelo botão **Adicionar imagens...**.
- Arrastar e soltar imagens diretamente na lista.
- Aceitar os formatos:
  - `.png`
  - `.jpg`
  - `.jpeg`
  - `.tif`
  - `.tiff`
  - `.bmp`
  - `.webp`
  - `.gif`
- Remover uma imagem selecionada da lista.
- Limpar toda a lista de imagens.
- Alterar a ordem das imagens com os botões **↑ Subir** e **↓ Descer**.
- Gerar **um PDF único** com todas as imagens, respeitando a ordem exibida na lista.
- Gerar **um PDF separado para cada imagem**.
- Escolher manualmente onde salvar o PDF ou a pasta de saída.
- Ajustar as imagens automaticamente para página **A4**, com orientação retrato ou paisagem conforme o formato da imagem.
- Evitar sobrescrever arquivos existentes, criando nomes como:
  - `arquivo.pdf`
  - `arquivo_2.pdf`
  - `arquivo_3.pdf`

### 2. Juntar PDFs

Na aba **Juntar PDFs**, você pode unir vários arquivos PDF em um único PDF final.

Funções disponíveis:

- Adicionar PDFs manualmente pelo botão **Adicionar PDFs...**.
- Arrastar e soltar PDFs diretamente na lista.
- Remover um PDF selecionado da lista.
- Limpar toda a lista de PDFs.
- Alterar a ordem dos PDFs com os botões **↑ Subir** e **↓ Descer**.
- Salvar todos os PDFs selecionados em um único arquivo final.
- Preservar a ordem da lista na junção.
- Evitar sobrescrever arquivos existentes, criando nomes incrementais automaticamente.
- Solicitar senha quando algum PDF protegido exigir desbloqueio para leitura.

### 3. Interface gráfica

A aplicação possui uma janela com duas abas:

- **Imagem → PDF**
- **Juntar PDFs**

A interface usa Tkinter e suporte a arrastar e soltar arquivos por meio da biblioteca `tkinterdnd2`.

### 4. Tratamento de arquivos e segurança contra sobrescrita

O app tenta facilitar o uso de caminhos e nomes de arquivos:

- Se o usuário informar um nome de saída sem `.pdf`, o programa adiciona `.pdf` automaticamente.
- Se o arquivo de saída já existir, o programa não sobrescreve o arquivo original.
- Arquivos duplicados na mesma lista são ignorados.
- Arquivos inválidos ou formatos não suportados são desconsiderados.

---

## Como funciona por dentro

O projeto usa estas bibliotecas principais:

| Biblioteca | Função no projeto |
|---|---|
| `img2pdf` | Converte imagens para PDF tentando preservar qualidade e evitar recompressão quando possível. |
| `pillow` | Abre e manipula imagens, além de gerar o ícone padrão do app quando não existe um ícone externo. |
| `pypdf` | Lê, descriptografa quando possível e junta arquivos PDF. |
| `tkinterdnd2` | Adiciona suporte a arrastar e soltar arquivos na interface Tkinter. |
| `tkinter` | Cria a interface gráfica do aplicativo. |

O arquivo `requirements.txt` instala as dependências externas:

```txt
img2pdf
pillow
pypdf
tkinterdnd2
```

O `tkinter` normalmente já acompanha o Python no Windows e no macOS quando instalado pelo site oficial. No Linux, pode ser necessário instalar o pacote do sistema separadamente.

---

## Requisitos

Antes de instalar, você precisa ter:

- Python **3.10 ou superior**.
- `pip`.
- Ambiente gráfico disponível.
- Arquivos do projeto na mesma pasta:
  - `img_to_pdf.py`
  - `requirements.txt`
  - `README.md`

A versão 3.10 ou superior é recomendada porque o código usa anotações modernas de tipo, como `list[str]` e `str | None`.

---

# Instalação no Windows

## 1. Instalar o Python

1. Acesse o site oficial do Python.
2. Baixe a versão mais recente do Python 3 para Windows.
3. Durante a instalação, marque a opção:

```text
Add python.exe to PATH
```

4. Conclua a instalação.

Depois, abra o **PowerShell** e confirme:

```powershell
python --version
```

Também confirme o `pip`:

```powershell
python -m pip --version
```

## 2. Acessar a pasta do projeto

Entre na pasta onde estão os arquivos do app.

Exemplo:

```powershell
cd "C:\Caminho\Do\Projeto"
```

A pasta deve conter pelo menos:

```text
img_to_pdf.py
requirements.txt
README.md
```

## 3. Criar ambiente virtual

No PowerShell:

```powershell
python -m venv .venv
```

## 4. Ativar o ambiente virtual

No PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se aparecer erro de política de execução, use este comando apenas para a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois ative novamente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando o ambiente estiver ativo, o terminal normalmente mostrará `(.venv)` no início da linha.

## 5. Atualizar o pip

```powershell
python -m pip install --upgrade pip
```

## 6. Instalar as dependências

```powershell
pip install -r requirements.txt
```

## 7. Executar o aplicativo

```powershell
python .\img_to_pdf.py
```

---

# Instalação no Linux

As instruções abaixo funcionam principalmente para distribuições baseadas em Debian/Ubuntu. Para outras distribuições, veja os exemplos logo abaixo.

## 1. Instalar Python, pip, venv e Tkinter

No Ubuntu, Debian, Linux Mint e derivados:

```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv python3-tk
```

Confirme a versão:

```bash
python3 --version
```

Confirme o `pip`:

```bash
python3 -m pip --version
```

## 2. Acessar a pasta do projeto

```bash
cd /caminho/do/projeto
```

A pasta deve conter:

```text
img_to_pdf.py
requirements.txt
README.md
```

## 3. Criar ambiente virtual

```bash
python3 -m venv .venv
```

## 4. Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

## 5. Atualizar o pip

```bash
python -m pip install --upgrade pip
```

## 6. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 7. Executar o aplicativo

```bash
python img_to_pdf.py
```

## Pacotes equivalentes em outras distribuições

Fedora:

```bash
sudo dnf install -y python3 python3-pip python3-tkinter
```

Arch Linux/Manjaro:

```bash
sudo pacman -Syu python python-pip tk
```

openSUSE:

```bash
sudo zypper install python3 python3-pip python3-tk
```

> Observação: se você estiver usando Linux Server sem interface gráfica, a aplicação não abrirá diretamente no terminal porque ela depende de janela gráfica.

---

# Instalação no macOS

## 1. Instalar o Python

Você pode instalar o Python pelo site oficial ou pelo Homebrew.

### Opção A: Python pelo site oficial

1. Baixe o instalador do Python para macOS no site oficial.
2. Instale normalmente.
3. Abra o Terminal e confirme:

```bash
python3 --version
```

### Opção B: Python pelo Homebrew

Se você usa Homebrew:

```bash
brew install python
```

Confirme:

```bash
python3 --version
```

## 2. Verificar Tkinter no macOS

Normalmente o Tkinter já vem disponível no Python instalado pelo site oficial.

Teste com:

```bash
python3 -m tkinter
```

Se abrir uma pequena janela de teste do Tkinter, está funcionando.

## 3. Acessar a pasta do projeto

```bash
cd /caminho/do/projeto
```

## 4. Criar ambiente virtual

```bash
python3 -m venv .venv
```

## 5. Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

## 6. Atualizar o pip

```bash
python -m pip install --upgrade pip
```

## 7. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 8. Executar o aplicativo

```bash
python img_to_pdf.py
```

---

# Como usar o aplicativo

## Converter várias imagens em um único PDF

1. Abra o app.
2. Entre na aba **Imagem → PDF**.
3. Clique em **Adicionar imagens...** ou arraste as imagens para a lista.
4. Organize a ordem usando **↑ Subir** e **↓ Descer**.
5. Deixe marcada a opção **PDF único**.
6. Deixe marcada a opção **Ajustar tamanho (A4)** se quiser padronizar as páginas em A4.
7. Escolha onde salvar o arquivo final.
8. Clique em **Converter**.

Resultado esperado:

```text
Um único PDF contendo todas as imagens, na ordem escolhida.
```

## Converter cada imagem em um PDF separado

1. Abra a aba **Imagem → PDF**.
2. Adicione as imagens.
3. Desmarque a opção **PDF único**.
4. Escolha a pasta onde os PDFs serão salvos.
5. Clique em **Converter**.

Resultado esperado:

```text
Um PDF separado para cada imagem.
```

Exemplo:

```text
foto1.jpg  -> foto1.pdf
foto2.png  -> foto2.pdf
foto3.webp -> foto3.pdf
```

## Juntar vários PDFs

1. Abra a aba **Juntar PDFs**.
2. Clique em **Adicionar PDFs...** ou arraste os PDFs para a lista.
3. Organize a ordem usando **↑ Subir** e **↓ Descer**.
4. Escolha onde salvar o PDF final.
5. Clique em **Juntar PDFs**.

Resultado esperado:

```text
Um único PDF contendo todos os PDFs adicionados, na ordem da lista.
```

---

# Observações importantes

## Ordem dos arquivos

A ordem exibida na lista é a ordem usada na conversão ou junção.

Se você adicionar:

```text
pagina_01.png
pagina_02.png
pagina_03.png
```

O PDF será gerado nessa mesma sequência.

## Ajuste A4

Quando a opção **Ajustar tamanho (A4)** está marcada, o app:

- Usa tamanho de página A4.
- Escolhe orientação retrato ou paisagem conforme a imagem.
- Mantém margem aproximada de 6,35 mm.
- Redimensiona a imagem para caber na página.
- Evita aumentar imagens pequenas além do tamanho original.

## Qualidade da imagem

O app tenta primeiro converter as imagens diretamente com `img2pdf`, evitando recompressão quando possível.

Se a conversão direta falhar, ele usa um método alternativo:

1. Abre a imagem com `Pillow`.
2. Converte a imagem em PNG em memória.
3. Gera o PDF a partir desse PNG.

Esse fallback aumenta a compatibilidade com imagens problemáticas.

## PDFs protegidos por senha

Ao juntar PDFs, se algum arquivo estiver protegido, o app tenta abrir sem senha.

Se não conseguir, ele exibe uma janela solicitando a senha.

Se a senha estiver errada ou não for informada, a junção será interrompida.

## Arquivos existentes

O app evita sobrescrever arquivos já existentes.

Exemplo:

```text
documento.pdf
documento_2.pdf
documento_3.pdf
```

---

# Estrutura do projeto

Estrutura mínima esperada:

```text
.
├── img_to_pdf.py
├── requirements.txt
└── README.md
```

Arquivos opcionais de ícone:

```text
pdf.ico
pdf.png
```

Se `pdf.ico` existir, ele será usado como ícone no Windows.

Se `pdf.png` existir, ele poderá ser usado como ícone alternativo.

Se nenhum dos dois existir, o próprio app gera um ícone simples escrito **PDF**.

---

# Principais funções do código

## Funções de apoio

| Função | O que faz |
|---|---|
| `_safe_pdf_path()` | Garante que o caminho de saída termine com `.pdf`. |
| `_parse_dnd_files()` | Interpreta arquivos arrastados para a janela, inclusive caminhos com espaços. |
| `_dpi_tuple()` | Normaliza informações de DPI usadas no cálculo de tamanho da imagem. |
| `a4_fit_layout_fun()` | Define layout A4, orientação e escala da imagem dentro da página. |

## Funções de conversão e junção

| Função | O que faz |
|---|---|
| `convert_image_to_pdf_single()` | Converte uma única imagem em um PDF. |
| `convert_images_to_one_pdf()` | Converte várias imagens em um único PDF. |
| `merge_pdfs()` | Junta vários PDFs em um único arquivo final e trata PDFs protegidos por senha. |

## Classe principal

| Classe/Função | O que faz |
|---|---|
| `App` | Classe principal da interface gráfica. |
| `_build_ui()` | Cria a estrutura geral da interface com abas. |
| `_build_tab_image()` | Monta a aba de conversão de imagens. |
| `_build_tab_merge()` | Monta a aba de junção de PDFs. |
| `_add_image_path()` | Adiciona uma imagem válida à lista. |
| `_on_drop_images()` | Recebe imagens arrastadas para a janela. |
| `_add_images()` | Abre o seletor de arquivos para escolher imagens. |
| `_remove_selected_image()` | Remove a imagem selecionada. |
| `_clear_images()` | Limpa a lista de imagens. |
| `_img_move_up()` | Move a imagem selecionada uma posição para cima. |
| `_img_move_down()` | Move a imagem selecionada uma posição para baixo. |
| `_on_one_pdf_toggle()` | Alterna entre PDF único e PDFs separados. |
| `_pick_img_output()` | Permite escolher arquivo final ou pasta de saída das imagens. |
| `_unique_outfile()` | Cria um nome alternativo se o arquivo já existir. |
| `_do_images_convert()` | Executa a conversão das imagens. |
| `_add_pdf_path()` | Adiciona um PDF válido à lista. |
| `_on_drop_pdfs()` | Recebe PDFs arrastados para a janela. |
| `_add_pdfs()` | Abre o seletor de arquivos para escolher PDFs. |
| `_remove_selected()` | Remove o PDF selecionado. |
| `_clear_list()` | Limpa a lista de PDFs. |
| `_move_up()` | Move o PDF selecionado uma posição para cima. |
| `_move_down()` | Move o PDF selecionado uma posição para baixo. |
| `_pick_merge_out()` | Permite escolher onde salvar o PDF juntado. |
| `_ask_password()` | Solicita senha para PDF protegido. |
| `_do_merge()` | Executa a junção dos PDFs. |

---

# Solução de problemas

## Erro: `ModuleNotFoundError`

Exemplo:

```text
ModuleNotFoundError: No module named 'img2pdf'
```

Solução:

```bash
pip install -r requirements.txt
```

Confirme também se o ambiente virtual está ativado.

## Erro relacionado ao Tkinter no Linux

Exemplo:

```text
ModuleNotFoundError: No module named 'tkinter'
```

No Ubuntu/Debian:

```bash
sudo apt update && sudo apt install -y python3-tk
```

Depois execute novamente:

```bash
python img_to_pdf.py
```

## A janela não abre no Linux Server

A aplicação precisa de ambiente gráfico.

Em servidores sem interface gráfica, será necessário:

- Executar em um computador com interface gráfica.
- Usar encaminhamento X11.
- Usar uma sessão remota com suporte gráfico.
- Adaptar o projeto para modo CLI, se desejado.

## Drag-and-drop não funciona

Verifique se a dependência está instalada:

```bash
pip show tkinterdnd2
```

Se não aparecer, instale novamente:

```bash
pip install tkinterdnd2
```

## O PDF final ficou com páginas em ordem errada

A ordem do PDF é exatamente a ordem exibida na lista.

Use os botões:

```text
↑ Subir
↓ Descer
```

antes de converter ou juntar.

## O app não sobrescreveu meu arquivo

Esse comportamento é intencional.

Se `arquivo.pdf` já existir, o app cria automaticamente:

```text
arquivo_2.pdf
```

---

# Atualizar dependências

Com o ambiente virtual ativado:

```bash
python -m pip install --upgrade pip
```

Depois:

```bash
pip install --upgrade -r requirements.txt
```

---

# Remover ambiente virtual e reinstalar do zero

## Windows PowerShell

```powershell
deactivate
```

Depois:

```powershell
Remove-Item -Recurse -Force .\.venv
```

Recrie:

```powershell
python -m venv .venv
```

Ative:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale novamente:

```powershell
pip install -r requirements.txt
```

## Linux/macOS

```bash
deactivate
```

Depois:

```bash
rm -rf .venv
```

Recrie:

```bash
python3 -m venv .venv
```

Ative:

```bash
source .venv/bin/activate
```

Instale novamente:

```bash
pip install -r requirements.txt
```

---

# Licença

Este projeto está disponível para uso pessoal, educacional e interno.

Se for publicar o projeto em um repositório, recomenda-se adicionar um arquivo `LICENSE` informando claramente os termos de uso.
