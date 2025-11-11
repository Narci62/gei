from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from django.core.files.storage import default_storage

def generer_pdf_epreuve(classe, trimestre, exercices):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, f"Epreuve - Classe : {classe.nom} | Trimestre {trimestre}")

    y = 760
    for i, ex in enumerate(exercices, start=1):
        p.setFont("Helvetica-Bold", 12)
        p.drawString(80, y, f"Exercice {i} ({ex.get_type_display()}): {ex.titre}")
        y -= 20
        p.setFont("Helvetica", 10)
        for line in ex.contenu.splitlines():
            p.drawString(100, y, line)
            y -= 15
            if y < 100:
                p.showPage()
                y = 800

    p.save()
    buffer.seek(0)

    # Enregistrement dans le dossier media
    file_name = f"epreuves_pdf/epreuve_{classe.id}_{trimestre}.pdf"
    file_content = ContentFile(buffer.read())
    file_path = default_storage.save(file_name, file_content)
    return file_path
