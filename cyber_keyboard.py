import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import random, math

class CyberCommandCenter:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Command Center X")
        self.root.geometry("1400x850")
        self.root.configure(bg="#050816")

        self.count = 0
        self.start_time = datetime.now()
        self.angle = 0

        self.canvas = tk.Canvas(root, bg="#050816", highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)

        self.particles = [[random.randint(0,1400),
                           random.randint(0,850),
                           random.randint(1,4)] for _ in range(180)]

        self.main = tk.Frame(
            root,
            bg="#081120",
            highlightbackground="#00ffff",
            highlightthickness=2
        )
        self.start_btn = tk.Button(
            root,text="GET STARTED KEYBOARD VISUALIZER",
            font=("Consolas", 22, "bold"),
            bg="red",
            fg="black",
            command=self.open_dashboard
        )

        self.start_btn.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )
        

        tk.Label(
            self.main,
            text="CYBER KEYBOARD VISUALIZER",
            font=("Consolas", 26, "bold"),
            fg="#00ffff",
            bg="#081120"
        ).pack(pady=10)

        top = tk.Frame(self.main, bg="#081120")
        top.pack()

        self.clock = tk.Label(top, fg="#00ffff", bg="#081120",
                              font=("Consolas", 12, "bold"))
        self.clock.grid(row=0, column=0, padx=20)

        self.counter = tk.Label(top, text="Keys: 0",
                                fg="#00ff88", bg="#081120",
                                font=("Consolas", 12, "bold"))
        self.counter.grid(row=0, column=1, padx=20)

        self.activity = tk.Label(top, text="Activity: 0",
                                 fg="#ff66ff", bg="#081120",
                                 font=("Consolas", 12, "bold"))
        self.activity.grid(row=0, column=2, padx=20)

        self.status = tk.Label(top, text="Status: NORMAL",
                               fg="#ffd700", bg="#081120",
                               font=("Consolas", 12, "bold"))
        self.status.grid(row=0, column=3, padx=20)

        self.key_display = tk.Label(
            self.main,
            text="PRESS ANY KEY",
            font=("Consolas", 30, "bold"),
            fg="#00ffff",
            bg="#101a30",
            width=25,
            height=2
        )
        self.key_display.pack(pady=15)

        btns = tk.Frame(self.main, bg="#081120")
        btns.pack()

        tk.Button(btns, text="Clear Log",
                  command=self.clear_log).pack(side="left", padx=5)
        tk.Button(btns, text="Export Log",
                  command=self.export_log).pack(side="left", padx=5)


        log_frame = tk.Frame(self.main, bg="#081120")
        log_frame.pack(fill="both", expand=True, padx=20, pady=20)

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.log = tk.Text(
            log_frame,
            bg="#0b1324",
            fg="#e5e7eb",
            insertbackground="#00ffff",
            font=("Consolas", 11),
            yscrollcommand=scrollbar.set
        )

        self.log.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(command=self.log.yview)

        self.root.bind("<KeyPress>", self.key_pressed)

        self.animate_background()
        self.update_clock()

    def open_dashboard(self):
        self.start_btn.destroy()

        self.main.place(
            relx=0.09,
            rely=0.04,
            relwidth=0.81,
            relheight=0.85
        )

        self.root.focus_force()    

    def animate_background(self):
        self.canvas.delete("all")

        w = self.root.winfo_width()
        h = self.root.winfo_height()

        for x in range(0, w, 40):
            self.canvas.create_line(x, 0, x, h, fill="#0a2035")

        for y in range(0, h, 40):
            self.canvas.create_line(0, y, w, y, fill="#0a2035")

        for p in self.particles:
            p[1] += p[2]
            if p[1] > h:
                p[0] = random.randint(0, w)
                p[1] = 0

            self.canvas.create_oval(
                p[0], p[1], p[0]+3, p[1]+3,
                fill="#00ffff", outline=""
            )

        cx, cy = w//2, h//2

        pulse = abs(math.sin(math.radians(self.angle))) * 25

        for r in [100, 160, 220, 280]:
            self.canvas.create_oval(
                cx-r-pulse, cy-r-pulse,
                cx+r+pulse, cy+r+pulse,
                outline="#00ff88"
            )

        for layer in [120, 180]:
            pts = []
            for i in range(6):
                a = math.radians(i*60 + self.angle)
                pts.extend([
                    cx + layer * math.cos(a),
                    cy + layer * math.sin(a)
                ])
            self.canvas.create_polygon(
                pts,
                outline="#00ffff",
                fill="",
                width=2
            )

        bx = cx + 300 * math.cos(math.radians(self.angle))
        by = cy + 300 * math.sin(math.radians(self.angle))

        self.canvas.create_line(
            cx, cy, bx, by,
            fill="#00ff88",
            width=3
        )

        self.angle += 2
        self.root.after(30, self.animate_background)

    def update_clock(self):
        now = datetime.now()
        self.clock.config(text=now.strftime("%H:%M:%S"))

        elapsed = max(
            1,
            int((now - self.start_time).total_seconds())
        )

        act = int(self.count / elapsed * 60)
        self.activity.config(text=f"Activity: {act}")

        self.root.after(1000, self.update_clock)

    def key_pressed(self, event):
        self.count += 1
        self.counter.config(text=f"Keys: {self.count}")
        self.key_display.config(text=event.keysym)

        if self.count > 100:
            self.status.config(text="Status: HIGH", fg="red")
        elif self.count > 30:
            self.status.config(text="Status: MEDIUM", fg="#ff9900")

        t = datetime.now().strftime("%H:%M:%S")
        self.log.insert("1.0", f"[{t}] KEY -> {event.keysym}\n")

    def clear_log(self):
        self.log.delete("1.0", tk.END)
        self.count = 0
        self.counter.config(text="Keys: 0")
        self.status.config(text="Status: NORMAL", fg="#ffd700")

    def export_log(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(self.log.get("1.0", tk.END))

if __name__ == "__main__":
    root = tk.Tk()
    CyberCommandCenter(root)
    root.mainloop()