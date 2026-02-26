from PIL import Image
import random

def message_to_bin(message):
    return ''.join(format(ord(i), '08b') for i in message)

def iter_points_aleatoires(largeur, hauteur, graine):
    """
    Génère une permutation pseudo-aléatoire des pixels (x, y) basée sur la graine.
    IMPORTANT : pas de grosse liste -> ça évite de freezer.
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

def cacher_message(image_path, message, output_path, graine):
    img = Image.open(image_path).convert("RGBA")

    marqueur_fin = '1111111111111110' * 4  # 64 bits
    binary_msg = message_to_bin(message) + marqueur_fin

    pixels = img.load()
    width, height = img.size

    # Capacité: 1 bit / pixel (canal rouge)
    if len(binary_msg) > width * height:
        raise ValueError("Message trop long pour cette image.")

    points = iter_points_aleatoires(width, height, graine)

    for bit in binary_msg:
        x, y = next(points)
        r, g, b, a = pixels[x, y]
        nouveau_r = (r & ~1) | int(bit)
        pixels[x, y] = (nouveau_r, g, b, a)

    img.save(output_path)
    print(f"Message caché dans {output_path}")

if __name__ == "__main__":
    cacher_message("images/image1.png", "Mon message secret", "images/image1_codee.png", "mdp123")
