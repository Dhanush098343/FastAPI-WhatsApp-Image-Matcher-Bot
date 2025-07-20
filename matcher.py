
from PIL import Image
import imagehash

def images_are_similar(img1: Image.Image, img2: Image.Image, max_distance=5) -> bool:
    try:
        img1 = img1.convert("RGB").resize((300, 300))
        img2 = img2.convert("RGB").resize((300, 300))

        hash1 = imagehash.phash(img1)
        hash2 = imagehash.phash(img2)

        return hash1 - hash2 <= max_distance  # Hamming distance
    except Exception as e:
        print(f"Matching error: {e}")
        return False
