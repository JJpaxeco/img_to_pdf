import io
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

import img2pdf
from PIL import Image
from pypdf import PdfReader, PdfWriter
from tkinterdnd2 import TkinterDnD, DND_FILES


IMG_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp", ".gif"}


def _safe_pdf_path(path_str: str) -> Path:
    p = Path(path_str.strip().strip('"'))
    if p.suffix.lower() != ".pdf":
        p = p.with_suffix(".pdf")
    return p


def _parse_dnd_files(data: str) -> list[str]:
    out, cur, in_brace = [], "", False
    for ch in data:
        if ch == "{":
            in_brace = True
            cur = ""
            continue
        if ch == "}" and in_brace:
            in_brace = False
            if cur:
                out.append(cur)
            cur = ""
            continue
        if ch == " " and not in_brace:
            if cur:
                out.append(cur)
                cur = ""
            continue
        cur += ch
    if cur:
        out.append(cur)
    return [p.strip().strip('"') for p in out if p.strip()]


def convert_image_to_pdf_single(input_image: Path, output_pdf: Path) -> None:
    if not input_image.exists() or not input_image.is_file():
        raise FileNotFoundError(f"Imagem não encontrada: {input_image}")
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    try:
        pdf_bytes = img2pdf.convert(str(input_image))
        output_pdf.write_bytes(pdf_bytes)
        return
    except Exception:
        pass

    try:
        with Image.open(input_image) as im:
            buf = io.BytesIO()
            im.save(buf, format="PNG", optimize=False)
            png_bytes = buf.getvalue()
        pdf_bytes = img2pdf.convert(png_bytes)
        output_pdf.write_bytes(pdf_bytes)
    except Exception as e:
        raise RuntimeError(f"Falha ao converter a imagem para PDF: {e}") from e


def convert_images_to_one_pdf(image_paths: list[Path], output_pdf: Path) -> None:
    if not image_paths:
        raise ValueError("Nenhuma imagem foi selecionada.")
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    # 1) tenta direto (melhor para manter sem recompressão quando possível)
    try:
        pdf_bytes = img2pdf.convert([str(p) for p in image_paths])
        output_pdf.write_bytes(pdf_bytes)
        return
    except Exception:
        pass

    # 2) fallback: converte tudo para PNG (lossless) em memória e gera o PDF
    try:
        payloads: list[bytes] = []
        for p in image_paths:
            with Image.open(p) as im:
                buf = io.BytesIO()
                im.save(buf, format="PNG", optimize=False)
                payloads.append(buf.getvalue())
        pdf_bytes = img2pdf.convert(payloads)
        output_pdf.write_bytes(pdf_bytes)
    except Exception as e:
        raise RuntimeError(f"Falha ao converter imagens para PDF único: {e}") from e


def merge_pdfs(input_pdfs: list[Path], output_pdf: Path, password_cb) -> None:
    if not input_pdfs:
        raise ValueError("Nenhum PDF foi selecionado.")

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()

    for pdf_path in input_pdfs:
        if not pdf_path.exists() or not pdf_path.is_file():
            raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

        reader = PdfReader(str(pdf_path))

        if reader.is_encrypted:
            ok = False
            try:
                ok = bool(reader.decrypt(""))
            except Exception:
                ok = False

            if not ok:
                pwd = password_cb(pdf_path.name)
                if not pwd:
                    raise RuntimeError(f"Senha não informada para: {pdf_path.name}")
                try:
                    if not reader.decrypt(pwd):
                        raise RuntimeError(f"Senha incorreta para: {pdf_path.name}")
                except Exception as e:
                    raise RuntimeError(f"Não foi possível abrir (criptografado): {pdf_path.name}. Detalhe: {e}") from e

        for page in reader.pages:
            writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)


