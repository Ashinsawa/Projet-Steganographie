import tkinter as tk
from tkinter import filedialog, messagebox

# On réutilise les fonctions 
from cacher import cacher_message
from extraire import extraire_message

# ----------------------------
# Fenêtre principale
# ----------------------------
root = tk.Tk()# Crée la fenêtre
root.title("Stéganographie - LSB (MNS)") # Titre de la fenêtre
root.geometry("600x450") # Taille (largeur x hauteur)

# ----------------------------
# Variable Tkinter (stockent du texte lié aux widgets)
# ----------------------------
encode_image_path = tk.StringVar() # chemin image à encoder
decode_image_path = tk.StringVar() # chemin image à décoder

# ----------------------------
# Fonctions appelées par les boutons
# ----------------------------
def choisir_image_a_encoder():
    """
    Ouvre un explorateur de fichiers pour choisir une image.
    Le chemin choisi est stocké dans encode_image_path.
    """
    path = filedialog.askopenfilename(
        title="Choisir une image (PNG)",
        filetypes=[("Images PNG", "*.png"), ("Toutes les images", "*.png;*.jpg;*.jpeg"), ("Tous les fichiers", "*.*")]
    )
    if path: # si l'utilisateur n'a pas annulé
        encode_image_path.set(path)

def choisir_image_a_decoder():
    """
    Même idée, mais pour décoder.
    """
    path = filedialog.askopenfilename(
        title="Choisir une image à décoder (PNG)",
        filetypes=[("Images PNG", "*.png"), ("Toutes les images", "*.png;*.jpg;*.jpeg"), ("Tous les fichiers", "*.*")]
    )
    if path: 
        decode_image_path.set(path)

def action_cacher_message():
    """
    Récupère le chemin de l'image + le texte dans la zone,
    puis demande où enregistrer la nouvelle image encodée.
    """
    img_path = encode_image_path.get()

    # Récupère le message tapé dans le widget Text (du début à la fin)
    msg = text_message.get("1.0", tk.END).strip()

    if not img_path:
        messagebox.showwarning("Attention", "Choisis une image à encoder.")
        return
    
    if not msg:
        messagebox.showwarning("Attention", "Tape un message à cacher.")
        return
    
    # Demande où sauvegarder l'image encodée
    output_path = filedialog.asksaveasfilename(
        title="Enregistrer l'image encodée",
        defaultextension=".png",
        filetypes=[("Images PNG", "*.png")],
        initialfile="image_codee.png"
    )

    if not output_path:
        return # l'utilisateur a annulé
    
    try:
        cacher_message(img_path, msg, output_path)
        messagebox.showinfo("OK", f"Message caché dans :\n{output_path}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")
    

def action_extraire_message():
    """
    Lit le chemin de l'image sélectionnée, extrait le message,
    puis l'affiche dans la zone de résultat.
    """
    img_path = decode_image_path.get()

    if not img_path:
        messagebox.showwarning("Attention", "Choisis une image à décoder.")
        return
    
    try:
        msg = extraire_message(img_path)
        # Efface l'ancienne sortie puis écrit la nouvelle
        text_resultat.delete("1.0, tk.END")
        text_resultat.insert(tk.END, msg)
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur", f"Une erreur est survenue :\n{e}")


# ----------------------------
# Interface - Partie 3a : Encoder
# ----------------------------
label_a = tk.Label(root, text="Cacher un message dans une image", font=("Arial", 12, "bold"))
label_a.pack(pady=(10, 5))

frame_encode = tk.Frame(root)
frame_encode.pack(fill="x", padx=10)

btn_choisir_encode = tk.Button(frame_encode, text="Choisir image", command=choisir_image_a_encoder)
btn_choisir_encode.pack(side="left")

entry_encode = tk.Entry(frame_encode, textvariable=encode_image_path)
entry_encode.pack(side="left", fill="x", expand=True, padx=10)

label_msg = tk.Label(root, text="Message à cacher :")
label_msg.pack(anchor="w", padx=10)

text_message = tk.Text(root, height=4)
text_message.pack(fill="x", padx=10)

btn_cacher = tk.Button(root, text="Cacher le message (générer image encodée)", command=action_cacher_message)
btn_cacher.pack(pady=10)


# Séparateur visuel
sep = tk.Label(root, text="-" * 80)
sep.pack(pady=5)


# ----------------------------
# Interface - Partie 3b : Decoder
# ----------------------------
label_b = tk.Label(root, text="Extraire un message d'une image", font=("Arial", 12, "bold"))
label_b.pack(pady=(5, 5))

frame_decode = tk.Frame(root)
frame_decode.pack(fill="x", padx=10)

btn_choisir_decode = tk.Button(frame_decode, text="Choisir image", command=choisir_image_a_decoder)
btn_choisir_decode.pack(side="left")

entry_decode = tk.Entry(frame_decode, textvariable=decode_image_path)
entry_decode.pack(side="left", fill="x", expand=True, padx=10)

btn_extraire = tk.Button(root, text="Extraire le message", command=action_extraire_message)
btn_extraire.pack(pady=10)

label_res = tk.Label(root, text="Message trouvé :")
label_res.pack(anchor="w", padx=10)

text_resultat = tk.Text(root, height=6)
text_resultat.pack(fill="both", expand=True, padx=10, pady=(0, 10))


# ----------------------------
# Boucle principale Tkinter
# ----------------------------
root.mainloop() # Garde la fenêtre ouverte et gère les clics