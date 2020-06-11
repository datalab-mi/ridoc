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


def test_odt2json():
    directory = '/app/tests/iga/data/doc.odt'
    name = 'doc name'
    Titre = 'doc titre'
    Date = 'doc date'
    Auteurs = 'doc auteur 1'
    #convertisseur_Pdf_Json(directory, name, Titre, Date, Auteurs)
    data = odt2json(directory)
    assert data == {'content': 'Ceci est le contenu d’un .odt'}, data


if __name__ == '__main__':
    test_odt2json()
