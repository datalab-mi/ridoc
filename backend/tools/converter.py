"""Fichier permettant de convertir les fichiers du .odt, pdf à .json """

import os
import json, collections
from odf import text, teletype
from odf.opendocument import load
from tika import parser
from os import environ
import re
from pathlib import Path
import unidecode

# remove "-"" at the beginning and the withespaces
reg_list = re.compile('^\-\s*(.*)')

def normalize(string: str):
    """Strip lower and accent removal
    Args:
        string (str): The string to process
    Returns:
        str: the decoded string
    """
    return unidecode.unidecode(string.strip().lower())

def odt2json(path: str, sections: list = []) -> dict:
    """ Read thanks to odf library an odt document
    Args:
        path (str) : path of the file
        sections (list) : The section to read.
    Returns:
        dict: Keys are sections and value the content read
    """
    for i, x in enumerate(sections):
        x['key'] = normalize(x['key'])
        sections[i] = x
    # extract test from doc
    doc = load(path)
    L = [teletype.extractText(x) for x in doc.getElementsByType(text.P)]

    # remove None and empty string (i.e borders)
    L = [x for x in L if x and x != '']

    # replace \xa0 and \n
    L = [x.replace(u'\xa0', u' ').replace(u'\n' , u' ') for x in L]
    L2 = []

    for x in L:
        g = re.match("^({sections})\s*:\s*(.*)".format(sections='|'.join([x['key'] for x in sections] )), normalize(x))

        if g:
            L2 += [g.group(1), x[g.span(2)[0]: g.span(2)[1]]] # span rather group to get origal string
        else:
            # Section is not present
            L2 += [x]

    # Remove empty or digit element
    L2 = [x for x in L2 if x and x != '' and not x.isdigit()]
    #print(L2)
    data = {}
    section_content = []
    current_section = ''
    is_array = False
    for x in L2:
        is_new_section = False
        for entry in sections:
            if normalize(x) in entry['key']:
                is_new_section = True
                is_array = entry.get('array', False)
                current_section = entry.get("=>", normalize(x))
                section_content = []
        #import pdb; pdb.set_trace()
        if not is_new_section:
            x_match = re.match(reg_list, x)
            if x_match:
                x = x_match.group(1)
            if re.search('[a-zA-Z0-9]', x): # If there are letters
                section_content += [x]

        # save the buffer until the next section
        if is_array:
            data[current_section] = []
            for el in section_content:
                data[current_section] += el.split(",")
        else :
            data[current_section] = ' '.join(section_content)

    if '' in data:
        data.pop('')
    return data


def pdf2json(path: str, sections: list = []) -> dict:
    """ Read thanks to tika docker a pdf document
    Args:
        path (str) : path of the file
        sections (list) : The section to read.
    Returns:
        dict: Keys are sections and value the content read
    """
    try:
        file_data = parser.from_file(path,"http://tika:9998/")
        data = file_data['content']
        data = data.replace(u'\xa0', u' ')
        data = data.replace(u'\n' , u' ')
        data = data.replace(u'\xa0', u' ')
        data = data.replace(u'\n' , u' ')
        data = re.sub(' +', ' ', data)
        data = data.strip()

    except Exception as e:
        print(e)
        data = ""
    return {"content" : data}

def save_json(data, json_file: str):
    json_file = Path(json_file)
    if not json_file.parent.exists():
        json_file.parent.mkdir(parents=True, exist_ok=True)
    print("save json to %s"%json_file)
    with open(json_file , 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    return 'OK'

if __name__ == '__main__':
    path = '/app/tests/doc.odt'
    data = convertisseur_odt_txt(path)
    save_json(data, 'docOdt.json')

    path = '/app/tests/doc.pdf'
    txt = convertisseur_pdf_txt(path)
    name = 'doc name'
    Titre = 'doc titre'
    Date = 'doc date'
    Auteurs = 'doc auteur 1'
    data = dict(Titre=Titre, Date=Date,Auteurs=Auteurs)
    data['Corps'] = txt
    save_json(data, 'doc.json')
