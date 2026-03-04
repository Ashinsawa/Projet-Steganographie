from PIL import Image
import random

# ------------------------------------------------------------
# extraire.py
# Objectif :
# - Lire les bits cachés dans le LSB du rouge, dans le même ordre aléatoire (même graine)
# - Reconstituer le message jusqu'au marqueur de fin (64 bits)
# ------------------------------------------------------------

def iter_points_aleatoires(largeur, hauteur, graine):
    """
    ATTENTION : doit être identique à cacher.py.
    Sinon, on ne relit pas les bits au même endroit => message impossible à retrouver.
    """
    n = largeur * hauteur
    rng = random.Random(graine)
    swaps = {}

    for i in range(n):
        j = rng.randrange(i, n)

        val_i = swaps.get(i, i)
        val_j = swaps.get(j, j)

        swaps[i] = val_j
        swaps[j] = val_i

        idx = swaps[i]
        x = idx % largeur
        y = idx // largeur
        yield (x, y)

def extraire_message(image_path, graine):
    """
    Extrait un message texte depuis une image encodée.

    - Parcourt les pixels dans un ordre pseudo-aléatoire dépendant de la graine.
    - Récupère le LSB du rouge (r & 1) pour reconstruire une suite de bits.
    - S'arrête quand on détecte le marqueur de fin (64 bits).
    """
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size

    bits_extraits = ""    # On empile les bits trouvés ("0"/"1")
    message_final = ""    # Message reconstruit en texte
    marqueur_fin = '1111111111111110' * 4  # doit être identique à cacher.py

    for (x, y) in iter_points_aleatoires(width, height, graine):
        r, g, b, a = pixels[x, y]

        # r & 1 -> récupère le dernier bit du rouge (0 ou 1)
        bits_extraits += str(r & 1)

        # Quand la fin de bits_extraits correspond au marqueur, on stoppe
        if bits_extraits.endswith(marqueur_fin):
            # On enlève le marqueur pour garder uniquement les bits du message
            bits_utiles = bits_extraits[:-len(marqueur_fin)]

            # On regroupe par 8 bits => 1 caractère ASCII
            for i in range(0, len(bits_utiles), 8):
                octet = bits_utiles[i:i+8]        # ex: "01000001"
                message_final += chr(int(octet, 2)) # binaire -> int -> char

            return message_final

    # Si on n'a jamais trouvé le marqueur : pas de message valide (ou mauvaise graine)
    return "Aucun marqueur de fin trouvé."

if __name__ == "__main__":
    print(extraire_message("images/image1_codee.png", "mdp123"))