from PIL import Image
import random

def iter_points_aleatoires(largeur, hauteur, graine):
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
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size

    bits_extraits = ""
    message_final = ""
    marqueur_fin = '1111111111111110' * 4  # doit être identique à cacher.py

    for (x, y) in iter_points_aleatoires(width, height, graine):
        r, g, b, a = pixels[x, y]
        bits_extraits += str(r & 1)

        if bits_extraits.endswith(marqueur_fin):
            bits_utiles = bits_extraits[:-len(marqueur_fin)]

            for i in range(0, len(bits_utiles), 8):
                octet = bits_utiles[i:i+8]
                message_final += chr(int(octet, 2))

            return message_final

    return "Aucun marqueur de fin trouvé."

if __name__ == "__main__":
    print(extraire_message("images/image1_codee.png", "mdp123"))
