from PIL import Image

def message_to_bin(message):
    # Convertit le message en binaire (8 bits par caractère)
    return ''.join(format(ord(i), '08b') for i in message)

def cacher_message(image_path, message, output_path):
    img = Image.open(image_path)
    binary_msg = message_to_bin(message) + '1111111111111110' # Marqueur de fin
    
    pixels = img.load()
    width, height = img.size
    
    idx = 0
    for y in range(height):
        for x in range(width):
            if idx < len(binary_msg):
                r, g, b = pixels[x, y]
                
                # On modifie le bit de poids faible du canal Rouge
                # (r & ~1) met le dernier bit à 0, puis on ajoute le bit du message
                nouveau_r = (r & ~1) | int(binary_msg[idx])
                
                pixels[x, y] = (nouveau_r, g, b)
                idx += 1
    
    img.save(output_path)
    print(f"Message caché dans {output_path}")

# Exemple d'utilisation
cacher_message("image_originale.png", "Secret MNS 2026", "image_codee.png")