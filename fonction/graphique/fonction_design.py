def rectangle_arrondi(canvas, x1, y1, x2, y2, radius, **kwargs):
    # Dessiner un rectangle avec des coins arrondis en utilisant des arcs de cercle
    return canvas.create_polygon(
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        fill=kwargs.get('fill', 'white'),
        outline=kwargs.get('outline', 'black'),
        width=kwargs.get('width', 1),
        smooth=True
    )

# Fonction pour ajuster la hauteur de la bulle en fonction du texte
def get_text_height(canvas, text, font, width):
    # Créer un texte temporaire pour mesurer la hauteur
    text_id = canvas.create_text(0, 0, text=text, font=font, width=width)
    bbox = canvas.bbox(text_id)  # Récupérer la bounding box du texte
    height = bbox[3] - bbox[1]  # Calculer la hauteur
    canvas.delete(text_id)  # Supprimer le texte temporaire
    return height