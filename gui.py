import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

from cacher import cacher_message
from extraire import extraire_message

# ----------------------------
# Fenêtre principale
# ----------------------------
root = tk.Tk()
root.title("Stéganographie - LSB (MNS)")
root.geometry("750x650")   # plus haut
root.minsize(700, 600)     # empêche une fenêtre trop petite
root.resizable(True, True) # autorise le redimensionnement

# ----------------------------
# Constantes "projet"
# ----------------------------
MARQUEUR_FIN = '1111111111111110' * 4  # 64 bits
SEUIL_RATIO = 0.001  # 0.1% = 0.001 en valeur décimale

# ----------------------------
# Variables Tkinter
# ----------------------------
encode_image_path = tk.StringVar()
decode_image_path = tk.StringVar()

encode_seed = tk.StringVar()
decode_seed = tk.StringVar()

# ----------------------------
# Helpers (calculs demandés en Q4)
# ----------------------------
def message_to_bin_len_bits(message: str) -> int:
    """
    Calcule le nombre de bits à stocker.
    Hypothèse du prof : 8 bits par caractère + marqueur de fin.
    """
    return len(message) * 8 + len(MARQUEUR_FIN)

def lire_taille_image(path: str):
    """Retourne (width, height) ou (None, None) si problème."""
    try:
        img = Image.open(path)
        return img.size  # (width, height)
    except Exception:
        return None, None

def update_encode_infos(*args):
    """
    Met à jour les labels d'infos (taille image, bits, ratio)
    dès qu'on change l'image ou le message.
    """
    path = encode_image_path.get()
    msg = text_message.get("1.0", tk.END).strip()

    if not path:
        label_img_size_val.config(text="-")
        label_bits_val.config(text="-")
        label_ratio_val.config(text="-")
        label_conclusion_val.config(text="-")
        return

    width, height = lire_taille_image(path)
    if width is None:
        label_img_size_val.config(text="Erreur lecture image")
        label_bits_val.config(text="-")
        label_ratio_val.config(text="-")
        label_conclusion_val.config(text="-")
        return

    total_pixels = width * height
    nb_bits = message_to_bin_len_bits(msg) if msg else len(MARQUEUR_FIN)  # si message vide: juste marqueur
    ratio = nb_bits / total_pixels

    label_img_size_val.config(text=f"{width} x {height} ({total_pixels} pixels)")
    label_bits_val.config(text=f"{nb_bits} bits")
    label_ratio_val.config(text=f"{ratio:.6f}  (≈ {ratio*100:.4f} %)")

    if ratio < SEUIL_RATIO:
        label_conclusion_val.config(text="✅ Ratio < 0,1% : le bruit naturel devrait masquer le message")
    else:
        label_conclusion_val.config(text="⚠️ Ratio ≥ 0,1% : le message peut être plus détectable")


# ----------------------------
# Actions boutons / sélection fichiers
# ----------------------------
def choisir_image_a_encoder():
    path = filedialog.askopenfilename(
        title="Choisir une image (PNG)",
        filetypes=[("Images PNG", "*.png"), ("Tous les fichiers", "*.*")]
    )
    if path:
        encode_image_path.set(path)
        update_encode_infos()

def choisir_image_a_decoder():
    path = filedialog.askopenfilename(
        title="Choisir une image à décoder (PNG)",
        filetypes=[("Images PNG", "*.png"), ("Tous les fichiers", "*.*")]
    )
    if path:
        decode_image_path.set(path)

def action_cacher_message():
    img_path = encode_image_path.get()
    msg = text_message.get("1.0", tk.END).strip()
    seed = encode_seed.get().strip()

    if not img_path:
        messagebox.showwarning("Attention", "Choisis une image à encoder.")
        return
    if not msg:
        messagebox.showwarning("Attention", "Tape un message à cacher.")
        return
    if not seed:
        messagebox.showwarning("Attention", "Tape une graine (mot de passe).")
        return

    output_path = filedialog.asksaveasfilename(
        title="Enregistrer l'image encodée",
        defaultextension=".png",
        filetypes=[("Images PNG", "*.png")],
        initialfile="image_codee.png"
    )
    if not output_path:
        return

    try:
        cacher_message(img_path, msg, output_path, seed)
        messagebox.showinfo("OK", f"Message caché dans :\n{output_path}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")

def action_extraire_message():
    img_path = decode_image_path.get()
    seed = decode_seed.get().strip()

    if not img_path:
        messagebox.showwarning("Attention", "Choisis une image à décoder.")
        return
    if not seed:
        messagebox.showwarning("Attention", "Tape la graine (mot de passe).")
        return

    try:
        msg = extraire_message(img_path, seed)
        text_resultat.delete("1.0", tk.END)
        text_resultat.insert(tk.END, msg)
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")


