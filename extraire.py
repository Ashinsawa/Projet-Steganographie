from PIL import Image
import random

def generer_points_aleatoires(largeur, hauteur, nb_bits, graine):
    rng = random.Random(graine)
    indices_possibles = list(range(largeur * hauteur))
    indices_choisis = rng.sample(indices_possibles, nb_bits)

    points = []
    for i in indices_choisis:
        x = i % largeur
        y = i // largeur
        points.append((x, y))
    return points

def extraire_message(image_path, graine):
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size

    bits_extraits = ""
    message_final = ""
    marqueur_fin = '1111111111111110' * 4

    points = generer_points_aleatoires(width, height, width * height, graine)

    for (x, y) in points:
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