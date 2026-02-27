import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

from steg_image_nb import cacher_image_nb, extraire_image_nb, image_nb_to_bits

root = tk.Tk()
root.title("Partie 3 - Cacher une image N&B")
root.geometry("750x520")
root.minsize(700, 500)

host_path = tk.StringVar()
secret_path = tk.StringVar()
seed_var = tk.StringVar()

decode_host_path = tk.StringVar()
decode_seed_var = tk.StringVar()

info_var = tk.StringVar(value="Sélectionne une image porteuse + une image N&B + une graine.")

def choisir_host():
    p = filedialog.askopenfilename(title="Choisir image porteuse", filetypes=[("PNG", "*.png"), ("Tous fichiers", "*.*")])
    if p:
        host_path.set(p)
        update_infos()

def choisir_secret():
    p = filedialog.askopenfilename(title="Choisir image N&B (logo)", filetypes=[("PNG", "*.png"), ("Tous fichiers", "*.*")])
    if p:
        secret_path.set(p)
        update_infos()

def update_infos():
    try:
        if not host_path.get() or not secret_path.get():
            return

        host = Image.open(host_path.get())
        W, H = host.size
        cap = W * H  # 1 bit/pixel

        w, h, bits = image_nb_to_bits(secret_path.get())
        total_bits = 16 + (w * h)
        ratio = total_bits / cap

        info_var.set(
            f"Porteuse: {W}x{H} (capacité ≈ {cap} bits)\n"
            f"Image cachée: {w}x{h} => {w*h} bits (+16 bits en-tête)\n"
            f"Total bits à cacher: {total_bits}\n"
            f"Ratio: {ratio:.6f} (≈ {ratio*100:.4f}%)"
        )
    except Exception as e:
        info_var.set(f"Erreur infos: {e}")

def action_cacher():
    if not host_path.get() or not secret_path.get():
        messagebox.showwarning("Attention", "Choisis l'image porteuse ET l'image à cacher.")
        return
    if not seed_var.get().strip():
        messagebox.showwarning("Attention", "Tape une graine (mot de passe).")
        return

    out = filedialog.asksaveasfilename(
        title="Enregistrer l'image encodée",
        defaultextension=".png",
        filetypes=[("PNG", "*.png")],
        initialfile="image_avec_logo_cache.png"
    )
    if not out:
        return

    try:
        cacher_image_nb(host_path.get(), secret_path.get(), out, seed_var.get().strip())
        messagebox.showinfo("OK", f"Image cachée dans :\n{out}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def choisir_decode_host():
    p = filedialog.askopenfilename(title="Choisir image encodée", filetypes=[("PNG", "*.png"), ("Tous fichiers", "*.*")])
    if p:
        decode_host_path.set(p)

def action_extraire():
    if not decode_host_path.get():
        messagebox.showwarning("Attention", "Choisis une image encodée à décoder.")
        return
    if not decode_seed_var.get().strip():
        messagebox.showwarning("Attention", "Tape la graine.")
        return

    out = filedialog.asksaveasfilename(
        title="Enregistrer l'image extraite",
        defaultextension=".png",
        filetypes=[("PNG", "*.png")],
        initialfile="logo_extrait.png"
    )
    if not out:
        return

    try:
        extraire_image_nb(decode_host_path.get(), out, decode_seed_var.get().strip())
        messagebox.showinfo("OK", f"Image extraite :\n{out}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))


# -------- UI --------
tk.Label(root, text="ENCODAGE : cacher une image N&B dans une image", font=("Arial", 12, "bold")).pack(pady=(10, 5))

f1 = tk.Frame(root); f1.pack(fill="x", padx=10)
tk.Button(f1, text="Choisir image porteuse", command=choisir_host).pack(side="left")
tk.Entry(f1, textvariable=host_path).pack(side="left", fill="x", expand=True, padx=10)

f2 = tk.Frame(root); f2.pack(fill="x", padx=10, pady=(5, 0))
tk.Button(f2, text="Choisir image à cacher (logo)", command=choisir_secret).pack(side="left")
tk.Entry(f2, textvariable=secret_path).pack(side="left", fill="x", expand=True, padx=10)

f3 = tk.Frame(root); f3.pack(fill="x", padx=10, pady=(5, 0))
tk.Label(f3, text="Graine :").pack(side="left")
tk.Entry(f3, textvariable=seed_var).pack(side="left", fill="x", expand=True, padx=10)

tk.Label(root, textvariable=info_var, justify="left").pack(anchor="w", padx=10, pady=(8, 0))

tk.Button(root, text="Cacher l'image N&B (générer image encodée)", command=action_cacher).pack(pady=10)

tk.Label(root, text="-" * 110).pack(pady=6)

tk.Label(root, text="DECODAGE : extraire l'image N&B", font=("Arial", 12, "bold")).pack(pady=(5, 5))

f4 = tk.Frame(root); f4.pack(fill="x", padx=10)
tk.Button(f4, text="Choisir image encodée", command=choisir_decode_host).pack(side="left")
tk.Entry(f4, textvariable=decode_host_path).pack(side="left", fill="x", expand=True, padx=10)

f5 = tk.Frame(root); f5.pack(fill="x", padx=10, pady=(5, 0))
tk.Label(f5, text="Graine :").pack(side="left")
tk.Entry(f5, textvariable=decode_seed_var).pack(side="left", fill="x", expand=True, padx=10)

tk.Button(root, text="Extraire l'image cachée", command=action_extraire).pack(pady=10)

root.mainloop()