from PIL import Image
import random

def message_to_bin(message):
    # Convertit le message en binaire (8 bits par caractère)
    return ''.join(format(ord(i), '08b') for i in message)

def generer_points_aleatoires(largeur, hauteur, nb_bits, graine):
    random.seed(graine)
    indices_possibles = list(range(largeur * hauteur))
    indices_choisis = random.sample(indices_possibles, nb_bits)

    points = []
    for i in indices_choisis:
        x = i % largeur
        y = i // largeur
        points.append((x, y))
    return points

def cacher_message(image_path, message, output_path, graine):
    # On force l'image en RGBA pour être sûr d'avoir 4 valeurs (r,g,b,a)
    img = Image.open(image_path).convert("RGBA")

    marqueur_fin = '1111111111111110' * 4 # 16*4 = 64 bits
    binary_msg = message_to_bin(message) + marqueur_fin
    
    pixels = img.load()
    width, height = img.size
    
    # Vérifie que l'image a assez de pixels pour stocker tous les bits
    if len(binary_msg) > width * height:
        raise ValueError("Message trop long pour cette image.")

    # Génère les positions où écrire les bits (réparties dans toute l'image)
    points = generer_points_aleatoires(width, height, len(binary_msg), graine)

    for idx, (x, y) in enumerate(points):
        r, g, b, a = pixels[x, y]
        nouveau_r = (r & ~1) | int(binary_msg[idx])
        pixels[x, y] = (nouveau_r, g, b, a)

    # ✅ IMPORTANT: on sauvegarde UNE SEULE FOIS, après la boucle    
    img.save(output_path)
    print(f"Message caché dans {output_path}")

if __name__ == "__main__":
    # Exemple d'utilisation (ne tourne que si on lance cacher.py directement)
    cacher_message("images/image1.png", "Mon message secret", "images/image1_codee.png", "mdp123")