from PIL import Image
import random


def iter_points_aleatoires(largeur, hauteur, graine):
    """
    Génère des positions (x,y) uniques dans un ordre pseudo-aléatoire,
    déterministe grâce à la graine.
    -> Très important : même graine => même ordre => on peut décoder.
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
    Ouvre une image, la convertit en noir & blanc, puis renvoie :
    (w, h, bits_pixels)
    bits_pixels = string de '0'/'1' de longueur w*h.
    """
    img = Image.open(secret_image_path).convert("L")  # niveaux de gris
    w, h = img.size

    # Limite imposée par l'en-tête 16 bits (8 bits largeur + 8 bits hauteur)
    if w > 255 or h > 255:
        raise ValueError("Image cachée trop grande (max 255x255).")

    # Seuil : >128 => blanc, sinon noir
    pix = img.load()
    bits = []
    for y in range(h):
        for x in range(w):
            bits.append("1" if pix[x, y] > 128 else "0")

    return w, h, "".join(bits)


def bits_to_image_nb(w, h, bits, output_path):
    """
    Reconstruit une image N&B (mode L) à partir d'une chaîne de bits.
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
    Cache l'image N&B (secret) dans l'image host en modifiant le LSB du rouge.
    Format stocké :
      - 16 bits : largeur (8) + hauteur (8)
      - puis w*h bits : pixels N&B
    """
    host = Image.open(host_image_path).convert("RGBA")
    pixels = host.load()
    W, H = host.size

    w, h, secret_bits = image_nb_to_bits(secret_image_path)

    header = format(w, "08b") + format(h, "08b")  # 16 bits
    bits_a_cacher = header + secret_bits

    # Capacité : 1 bit par pixel (canal rouge)
    if len(bits_a_cacher) > W * H:
        raise ValueError("Image porteuse trop petite pour cacher cette image N&B.")

    points = iter_points_aleatoires(W, H, graine)

    for bit in bits_a_cacher:
        x, y = next(points)
        r, g, b, a = pixels[x, y]
        pixels[x, y] = ((r & ~1) | int(bit), g, b, a)

    host.save(output_path)


def extraire_image_nb(host_image_path, output_path, graine):
    """
    Extrait une image N&B cachée dans host, grâce à la graine.
    Lis :
      - 16 bits -> w,h
      - puis w*h bits -> pixels
    Puis reconstruit l'image et la sauvegarde.
    """
    host = Image.open(host_image_path).convert("RGBA")
    pixels = host.load()
    W, H = host.size

    points = iter_points_aleatoires(W, H, graine)

    # Lire l'en-tête 16 bits
    header_bits = ""
    for _ in range(16):
        x, y = next(points)
        r, g, b, a = pixels[x, y]
        header_bits += str(r & 1)

    w = int(header_bits[:8], 2)
    h = int(header_bits[8:], 2)

    if w == 0 or h == 0 or w > 255 or h > 255:
        raise ValueError("En-tête invalide (mauvaise graine ou image non encodée).")

    total = w * h

    # Lire les bits de l'image
    bits_pixels = ""
    for _ in range(total):
        x, y = next(points)
        r, g, b, a = pixels[x, y]
        bits_pixels += str(r & 1)

    bits_to_image_nb(w, h, bits_pixels, output_path)