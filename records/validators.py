from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_type(value):
    """
    Valide qu'un fichier est une image JPEG ou PNG.
    Vérifie l'extension et tente d'ouvrir l'image avec Pillow.
    """
    # Vérification de l'extension du fichier
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError("Seules les images .jpg, .jpeg et .png sont autorisées.")

    # Vérification du contenu réel de l'image
    try:
        image = Image.open(value)
        if image.format not in ('JPEG', 'PNG'):
            raise ValidationError("Le fichier n'est pas une image JPEG ou PNG valide.")
    except Exception:
        raise ValidationError("Le fichier n'est pas une image valide.")


def validate_image_size(image, record=None):
    """
    Limite le nombre d'images à 50 par catégorie pour un enregistrement donné.
    """
    if record:
        category = getattr(image.instance, 'category', None)
        if category:
            image_count = record.images.filter(category=category).count()
            if image_count >= 50:
                raise ValidationError("Vous ne pouvez pas ajouter plus de 50 images pour cette catégorie.")
