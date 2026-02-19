from PIL import Image

def extraire_message(image_path):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size
    
    bits_extraits = ""
    message_final = ""
    marqueur_fin = '1111111111111110'
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # On récupère le bit de poids faible (LSB) avec l'opérateur ET
            bits_extraits += str(r & 1)
            
            # On vérifie si on a trouvé le marqueur de fin
            if bits_extraits.endswith(marqueur_fin):
                # On retire le marqueur pour ne garder que les données
                bits_utiles = bits_extraits[:-len(marqueur_fin)]
                
                # On regroupe par 8 bits pour reformer les caractères
                for i in range(0, len(bits_utiles), 8):
                    octet = bits_utiles[i:i+8]
                    message_final += chr(int(octet, 2))
                
                return message_final
    
    return "Aucun marqueur de fin trouvé."

# Exemple d'utilisation :
print(extraire_message("images/image1_codee_codee.png"))