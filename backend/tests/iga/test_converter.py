import sys, json

sys.path.append('./tools')

from converter import pdf2json, odt2json

def test_pdf2json():
    directory = '/app/tests/iga/data/doc.pdf'
    #directory = '/app/tests/data/ignit_pnigitis.pdf'
    name = 'doc name'
    Titre = 'doc titre'
    Date = 'doc date'
    Auteurs = 'doc auteur 1'
    #convertisseur_Pdf_Json(directory, name, Titre, Date, Auteurs)
    data = pdf2json(directory)
    assert data == {'content': 'Ceci est un texte pdf'}, data

