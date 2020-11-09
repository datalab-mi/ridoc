import argparse
import pandas as pd

#Fonction tools

#Checks path existance
def dir_path(path):
    if path.exists():
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

#From metric (str), returns its settings (dict)
def metric_parameters(metric):
    rank_body_metrics = {}

    if metric == 'precision':
        rank_body_metrics['precision'] = {"k": 1,
                                          "relevant_rating_threshold": 1e3,
                                          "ignore_unlabeled": False}
    elif metric == 'recall':
        rank_body_metrics['recall'] = {"k": 1,
                                        "relevant_rating_threshold": 1e3}

    elif metric == 'mean_reciprocal_rank':
        rank_body_metrics['mean_reciprocal_rank'] = {"k": 1,
                                                      "relevant_rating_threshold": 1e3}
    elif metric == 'dcg':
        rank_body_metrics['dcg'] = {"k": 3,
                                    "normalize": False}
    elif metric == 'expected_reciprocal_rank':
        rank_body_metrics['expected_reciprocal_rank'] = {"maximum_relevance": 1e3,
                                                          "k":1}
    else: print(metric + ' not recognized as a metric')
    return rank_body_metrics

#From PoC test base to cleaned test base
def clean_test_base(test_base_path, new_file_path):

    ''' Takes the Question/Answer odt file given by IGPN : test_base_path
        Returns a cleaned csv file taking into account the differences between the documents in the database: stored in new_file_path'''
    data = pd.read_excel(test_base_path, engine="odf")

    #Modification of the file names
    data.loc[data['Fiches'] == '2019 Droit de grève et astreinte des ASPTS' , 'Fiches']  = '2019  astreinte et droit de grève des ASPTS 07'
    data.loc[data['Fiches'] == '2019 Préavis et droit de grève  ' , 'Fiches']  = '2019  droit de grève 03'
    data.loc[data['Fiches'] == '2019 Attroupement délictuel MO' , 'Fiches']  = '2019 attroupement délictuel MO'
    data.loc[data['Fiches'] == '2019 Médicaments durant la rétention ou la GAV' , 'Fiches']  = "2019 administration de médicaments lors d'une rétention ou d'une GAV"
    data.loc[data['Fiches'] == '2019 AFI – MFI' , 'Fiches']  = "2019 distinction AFI et MFI"
    data.loc[data['Fiches'] == '2019 Conditions du port de l’arme hors service' , 'Fiches']  = "2019-condition du port de l'arme hors service"
    data.loc[data['Fiches'] == "2019 Port de l'arme hors service durant la scolarité en école de police " , 'Fiches']  = "2019 port de l'arme hors service durant la scolarité"
    data.loc[data['Fiches'] == "2019 Attribution et détention de l'arme de service par les fonctionnaires de police" , 'Fiches']  = "2019  Attribution et détention de l'arme de service par les fonctionnaires de police 02"

    #Mispelling
    data.loc[data['Questions'] == "De quelle autonomie dispose un ajoint de sécurité ?" , "Questions"] = "De quelle autonomie dispose un adjoint de sécurité ?"
    data.loc[data['Questions'] == "l’Usage des armes estil possible contre un toupement ?" , "Questions"] = "l’Usage des armes estil possible contre un attroupement ?"


    #Remove unrelevant answers
    data = data.drop(np.where(data['Questions'] == "Le chargeur doit-il être dégarni ?")[0] , axis = 0)
    data = data.drop(np.where(data['Questions'] == "Est ce que j’ai le droit de tirer dans la rue ?")[0] , axis = 0)

    #Remove ungiven documents
    data = data.drop(np.where(data['Fiches'] == '2019 Compte rendu après identification – LRPPN – TAJ')[0] , axis = 0)
    data = data.drop(np.where(data['Fiches'] == '2019 Utilisation des informations issues du TAJ dans une EAPD')[0] , axis = 0)
    data = data.drop(np.where(data['Fiches'] == "2019 Blâme et Avancement d'un fonctionnaire")[0] , axis = 0)
    data = data.drop(np.where(data['Fiches'] == '2019 Anonymat des fonctionnaires CRS dans les procédures judiciaires')[0] , axis = 0)
    data = data.drop(np.where(data['Fiches'] == '2019 Cumul d’une activité d’import / export')[0] , axis = 0)

    #Questions adding
    data = data.append(pd.DataFrame([["Peut-on mettre un IPM en geole de GAV ?" , "06 Surveillance des personnes retenues au poste de police pour ivresse publique et manifeste"] ,
                ["quelle sosnt les limites du 11-2 CPP ?" , "03 Article 11-2"],
                ["Ou doit-on ranger son arme ?" , "2019 Conservation arme ind – lieux de dépôt – meuble sécurisé"],
                ["qu’est ce qu’un endroit sécurisé ?" , "2019 dépôts des armes- casiers"],
                ["quelle est la différence entre le dépôt et le stockag ?" , "03 conditions de conservation d'armes collectives"] ,
                ["Est ce que j’ai le droit de ramener mon arme à la maisn ?" , "2019   conservation de l'ame à domicile"],
                ["qu’est ce qu’une activité libre ?" , "2019  cumul d'activité"]] , columns = ['Questions' , "Fiches"]) , sort = True)

    #Nettoyage
    data['Fiches'] = data['Fiches'].map(lambda x:x.lower())
    data["Questions"] = data["Questions"].map(lambda x: unicodedata.normalize("NFKD", x))
    data = data.reset_index()
    data = data.drop("index" , axis = 1)
    data = data.drop("Unnamed: 0" , axis = 1)


    data.to_csv(new_file_path,index=False, encoding="utf-8")

    return data
