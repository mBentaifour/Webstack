from PIL import Image
from io import BytesIO
from django.core.files import File
import os

def resize_image(image, size=(800, 800), quality=85, format='JPEG'):
    """
    Redimensionne et optimise une image
    :param image: Le fichier image d'origine
    :param size: Tuple (width, height) pour la taille maximale
    :param quality: Qualité de compression (1-100)
    :param format: Format de sortie ('JPEG', 'PNG', etc.)
    :return: Fichier image redimensionné et optimisé
    """
    if not image:
        return None

    # Ouvrir l'image avec Pillow
    img = Image.open(image)

    # Convertir en RGB si nécessaire (pour les images PNG avec transparence)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Calculer les nouvelles dimensions en conservant le ratio
    ratio = min(size[0] / img.width, size[1] / img.height)
    new_size = (int(img.width * ratio), int(img.height * ratio))

    # Redimensionner l'image
    if img.size != new_size:
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    # Préparer le buffer pour sauvegarder l'image
    buffer = BytesIO()
    
    # Sauvegarder l'image optimisée dans le buffer
    img.save(buffer, format=format, quality=quality, optimize=True)
    
    # Préparer le nom du fichier
    file_name = os.path.splitext(os.path.basename(image.name))[0]
    file_extension = format.lower()
    
    # Créer un nouveau fichier Django à partir du buffer
    file_object = File(buffer)
    file_object.name = f"{file_name}.{file_extension}"
    
    return file_object

def create_thumbnail(image, size=(300, 300)):
    """
    Crée une miniature de l'image
    :param image: Le fichier image d'origine
    :param size: Tuple (width, height) pour la taille de la miniature
    :return: Fichier image miniature
    """
    return resize_image(image, size=size, quality=60)
