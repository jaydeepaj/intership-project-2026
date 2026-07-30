import os
import hashlib
import customtkinter as ctk
import tkinter as tk
import random
import math
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PIL import Image

class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Cyber Image Encryptor ⚡")
        self.root.geometry("1200x750")
        ctk.set_default_color_theme("blue")

        self.radar_canvas = tk.Canvas(
            self.root,
            width=400,
            height=400,
            bg="black",
            highlightthickness=0
        )

        self.radar_canvas.pack(pady=10)

        self.radar_canvas.place(
            x=20,
            y=120
        )
        
        self.angle = 0

        self.animate_rings()

        self.selected_file = None

        title = ctk.CTkLabel(root, text="⚡ CYBER IMAGE ENCRYPTOR ⚡", font=("Consolas", 32, "bold"), text_color="#00ffff")
        title.pack(pady=20)

        self.main_frame = ctk.CTkScrollableFrame(
            self.root,
            corner_radius=20,
            border_width=2,
            border_color="#00FFFF"
        )
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            self.main_frame,
            text="╔══",
            text_color="#00FFFF",
            font=("Consolas", 24)
        ).place(x=5, y=5)

        ctk.CTkLabel(
            self.main_frame,
            text="══╗",
            text_color="#00FFFF",
            font=("Consolas", 24)
        ).place(relx=1, x=-60, y=5)

        ctk.CTkLabel(
            self.main_frame,
            text="╚══",
            text_color="#00FFFF",
            font=("Consolas", 24)
        ).place(x=5, rely=1, y=-40)

        ctk.CTkLabel(
           self.main_frame,
           text="══╝",
           text_color="#00FFFF",
           font=("Consolas", 24)
        ).place(relx=1, x=-60, rely=1, y=-40)

        self.status = ctk.CTkLabel(
            self.main_frame,
            text="🟢 AES-256 ACTIVE",
            text_color="#00FF88",
            font=("Consolas", 14, "bold")
        )
        self.status.pack(pady=5)

        self.select_btn = ctk.CTkButton(
            self.main_frame,
            text="📂 Select Image",
            command=self.select_file,
            width=250,
            height=40
        )
        self.select_btn.pack(pady=10)

        self.file_label = ctk.CTkLabel(
            root,
            text="No file selected"
        )
        self.file_label.pack()

        self.preview_frame = ctk.CTkFrame(
            self.main_frame,
            width=320,
            height=320,
            border_width=2,
            border_color="#00FFFF"
        )
        self.preview_frame.pack(pady=10)

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="IMAGE PREVIEW"
        )
        self.preview_label.pack(expand=True)
        self.preview_label.pack(pady=10)

        self.password = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="🔑 Enter Secret Password",
            width=350,
            height=40,
            show="*"
        )
        self.password.pack(pady=15)

        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10)

        self.encrypt_btn = ctk.CTkButton(
            btn_frame,
            text="🔒 Encrypt",
            width=180,
            command=self.encrypt_file
        )
        self.encrypt_btn.pack(side="left", padx=10)

        self.decrypt_btn = ctk.CTkButton(
            btn_frame,
            text="🔓 Decrypt",
            width=180,
            command=self.decrypt_file
        )
        self.decrypt_btn.pack(side="left", padx=10)

        self.hash_btn = ctk.CTkButton(root, text="Generate SHA256", command=self.generate_hash)
        self.hash_btn.pack(pady=5)

        self.logs = ctk.CTkTextbox(self.main_frame, width=900, height=220, font=("Consolas", 12))
        self.logs.pack(pady=20)
   
    def draw_hexagon(self, canvas, x, y, size):
        points = []
        for i in range(6):
            angle = math.radians(60 * i)
            points.extend([
                x + size * math.cos(angle),
                y + size * math.sin(angle)
            ])

        canvas.create_polygon(
            points,
            outline="#00FFFF",
            fill="",
            width=1
        )

    def animate_rings(self):

        self.radar_canvas.delete("all")

        cx = 200
        cy = 200

        for r in [40, 70, 100]:
            self.radar_canvas.create_oval(
                cx-r, cy-r,
                cx+r, cy+r,
                outline="#00FFFF",
                width=2
            )

        x = cx + 100 * math.cos(math.radians(self.angle))
        y = cy + 100 * math.sin(math.radians(self.angle))

        self.radar_canvas.create_line(
            cx, cy,
            x, y,
            fill="#00FFFF",
            width=3
        )

        self.angle += 4

        self.root.after(
            30,
            self.animate_rings
        )
    def log(self, msg):
        self.logs.insert("end", msg + "\n")
        self.logs.see("end")

    def select_file(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.bmp *.gif")
            ]
        )

        if not path:
            return

        self.selected_file = path

        self.file_label.configure(
            text=os.path.basename(path)
        )

        image = Image.open(path)

        image.thumbnail((300, 300))

        preview = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )

        self.preview_label.configure(
            image=preview,
            text=""
        )

        self.preview_label.image = preview

        self.log(f"Selected: {path}")

    def derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        return kdf.derive(password.encode())

    def encrypt_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Select a file first")
            return

        password = self.password.get()

        if not password:
            messagebox.showerror("Error", "Enter password")
            return

        self.status.configure(text="🟡 ENCRYPTING...")
        self.root.update()

        with open(self.selected_file, "rb") as f:
            data = f.read()

        salt = os.urandom(16)
        nonce = os.urandom(12)

        key = self.derive_key(password, salt)

        encrypted = AESGCM(key).encrypt(
            nonce,
            data,
            None
        )

        out_file = self.selected_file + ".enc"

        with open(out_file, "wb") as f:
            f.write(salt + nonce + encrypted)

        self.log(f"Encrypted -> {out_file}")

        self.status.configure(
            text="🟢 ENCRYPTION COMPLETE"
        )

    def decrypt_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Select encrypted file")
            return

        password = self.password.get()
        if not password:
            messagebox.showerror("Error", "Enter password")
            return

        try:
            with open(self.selected_file, "rb") as f:
                salt = f.read(16)
                nonce = f.read(12)
                enc = f.read()

            key = self.derive_key(password, salt)
            data = AESGCM(key).decrypt(nonce, enc, None)

            out_file = self.selected_file.replace(".enc", "_decrypted")

            with open(out_file, "wb") as f:
                f.write(data)

            self.log(f"Decrypted -> {out_file}")

        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")
        
        # Decryption start
        self.status.configure(text="🟡 DECRYPTING...")
        self.root.update()

# decrypt code

        self.status.configure(text="🔓 DECRYPTION COMPLETE")

    def generate_hash(self):
        if not self.selected_file:
            return

        sha = hashlib.sha256()

        with open(self.selected_file, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                sha.update(chunk)

        self.log("SHA256: " + sha.hexdigest())


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = ImageEncryptorApp(root)
    root.mainloop()