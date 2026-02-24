from PIL import Image
from pathlib import Path

print("✅ analyse_images.py a bien démarré")

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"

print("📁 Dossier projet :", BASE_DIR)
print("🖼️ Dossier images :", IMAGES_DIR)


def image_diff(image1_path, image2_path, output_path):
    img1 = Image.open(image1_path).convert("RGBA")
    img2 = Image.open(image2_path).convert("RGBA")

    if img1.size != img2.size:
        print("Les images n'ont pas la même taille.")
        return False

    width, height = img1.size
    p1 = img1.load()
    p2 = img2.load()

    diff_img = Image.new("RGBA", (width, height))
    pd = diff_img.load()

    nb_diff = 0  # ✅ compteur

    for y in range(height):
        for x in range(width):
            if p1[x, y] == p2[x, y]:
                pd[x, y] = (255, 255, 255, 255)
            else:
                pd[x, y] = (255, 0, 0, 255)
                nb_diff += 1  # ✅

    diff_img.save(output_path)
    print(f"Image diff créée : {output_path}")
    print(f"✅ Pixels différents : {nb_diff} / {width*height}")  # ✅ preuve
    return True



def visualiser_lsb_rouge(image_path, output_path):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()

    out = Image.new("RGBA", (width, height))
    pout = out.load()

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            v = (r & 1) * 255
            pout[x, y] = (v, v, v, 255)

    out.save(output_path)
    print(f"✅ Image LSB créée : {output_path}")


if __name__ == "__main__":
    print("▶️ Bloc main exécuté")

    img_originale = IMAGES_DIR / "image1.png"
    img_codee = IMAGES_DIR / "image1_codee.png"

    print("🔎 Existe image1.png ?", img_originale.exists())
    print("🔎 Existe image1_codee.png ?", img_codee.exists())

    if not img_originale.exists():
        print("❌ image1.png introuvable dans images/")
        raise SystemExit(1)

    if not img_codee.exists():
        print("⚠️ image1_codee.png introuvable : crée-la d'abord avec cacher.py ou ta GUI")
        raise SystemExit(1)

    image_diff(img_originale, img_codee, IMAGES_DIR / "diff_image1.png")
    visualiser_lsb_rouge(img_codee, IMAGES_DIR / "lsb_rouge_image1_codee.png")
    visualiser_lsb_rouge(img_originale, IMAGES_DIR / "lsb_rouge_image1.png")
