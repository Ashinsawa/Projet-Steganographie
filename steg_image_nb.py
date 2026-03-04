from PIL import Image
import random

# ------------------------------------------------------------
# steg_image_nb.py
# Objectif :
# - Cacher une image noir et blanc (petite) dans une image porteuse
# - Disperser les bits grâce à une graine (seed)
#
# Problème : pas de marqueur de fin possible.
# Solution : stocker la taille de l'image cachée dans les 16 premiers bits :
#   - 8 bits largeur (0..255)
#   - 8 bits hauteur (0..255)
#
# Ensuite on stocke w*h bits (1 bit/pixel N&B).
# ------------------------------------------------------------

def iter_points_aleatoires(largeur, hauteur, graine):
    """
    Même générateur de pixels que pour le texte :
    - ordre pseudo-aléatoire dépendant de la graine
    - permet de retrouver exactement les mêmes pixels au décodage
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

def image_nb_to_bits(secret_image_path):
    """
    Ouvre l'image à cacher et la convertit en niveaux de gris ("L").

    Puis on transforme en noir/blanc via un seuil :
      - pixel > 128 -> blanc -> bit 1
      - sinon -> noir -> bit 0

    Renvoie :
      (w, h, bits_pixels) où bits_pixels est une chaîne "0"/"1" de longueur w*h.
    """
    img = Image.open(secret_image_path).convert("L")
    w, h = img.size

    # En-tête 16 bits = 8 bits pour w + 8 bits pour h => w et h max = 255
    if w > 255 or h > 255:
        raise ValueError("Image cachée trop grande (max 255x255).")

    pix = img.load()
    bits = []
    for y in range(h):
        for x in range(w):
            bits.append("1" if pix[x, y] > 128 else "0")

    return w, h, "".join(bits)

def bits_to_image_nb(w, h, bits, output_path):
    """
    Reconstruit une image noir/blanc (mode 'L') depuis une chaîne de bits.
    - 1 -> blanc (255)
    - 0 -> noir (0)
    """
    out = Image.new("L", (w, h))
    pout = out.load()

    idx = 0
    for y in range(h):
        for x in range(w):
            pout[x, y] = 255 if bits[idx] == "1" else 0
            idx += 1

    out.save(output_path)

def cacher_image_nb(host_image_path, secret_image_path, output_path, graine):
    """
    Cache une image N&B dans une image porteuse :
    - On modifie le LSB du rouge (R) dans l'image porteuse.
    - 1 bit stocké par pixel.

    Format stocké :
    - 16 bits header = largeur (8 bits) + hauteur (8 bits)
    - puis w*h bits = pixels de l'image N&B
    """
    host = Image.open(host_image_path).convert("RGBA")
    pixels = host.load()
    W, H = host.size

    w, h, secret_bits = image_nb_to_bits(secret_image_path)

    # En-tête 16 bits : on encode w et h en binaire sur 8 bits chacun
    header = format(w, "08b") + format(h, "08b")
    bits_a_cacher = header + secret_bits

    # Capacité : 1 bit/pixel dans l'image porteuse
    if len(bits_a_cacher) > W * H:
        raise ValueError("Image porteuse trop petite pour cacher cette image N&B.")

    points = iter_points_aleatoires(W, H, graine)

    # On écrit bit par bit dans le LSB du rouge
    for bit in bits_a_cacher:
        x, y = next(points)
        r, g, b, a = pixels[x, y]
        pixels[x, y] = ((r & ~1) | int(bit), g, b, a)

    host.save(output_path)

def extraire_image_nb(host_image_path, output_path, graine):
    """
    Extrait une image N&B cachée dans l'image porteuse host_image_path.

    Étapes :
    1) Lire 16 bits -> reconstruire w et h
    2) Lire w*h bits -> pixels N&B
    3) Reconstruire et sauvegarder l'image extraite
    """
    host = Image.open(host_image_path).convert("RGBA")
    pixels = host.load()
    W, H = host.size

    points = iter_points_aleatoires(W, H, graine)

    # 1) Lire l'en-tête (16 bits)
    header_bits = ""
    for _ in range(16):
        x, y = next(points)
        r, g, b, a = pixels[x, y]
        header_bits += str(r & 1)

    # Les 8 premiers bits = largeur, les 8 suivants = hauteur
    w = int(header_bits[:8], 2)
    h = int(header_bits[8:], 2)

    # Vérification basique : si seed mauvaise ou image non encodée => w/h incohérents
    if w == 0 or h == 0 or w > 255 or h > 255:
        raise ValueError("En-tête invalide (mauvaise graine ou image non encodée).")

    # 2) Lire les bits des pixels N&B
    total = w * h
    bits_pixels = ""
    for _ in range(total):
        x, y = next(points)
        r, g, b, a = pixels[x, y]
        bits_pixels += str(r & 1)

    # 3) Reconstruire l'image extraite
    bits_to_image_nb(w, h, bits_pixels, output_path)