class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ferramentas PDF (Tkinter)")
        self.geometry("820x520")
        self.minsize(820, 520)

        self._merge_seen = set()
        self._img_seen = set()

        self._build_ui()

    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        tab_img = ttk.Frame(nb)
        tab_merge = ttk.Frame(nb)

        nb.add(tab_img, text="Imagem → PDF")
        nb.add(tab_merge, text="Juntar PDFs")

        self._build_tab_image(tab_img)
        self._build_tab_merge(tab_merge)

    # ===================== Aba 1: Imagens -> PDF(s) =====================

    def _build_tab_image(self, parent: ttk.Frame):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        # Top bar
        top = ttk.Frame(parent)
        top.grid(row=0, column=0, sticky="ew", padx=8, pady=(12, 6))
        top.columnconfigure(3, weight=1)

        ttk.Button(top, text="Adicionar imagens...", command=self._add_images).grid(row=0, column=0, sticky="w")
        ttk.Button(top, text="Remover selecionada", command=self._remove_selected_image).grid(row=0, column=1, padx=8)
        ttk.Button(top, text="Limpar lista", command=self._clear_images).grid(row=0, column=2)

        self.one_pdf_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="PDF único", variable=self.one_pdf_var, command=self._on_one_pdf_toggle).grid(row=0, column=4, sticky="e")

        # Big drop area (list)
        mid = ttk.Frame(parent)
        mid.grid(row=1, column=0, sticky="nsew", padx=8, pady=6)
        mid.columnconfigure(0, weight=1)
        mid.rowconfigure(1, weight=1)

        ttk.Label(mid, text="Arraste e solte imagens aqui (a ordem da lista será a ordem do PDF):").grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.img_list: list[Path] = []
        self.img_listbox = tk.Listbox(mid, selectmode=tk.SINGLE)
        self.img_listbox.grid(row=1, column=0, sticky="nsew")

        sb = ttk.Scrollbar(mid, orient="vertical", command=self.img_listbox.yview)
        sb.grid(row=1, column=1, sticky="ns")
        self.img_listbox.configure(yscrollcommand=sb.set)

        # DnD on the biggest area (listbox)
        self.img_listbox.drop_target_register(DND_FILES)
        self.img_listbox.dnd_bind("<<Drop>>", self._on_drop_images)

        # Reorder buttons
        side = ttk.Frame(mid)
        side.grid(row=1, column=2, sticky="ns", padx=(10, 0))
        ttk.Button(side, text="↑ Subir", command=self._img_move_up).grid(row=0, column=0, pady=(0, 6), sticky="ew")
        ttk.Button(side, text="↓ Descer", command=self._img_move_down).grid(row=1, column=0, pady=(0, 6), sticky="ew")

        # Bottom output chooser
        bottom = ttk.Frame(parent)
        bottom.grid(row=2, column=0, sticky="ew", padx=8, pady=(10, 6))
        bottom.columnconfigure(1, weight=1)

        self.img_out_label = ttk.Label(bottom, text="Salvar PDF final em:")
        self.img_out_label.grid(row=0, column=0, sticky="w")

        self.img_out_var = tk.StringVar()
        ttk.Entry(bottom, textvariable=self.img_out_var).grid(row=0, column=1, sticky="ew", padx=8)

        self.img_out_btn = ttk.Button(bottom, text="Escolher...", command=self._pick_img_output)
        self.img_out_btn.grid(row=0, column=2)

        ttk.Button(parent, text="Converter", command=self._do_images_convert).grid(row=3, column=0, pady=(8, 12))

        self._on_one_pdf_toggle()  # set initial label/button behavior

    def _normalize_path(self, p: Path) -> str:
        try:
            return str(p.resolve())
        except Exception:
            return str(p)

    def _add_image_path(self, img_path: Path):
        if img_path.suffix.lower() not in IMG_EXTS:
            return
        if not img_path.exists() or not img_path.is_file():
            return

        rp = self._normalize_path(img_path)
        if rp in self._img_seen:
            return

        self._img_seen.add(rp)
        self.img_list.append(img_path)
        self.img_listbox.insert(tk.END, img_path.name)

        # Sugestão automática de saída
        if not self.img_out_var.get().strip():
            if self.one_pdf_var.get():
                suggested = img_path.with_name(f"{img_path.stem}_IMAGENS.pdf")
                self.img_out_var.set(str(suggested))
            else:
                self.img_out_var.set(str(img_path.parent))

    def _on_drop_images(self, event):
        paths = _parse_dnd_files(event.data)
        added = 0
        for raw in paths:
            p = Path(raw)
            if p.suffix.lower() in IMG_EXTS:
                before = len(self.img_list)
                self._add_image_path(p)
                if len(self.img_list) > before:
                    added += 1
        if added == 0:
            messagebox.showwarning("Nenhuma imagem válida", "Solte arquivos de imagem (png, jpg, tiff, bmp, webp, gif).")
        return "break"

    def _add_images(self):
        paths = filedialog.askopenfilenames(
            title="Selecione imagens",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp *.webp *.gif"), ("Todos os arquivos", "*.*")],
        )
        for p in paths:
            self._add_image_path(Path(p))

    def _remove_selected_image(self):
        sel = self.img_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        removed = self.img_list[idx]

        self.img_listbox.delete(idx)
        del self.img_list[idx]

        self._img_seen.discard(self._normalize_path(removed))

    def _clear_images(self):
        self.img_listbox.delete(0, tk.END)
        self.img_list.clear()
        self._img_seen.clear()

    def _img_move_up(self):
        sel = self.img_listbox.curselection()
        if not sel:
            return
        i = sel[0]
        if i <= 0:
            return
        self.img_list[i - 1], self.img_list[i] = self.img_list[i], self.img_list[i - 1]
        txt = self.img_listbox.get(i)
        self.img_listbox.delete(i)
        self.img_listbox.insert(i - 1, txt)
        self.img_listbox.selection_set(i - 1)

    def _img_move_down(self):
        sel = self.img_listbox.curselection()
        if not sel:
            return
        i = sel[0]
        if i >= len(self.img_list) - 1:
            return
        self.img_list[i + 1], self.img_list[i] = self.img_list[i], self.img_list[i + 1]
        txt = self.img_listbox.get(i)
        self.img_listbox.delete(i)
        self.img_listbox.insert(i + 1, txt)
        self.img_listbox.selection_set(i + 1)

    def _on_one_pdf_toggle(self):
        # Ajusta label + comportamento de escolha
        if self.one_pdf_var.get():
            self.img_out_label.configure(text="Salvar PDF final em:")
            if self.img_list and (not self.img_out_var.get().strip() or Path(self.img_out_var.get()).is_dir()):
                first = self.img_list[0]
                self.img_out_var.set(str(first.with_name(f"{first.stem}_IMAGENS.pdf")))
        else:
            self.img_out_label.configure(text="Salvar PDFs na pasta:")
            if self.img_list and (not self.img_out_var.get().strip() or self.img_out_var.get().strip().lower().endswith(".pdf")):
                self.img_out_var.set(str(self.img_list[0].parent))

    def _pick_img_output(self):
        if self.one_pdf_var.get():
            path = filedialog.asksaveasfilename(title="Salvar PDF como", defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
            if path:
                self.img_out_var.set(path)
        else:
            folder = filedialog.askdirectory(title="Escolha a pasta para salvar os PDFs")
            if folder:
                self.img_out_var.set(folder)

    def _do_images_convert(self):
        try:
            if not self.img_list:
                raise ValueError("Adicione imagens na lista (arraste e solte ou use o botão).")
            if not self.img_out_var.get().strip():
                raise ValueError("Escolha o destino de saída.")

            if self.one_pdf_var.get():
                out_pdf = _safe_pdf_path(self.img_out_var.get())
                convert_images_to_one_pdf(self.img_list, out_pdf)
                messagebox.showinfo("Concluído", f"PDF único gerado com sucesso:\n{out_pdf}")
            else:
                out_dir = Path(self.img_out_var.get().strip().strip('"'))
                out_dir.mkdir(parents=True, exist_ok=True)

                ok = 0
                for img in self.img_list:
                    out_pdf = out_dir / f"{img.stem}.pdf"
                    convert_image_to_pdf_single(img, out_pdf)
                    ok += 1

                messagebox.showinfo("Concluído", f"PDFs gerados com sucesso: {ok}\nPasta:\n{out_dir}")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ===================== Aba 2: Juntar PDFs =====================

    def _build_tab_merge(self, parent: ttk.Frame):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        top = ttk.Frame(parent)
        top.grid(row=0, column=0, sticky="ew", padx=8, pady=(12, 6))
        top.columnconfigure(0, weight=1)

        ttk.Button(top, text="Adicionar PDFs...", command=self._add_pdfs).grid(row=0, column=0, sticky="w")
        ttk.Button(top, text="Remover selecionado", command=self._remove_selected).grid(row=0, column=1, padx=8)
        ttk.Button(top, text="Limpar lista", command=self._clear_list).grid(row=0, column=2)

        mid = ttk.Frame(parent)
        mid.grid(row=1, column=0, sticky="nsew", padx=8, pady=6)
        mid.columnconfigure(0, weight=1)
        mid.rowconfigure(1, weight=1)

        ttk.Label(mid, text="Arraste e solte PDFs aqui (a ordem da lista será a ordem final):").grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.pdf_list: list[Path] = []
        self.listbox = tk.Listbox(mid, selectmode=tk.SINGLE)
        self.listbox.grid(row=1, column=0, sticky="nsew")

        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self._on_drop_pdfs)

        sb = ttk.Scrollbar(mid, orient="vertical", command=self.listbox.yview)
        sb.grid(row=1, column=1, sticky="ns")
        self.listbox.configure(yscrollcommand=sb.set)

        buttons = ttk.Frame(mid)
        buttons.grid(row=1, column=2, sticky="ns", padx=(10, 0))
        ttk.Button(buttons, text="↑ Subir", command=self._move_up).grid(row=0, column=0, pady=(0, 6), sticky="ew")
        ttk.Button(buttons, text="↓ Descer", command=self._move_down).grid(row=1, column=0, pady=(0, 6), sticky="ew")

        bottom = ttk.Frame(parent)
        bottom.grid(row=2, column=0, sticky="ew", padx=8, pady=(10, 6))
        bottom.columnconfigure(1, weight=1)

        ttk.Label(bottom, text="Salvar PDF final em:").grid(row=0, column=0, sticky="w")
        self.merge_out_var = tk.StringVar()
        ttk.Entry(bottom, textvariable=self.merge_out_var).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(bottom, text="Escolher...", command=self._pick_merge_out).grid(row=0, column=2)

        ttk.Button(parent, text="Juntar PDFs", command=self._do_merge).grid(row=3, column=0, pady=(8, 12))

    def _add_pdf_path(self, pdf_path: Path):
        try:
            rp = str(pdf_path.resolve())
        except Exception:
            rp = str(pdf_path)

        if rp in self._merge_seen:
            return

        self._merge_seen.add(rp)
        self.pdf_list.append(pdf_path)
        self.listbox.insert(tk.END, pdf_path.name)

        if not self.merge_out_var.get().strip():
            self.merge_out_var.set(str(pdf_path.with_name(f"{pdf_path.stem}_JUNTADO.pdf")))

    def _on_drop_pdfs(self, event):
        paths = _parse_dnd_files(event.data)
        for p in paths:
            if p.lower().endswith(".pdf"):
                self._add_pdf_path(Path(p))
        return "break"

    def _add_pdfs(self):
        paths = filedialog.askopenfilenames(title="Selecione PDFs para juntar (ordem importa)", filetypes=[("PDF", "*.pdf")])
        for p in paths:
            self._add_pdf_path(Path(p))

    def _remove_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        removed = self.pdf_list[idx]
        self.listbox.delete(idx)
        del self.pdf_list[idx]

        try:
            rp = str(removed.resolve())
        except Exception:
            rp = str(removed)
        self._merge_seen.discard(rp)

    def _clear_list(self):
        self.listbox.delete(0, tk.END)
        self.pdf_list.clear()
        self._merge_seen.clear()

    def _move_up(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        i = sel[0]
        if i <= 0:
            return
        self.pdf_list[i - 1], self.pdf_list[i] = self.pdf_list[i], self.pdf_list[i - 1]
        txt = self.listbox.get(i)
        self.listbox.delete(i)
        self.listbox.insert(i - 1, txt)
        self.listbox.selection_set(i - 1)

    def _move_down(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        i = sel[0]
        if i >= len(self.pdf_list) - 1:
            return
        self.pdf_list[i + 1], self.pdf_list[i] = self.pdf_list[i], self.pdf_list[i + 1]
        txt = self.listbox.get(i)
        self.listbox.delete(i)
        self.listbox.insert(i + 1, txt)
        self.listbox.selection_set(i + 1)

    def _pick_merge_out(self):
        path = filedialog.asksaveasfilename(title="Salvar PDF final como", defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if path:
            self.merge_out_var.set(path)

    def _ask_password(self, filename: str) -> str | None:
        return simpledialog.askstring("PDF protegido", f"Informe a senha do PDF:\n{filename}", show="*")

    def _do_merge(self):
        try:
            if not self.merge_out_var.get().strip():
                raise ValueError("Escolha o caminho de saída do PDF final.")
            out_path = _safe_pdf_path(self.merge_out_var.get())
            merge_pdfs(self.pdf_list, out_path, password_cb=self._ask_password)
            messagebox.showinfo("Concluído", f"PDF juntado com sucesso:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    App().mainloop()