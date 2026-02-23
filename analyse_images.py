from PIL import Image

def image_diff(image1_path, image2_path, output_path):
    """
    Crée une image montrant les différence entre 2 images de même taille.
    - pixels identiques => blanc
    - pixels différents => rouge
    Si les tailles sont différentes => ne fait rien (retoure False)
    """
    img1 = Image.open(image1_path).convert("RGBA")
    img2 = Image.open(image2_path).convert("RGBA")

    # Vérifie que les images ont la même taille
    if img1.size != img2.size:
        print("Les images n'ont pas la même taille. Aucune image de différence créée.")
        return False
    
    width, height = img1.size
    p1 = img1.load()
    p2 = img2.load()

    # Nouvelle image de sortie (même taille)
    diff_img = Image.new("RGBA", (width, height))
    pd = diff_img.load()

    # On parcourt tous les pixels
    for y in range(height):
        for x in range(width):
            if p1[x, y] == p2[x, y]:
                # Pixel identique => blanc
                pd[x, y] = (255, 0, 0, 255)
            else:
                # Pixel différent => rouge
                pd[x, y] = (255, 255, 255, 255)

    diff_img.save(output_path)
    print(f"Image de différences créée : {output_path}")
    return True


def visualiser_lsb_rouge(image_path, output_path):
    """
    Crée une image noir/blanc qui montre uniquement le LSB du canal rouge.
    - Si le LSB de R vaut 0 => noir (0)
    - Si le LSB de R vaut 1 => blanc (255)
    """
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()

    out = Image.new("RGBA", (width, height))
    pout = out.load()

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]

            # extrait le bit LSB puis le transforme en 0 ou 255
            visualisation_lsb = (r & 1) * 255

            # on met la même valeur sur R,G,B => image en niveaux de gris
            pout[x, y] = (visualisation_lsb, visualisation_lsb, visualisation_lsb, 255)

        out.save(output_path)
        print(f"Image LSB rouge créée : {output_path}")

    if __name__ == "__main__":
        # ---- Tests simples ----

        # Q4 : différence entre image originale et image encodée
        image_diff(
            "images/image1.png",
            "images/image1_codee.png",
            "images/diff_image1.png"
        )

        # Q5 : visualiser le LSB rouge d'une image encodée
        visualiser_lsb_rouge(
            "image/image1_codee.png",
            "images/lsb_rouge_image1_codee.png"
        )

        # Q5 (optionnel) : visualiser aussi une image non encodée pour comparer
        visualiser_lsb_rouge(
            "images/image1.png",
            "images/lsb_rouge_image1.png"
        )