# ----------------------------
# UI - Partie Encode (Q3a + Q4)
# ----------------------------
label_a = tk.Label(root, text="Cacher un message dans une image", font=("Arial", 12, "bold"))
label_a.pack(pady=(10, 5))

frame_encode = tk.Frame(root)
frame_encode.pack(fill="x", padx=10)

btn_choisir_encode = tk.Button(frame_encode, text="Choisir image", command=choisir_image_a_encoder)
btn_choisir_encode.pack(side="left")

entry_encode = tk.Entry(frame_encode, textvariable=encode_image_path)
entry_encode.pack(side="left", fill="x", expand=True, padx=10)

# Seed encode
frame_seed_enc = tk.Frame(root)
frame_seed_enc.pack(fill="x", padx=10, pady=(5, 0))
tk.Label(frame_seed_enc, text="Graine (mot de passe) :").pack(side="left")
tk.Entry(frame_seed_enc, textvariable=encode_seed).pack(side="left", fill="x", expand=True, padx=10)

# Message
label_msg = tk.Label(root, text="Message à cacher :")
label_msg.pack(anchor="w", padx=10)

text_message = tk.Text(root, height=4)
text_message.pack(fill="x", padx=10)
text_message.bind("<KeyRelease>", lambda e: update_encode_infos())

# Infos demandées Q4
frame_infos = tk.Frame(root)
frame_infos.pack(fill="x", padx=10, pady=(8, 0))

tk.Label(frame_infos, text="Taille image :").grid(row=0, column=0, sticky="w")
label_img_size_val = tk.Label(frame_infos, text="-")
label_img_size_val.grid(row=0, column=1, sticky="w", padx=10)

tk.Label(frame_infos, text="Taille message (bits) :").grid(row=1, column=0, sticky="w")
label_bits_val = tk.Label(frame_infos, text="-")
label_bits_val.grid(row=1, column=1, sticky="w", padx=10)

tk.Label(frame_infos, text="Ratio bits / pixels :").grid(row=2, column=0, sticky="w")
label_ratio_val = tk.Label(frame_infos, text="-")
label_ratio_val.grid(row=2, column=1, sticky="w", padx=10)

label_conclusion_val = tk.Label(root, text="-")
label_conclusion_val.pack(anchor="w", padx=10, pady=(3, 0))

btn_cacher = tk.Button(root, text="Cacher le message (générer image encodée)", command=action_cacher_message)
btn_cacher.pack(pady=10)

# Séparateur
sep = tk.Label(root, text="-" * 100)
sep.pack(pady=6)

# ----------------------------
# UI - Partie Decode (Q3b)
# ----------------------------
label_b = tk.Label(root, text="Extraire un message d'une image", font=("Arial", 12, "bold"))
label_b.pack(pady=(5, 5))

frame_decode = tk.Frame(root)
frame_decode.pack(fill="x", padx=10)

btn_choisir_decode = tk.Button(frame_decode, text="Choisir image", command=choisir_image_a_decoder)
btn_choisir_decode.pack(side="left")

entry_decode = tk.Entry(frame_decode, textvariable=decode_image_path)
entry_decode.pack(side="left", fill="x", expand=True, padx=10)

# Seed decode
frame_seed_dec = tk.Frame(root)
frame_seed_dec.pack(fill="x", padx=10, pady=(5, 0))
tk.Label(frame_seed_dec, text="Graine (mot de passe) :").pack(side="left")
tk.Entry(frame_seed_dec, textvariable=decode_seed).pack(side="left", fill="x", expand=True, padx=10)

btn_extraire = tk.Button(root, text="Extraire le message", command=action_extraire_message)
btn_extraire.pack(pady=10)

label_res = tk.Label(root, text="Message trouvé :")
label_res.pack(anchor="w", padx=10)

# Frame pour mettre Text + Scrollbar côte à côte
frame_result = tk.Frame(root)
frame_result.pack(fill="both", expand=True, padx=10, pady=(0, 10))

scroll_y = tk.Scrollbar(frame_result, orient="vertical")
scroll_y.pack(side="right", fill="y")

text_resultat = tk.Text(frame_result, height=8, yscrollcommand=scroll_y.set)
text_resultat.pack(side="left", fill="both", expand=True)

scroll_y.config(command=text_resultat.yview)

# Initialise les infos
update_encode_infos()

root.mainloop()