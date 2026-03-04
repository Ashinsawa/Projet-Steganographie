from PIL import Image
import random

# ------------------------------------------------------------
# cacher.py
# Objectif :
# - Convertir un message texte en bits ("0" / "1")
# - Disperser ces bits dans l'image (sur le LSB du canal rouge)
# - Utiliser une "graine" (seed) comme mot de passe : même seed => mêmes pixels
#
# Format stocké :
# - message en binaire (8 bits par caractère)
# - + marqueur de fin (64 bits) pour savoir quand s'arrêter au décodage
# ------------------------------------------------------------

def message_to_bin(message):
    """
    Convertit un message en binaire (8 bits par caractère).
    Exemple: "A" -> "01000001"
    """
    return ''.join(format(ord(i), '08b') for i in message)

def iter_points_aleatoires(largeur, hauteur, graine):
    """
    Génère une permutation pseudo-aléatoire des pixels (x, y) basée sur la graine.

    Important :
    - On évite de construire une énorme liste de tous les pixels (peut faire freezer).
    - On utilise un mélange "streaming" (style Fisher-Yates) avec un dict 'swaps'
      pour simuler les échanges sans stocker tout le tableau.

    Même (largeur, hauteur, graine) => même ordre de pixels.
    """
    n = largeur * hauteur
    rng = random.Random(graine)  # Générateur aléatoire local : dépend seulement de la graine
    swaps = {}                   # Stocke les swaps virtuels (économie mémoire)

    for i in range(n):
        # On choisit j entre i et n-1 (comme un Fisher-Yates)
        j = rng.randrange(i, n)

        # Valeurs actuelles (si déjà swappées, on récupère dans swaps)
        val_i = swaps.get(i, i)
        val_j = swaps.get(j, j)

        # On "swap" ces valeurs
        swaps[i] = val_j
        swaps[j] = val_i

        # idx = index linéaire du pixel (0..n-1) après mélange
        idx = swaps[i]

        # Conversion index linéaire -> coordonnées (x, y)
        x = idx % largeur
        y = idx // largeur
        yield (x, y)

def cacher_message(image_path, message, output_path, graine):
    """
    Cache un message dans l'image image_path et sauvegarde le résultat dans output_path.

    - Le message est stocké dans le bit de poids faible (LSB) du canal Rouge (R).
    - On modifie 1 pixel = 1 bit (donc capacité = largeur*hauteur bits).
    - Les pixels utilisés sont dispersés sur toute l'image grâce à la graine.
    """
    # On force RGBA pour éviter les erreurs (certaines images PNG ont un alpha => 4 valeurs)
    img = Image.open(image_path).convert("RGBA")

    # Marqueur de fin long (64 bits) => limite les "faux messages" dans une image non encodée
    marqueur_fin = '1111111111111110' * 4  # 64 bits

    # Le contenu réellement caché = message binaire + marqueur fin
    binary_msg = message_to_bin(message) + marqueur_fin

    pixels = img.load()
    width, height = img.size

    # Capacité : 1 bit par pixel (on ne touche qu'au rouge)
    if len(binary_msg) > width * height:
        raise ValueError("Message trop long pour cette image.")

    # Génère un ordre pseudo-aléatoire des pixels (x, y) à modifier
    points = iter_points_aleatoires(width, height, graine)

    # Pour chaque bit :
    # - on prend le prochain pixel aléatoire
    # - on remplace le dernier bit du rouge par ce bit
    for bit in binary_msg:
        x, y = next(points)
        r, g, b, a = pixels[x, y]

        # (r & ~1) -> met le dernier bit de r à 0
        # | int(bit) -> met ce dernier bit à 0 ou 1 selon le message
        nouveau_r = (r & ~1) | int(bit)

        # On réécrit le pixel : on modifie uniquement R, on garde G,B,A identiques
        pixels[x, y] = (nouveau_r, g, b, a)

    # On sauvegarde UNE SEULE FOIS à la fin (important pour ne pas spam / ralentir)
    img.save(output_path)
    print(f"Message caché dans {output_path}")

# Test console (ne s'exécute que si on lance cacher.py directement)
if __name__ == "__main__":
    cacher_message("images/image1.png", "Mon message secret", "images/image1_codee.png", "mdp123")