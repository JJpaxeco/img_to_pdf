PDF Tools v2.2

Arquivos:
- img_to_pdf_v2_2.py
- requirements_v2_2.txt

Para testar a versão nova:
1. Coloque estes dois arquivos em uma pasta nova.
2. Abra o PowerShell nessa pasta.
3. Execute:
   py -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements_v2_2.txt
   py img_to_pdf_v2_2.py

A janela precisa mostrar no título: Ferramentas PDF (Tkinter) - v2.2

Na aba Word/Excel -> PDF deve aparecer:
- Office: verificação ainda não realizada / status do Office
- Modo de conversão
- Automático
- Office fiel
- Simples sem Office
- Botão Verificar Office

Se você abrir um .exe antigo, nada disso vai aparecer. É necessário gerar o .exe novamente usando este arquivo v2.2.
