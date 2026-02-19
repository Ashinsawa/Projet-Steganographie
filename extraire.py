from PIL import Image

def extraire_message(image_path):
    # On force en RGBA pour être sûr d'avoir 4 valeurs
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size
    
    bits_extraits = ""
    message_final = ""
    marqueur_fin = '1111111111111110'
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # On récupère le bit de poids faible (LSB) du rouge
            bits_extraits += str(r & 1)
            
            # Si on a trouvé le marqueur de fin, on reconstruit le message
            if bits_extraits.endswith(marqueur_fin):
                bits_utiles = bits_extraits[:-len(marqueur_fin)]
                
                for i in range(0, len(bits_utiles), 8):
                    octet = bits_utiles[i:i+8]
                    message_final += chr(int(octet, 2))
                
                return message_final
    
    return "Aucun marqueur de fin trouvé."

# Exemple d'utilisation :
print(extraire_message("images/image1_codee.png"))