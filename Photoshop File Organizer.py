import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font

class PersianDesignOrganizer:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.file_categories = {
            "PSD": [".psd", ".psb"],
            "وکتور": [".ai", ".eps", ".svg", ".afdesign", ".pdf"],
            "تصاویر": [".jpg", ".jpeg", ".png", ".webp", ".tiff"],
            "سه‌بعدی": [".obj", ".fbx", ".blend", ".stl", ".3ds"],
            "ویدیو": [".mp4", ".mov", ".avi", ".mkv", ".proj"],
            "UI/UX": [".xd", ".fig", ".sketch"],
            "فونت‌ها": [".ttf", ".otf", ".woff", ".woff2"],
            "بافت‌ها": [".tga", ".bmp", ".hdr", ".exr"],
            "کتابخانه‌ها": [".csl", ".ase", ".aco", ".pat"],
            "ماکاپ‌ها": [".mockup"],
            "متفرقه": []
        }

    def setup_ui(self):
        self.root.title("مرتب ساز فایل های طراحی")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        self.font_normal = ("Vazir", 10)
        self.font_title = ("Vazir", 12, "bold")
        
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5", font=self.font_normal)
        self.style.configure("TButton", font=self.font_normal, padding=6)
        self.style.configure("Title.TLabel", font=self.font_title, foreground="#2c3e50")
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(
            self.main_frame,
            text="مرتب ساز فایل های طراحی",
            style="Title.TLabel"
        ).pack()
        
        self.source_frame = ttk.Frame(self.main_frame)
        self.source_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.source_frame, text="پوشه حاوی فایل های طراحی را انتخاب کنید").pack()
        self.source_entry = ttk.Entry(self.source_frame,
                                      width=40)
        self.source_entry.pack(pady=5)

        ttk.Button(
            self.source_frame,
            text="انتخاب",
            command=self.browse_folder,
            width=10
        ).pack()

        ttk.Label(self.main_frame, text="پوشه های قابل ایجاد").pack(pady=(10, 5))
        self.folder_preview = tk.Listbox(
            self.main_frame,
            height=8,
            selectbackground="#3498db",
            bg="white",
            relief="flat",
            font=self.font_normal
        )
        self.folder_preview.pack(fill=tk.BOTH, expand=True)
        
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="آماده")
        ttk.Label(
            self.main_frame,
            textvariable=self.status_var,
            foreground="#7f8c8d",
            font=self.font_normal
        ).pack()
        
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame,
            text="شروع مرتب سازی",
            command=self.organize_files
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="بازنشانی",
            command=self.reset
        ).pack(side=tk.LEFT)

        self.label_footer = tk.Label(
            self.main_frame,
            text="DataBloom\nt.me/Data_Bloom\ngithub.com/Data-Blooom",
        )
        self.label_footer.pack()

    def browse_folder(self):
        folder = filedialog.askdirectory(title="پوشه حاوی فایل های طراحی را انتخاب کنید")
        if folder:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, folder)
            self.update_preview()

    def update_preview(self):
        self.folder_preview.delete(0, tk.END)
        folder = self.source_entry.get()
        
        if not folder or not os.path.exists(folder):
            return
            
        found_categories = set()
        
        for filename in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, filename)):
                ext = os.path.splitext(filename)[1].lower()
                for cat, exts in self.file_categories.items():
                    if ext in exts:
                        found_categories.add(cat)
                        break
        
        found_categories.add("متفرقه")
        
        for cat in sorted(found_categories):
            self.folder_preview.insert(tk.END, f"• {cat}")

    def organize_files(self):
        source = self.source_entry.get()
        if not source or not os.path.exists(source):
            messagebox.showerror("خطا", "لطفا یک پوشه معتبر انتخاب کنید")
            return
            
        total_files = len([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])
        if total_files == 0:
            messagebox.showinfo("اطلاع", "هیچ فایلی برای مرتب سازی یافت نشد")
            return
            
        self.progress["maximum"] = total_files
        processed = 0
        created_folders = set()
        
        for filename in os.listdir(source):
            src_path = os.path.join(source, filename)
            
            if os.path.isfile(src_path):
                ext = os.path.splitext(filename)[1].lower()
                category = "متفرقه"
                
                for cat, exts in self.file_categories.items():
                    if ext in exts:
                        category = cat
                        break
                
                if category not in created_folders:
                    os.makedirs(os.path.join(source, category), exist_ok=True)
                    created_folders.add(category)
                
                dest_path = os.path.join(source, category, filename)
                if os.path.exists(dest_path):
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(source, category, f"{base}_{counter}{ext}")
                        counter += 1
                
                shutil.move(src_path, dest_path)
                processed += 1
                self.progress["value"] = processed
                self.root.update()
        
        report = (
            f"تعداد {processed} فایل مرتب سازی شد\n"
            f"تعداد {len(created_folders)} پوشه ایجاد شد\n\n"
            "پوشه های ایجاد شده:\n"
            + "\n".join(f"• {cat}" for cat in sorted(created_folders))
        )
        
        messagebox.showinfo("اتمام عملیات", report)
        self.status_var.set("انجام شد!")

    def reset(self):
        self.source_entry.delete(0, tk.END)
        self.folder_preview.delete(0, tk.END)
        self.progress["value"] = 0
        self.status_var.set("آماده")

if __name__ == "__main__":
    root = tk.Tk()
    app = PersianDesignOrganizer(root)
    root.mainloop()