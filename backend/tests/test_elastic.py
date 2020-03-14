import sys

sys.path.append('./tools')

from convertisseur import convertisseur_Pdf_Json

def test_pdf2json():
    directory = '/app/tests/doc.pdf'
    name = 'doc name'
    Titre = 'doc titre'
    Date = 'doc date'
    Auteurs = 'doc auteur 1'
    #convertisseur_Pdf_Json(directory, name, Titre, Date, Auteurs)
    pass

