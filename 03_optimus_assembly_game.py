"""Optimus Bot Factory Precision Assembly Game
Parts ride the conveyor. Press SPACE when a part is centered under the robot arm. 3 defects = shutdown."""
import tkinter as tk, random
W, H, TX, CY = 900, 520, 450, 380
KINDS = [("Actuator", "#e55", 70), ("Battery", "#5c5", 56), ("Torso", "#58f", 90), ("Joint", "#fa3", 44), ("Sensor", "#c6f", 50)]

class Game:
    def __init__(s, root):
        s.c = tk.Canvas(root, width=W, height=H, bg="#151a20", highlightthickness=0); s.c.pack()
        root.bind("<space>", s.place); root.bind("r", lambda e: s.reset())
        s.best = 0; s.reset(); s.last = None; s.loop()
    def reset(s):
        s.parts, s.asm, s.score, s.units, s.strikes, s.combo = [], [], 0, 0, 0, 0
        s.spawn, s.placed, s.arm, s.msg, s.over = 0.0, 0, 0.0, "", False
    def speed(s): return 150 + 7 * s.placed
    def place(s, e=None):
        if s.over: return
        cand = [p for p in s.parts if abs(p["x"] - TX) <= 80]
        if not cand: s.msg = "Nothing in range"; s.combo = 0; return
        p = min(cand, key=lambda q: abs(q["x"] - TX))
        dx = p["x"] - TX; prec = max(0, 100 - abs(dx) / 80 * 100)
        s.parts.remove(p); s.placed += 1; s.arm = 0.25
        if abs(dx) > 40:
            s.strikes += 1; s.combo = 0; s.msg = f"MISALIGNED ({prec:.0f}%) - defect!"
        else:
            s.combo = s.combo + 1 if prec >= 90 else 0
            s.score += int(prec) + 10 * s.combo; s.msg = f"Precision {prec:.0f}%  combo x{s.combo}"
            s.asm.append((p["color"], dx, p["name"]))
            if len(s.asm) >= 5: s.units += 1; s.score += 100; s.asm = []
        if s.strikes >= 3: s.over = True; s.best = max(s.best, s.score)
    def loop(s):
        dt = 0.016
        if not s.over:
            s.spawn -= dt
            if s.spawn <= 0:
                n, col, w = random.choice(KINDS); s.parts.append({"x": -50.0, "name": n, "color": col, "w": w})
                s.spawn = max(0.7, 1.6 - s.placed * 0.02) + random.random() * 0.5
            for p in s.parts: p["x"] += s.speed() * dt
            for p in s.parts[:]:
                if p["x"] > W + 60: s.parts.remove(p); s.strikes += 1; s.combo = 0; s.msg = "Part missed - defect!"
            if s.strikes >= 3: s.over = True; s.best = max(s.best, s.score)
            s.arm = max(0, s.arm - dt)
        s.draw(); s.c.after(16, s.loop)
    def draw(s):
        c = s.c; c.delete("all")
        c.create_rectangle(0, CY + 30, W, CY + 60, fill="#333"); 
        for x in range(-40, W, 40): c.create_line(x + (s.placed * 0) , CY + 30, x, CY + 60, fill="#444")
        c.create_rectangle(TX - 80, CY - 60, TX + 80, CY + 30, outline="#3af", dash=(4, 4)); c.create_line(TX, CY - 70, TX, CY + 30, fill="#3af")
        for p in s.parts:
            c.create_rectangle(p["x"] - p["w"] / 2, CY - 20, p["x"] + p["w"] / 2, CY + 30, fill=p["color"], outline="white")
            c.create_text(p["x"], CY + 5, text=p["name"], fill="black", font=("Arial", 8, "bold"))
        tip = CY - 90 + (50 if s.arm > 0 else 0)
        c.create_line(TX, 20, TX, tip, fill="#bbb", width=8); c.create_oval(TX - 14, tip - 6, TX + 14, tip + 14, fill="#999")
        c.create_text(700, 40, text="ASSEMBLY (5 parts = 1 bot)", fill="white")
        for i, (col, dx, n) in enumerate(s.asm):
            y = 230 - i * 30; c.create_rectangle(700 + dx - 40, y, 700 + dx + 40, y + 26, fill=col, outline="white"); c.create_text(700 + dx, y + 13, text=n, font=("Arial", 8, "bold"))
        c.create_line(700, 60, 700, 250, fill="#555", dash=(2, 4))
        c.create_text(10, 10, anchor="nw", fill="white", font=("Consolas", 13), text=f"SCORE {s.score}   BOTS {s.units}   DEFECTS {s.strikes}/3   BEST {s.best}")
        c.create_text(W / 2, 470, text=s.msg, fill="#8f8", font=("Arial", 14))
        if s.over: c.create_text(W / 2, 150, text="LINE SHUTDOWN - press R", fill="red", font=("Arial", 30, "bold"))
root = tk.Tk(); root.title("Optimus Bot Assembly"); Game(root); root.mainloop()
