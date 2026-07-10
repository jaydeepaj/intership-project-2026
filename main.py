import os
import hashlib
import customtkinter as ctk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PIL import Image

class ImageEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Image Encryptor")
        self.root.geometry("900x600")

        self.selected_file = None

        title = ctk.CTkLabel(root, text="CYBER IMAGE ENCRYPTOR", font=("Consolas", 28, "bold"))
        title.pack(pady=15)

        self.select_btn = ctk.CTkButton(root, text="Select Image/File", command=self.select_file)
        self.select_btn.pack(pady=10)

        self.file_label = ctk.CTkLabel(
            root,
            text="No file selected"
        )
        self.file_label.pack()

        self.preview_label = ctk.CTkLabel(
            root,
            text=""
        )
        self.preview_label.pack(pady=10)

        self.password = ctk.CTkEntry(root, placeholder_text="Enter Password", show="*", width=300)
        self.password.pack(pady=10)

        self.encrypt_btn = ctk.CTkButton(root, text="Encrypt", command=self.encrypt_file)
        self.encrypt_btn.pack(pady=5)

        self.decrypt_btn = ctk.CTkButton(root, text="Decrypt", command=self.decrypt_file)
        self.decrypt_btn.pack(pady=5)

        self.hash_btn = ctk.CTkButton(root, text="Generate SHA256", command=self.generate_hash)
        self.hash_btn.pack(pady=5)

        self.logs = ctk.CTkTextbox(root, width=700, height=250)
        self.logs.pack(pady=20)

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

        with open(self.selected_file, "rb") as f:
            data = f.read()

        salt = os.urandom(16)
        nonce = os.urandom(12)

        key = self.derive_key(password, salt)
        encrypted = AESGCM(key).encrypt(nonce, data, None)

        out_file = self.selected_file + ".enc"

        with open(out_file, "wb") as f:
            f.write(salt + nonce + encrypted)

        self.log(f"Encrypted -> {out_file}")

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