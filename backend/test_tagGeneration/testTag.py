import json, os
from dotenv import load_dotenv
from tools.elastic import get_index_name, get_tag, replace_blue_green, create_index, put_alias, inject_documents, search, index_file, suggest, build_query
import elasticsearch
from elasticsearch import Elasticsearch
from benchmark.utils import *
import pdb;
from multi_rake import Rake
import yake
from keybert import KeyBERT
from summa import keywords
import spacy

pdb.set_trace()

filename="BFC2015-12-15026-fret-saint-pierre-et-miquelon.pdf"
index_name = os.getenv('INDEX_NAME')
ES_PORT=os.getenv('ES_PORT')
ES_HOST=os.getenv('ES_HOST')

#Instanciation of elasticsearch
es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])

content = es.get(index=index_name, id=filename)
textbrut=content['_source']['content']
stopwords=["a","à","â","abord","afin","ah","ai","aie","ainsi","allaient","allo","allô","allons","après","assez","attendu","au","aucun","aucune","aujourd","aujourd'hui","auquel","aura","auront","aussi","autre","autres","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avoir","ayant","b","bah","beaucoup","bien","bigre","boum","bravo","brrr","c","ça","car","ce","ceci","cela","celle","celle-ci","celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","cent","cependant","certain","certaine","certaines","certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là","chacun","chaque","cher","chère","chères","chers","chez","chiche","chut","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien","comme","comment","compris","concernant","contre","couic","crac","d","da","dans","de","debout","dedans","dehors","delà","depuis","derrière","des","dès","désormais","desquelles","desquels","dessous","dessus","deux","deuxième","deuxièmement","devant","devers","devra","différent","différente","différentes","différents","dire","divers","diverse","diverses","dix","dix-huit","dixième","dix-neuf","dix-sept","doit","doivent","donc","dont","douze","douzième","dring","du","duquel","durant","e","effet","eh","elle","elle-même","elles","elles-mêmes","en","encore","entre","envers","environ","es","ès","est","et","etant","étaient","étais","était","étant","etc","été","etre","être","eu","euh","eux","eux-mêmes","excepté","f","façon","fais","faisaient","faisant","fait","feront","fi","flac","floc","font","g","gens","h","ha","hé","hein","hélas","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","i","il","ils","importe","j","je","jusqu","jusque","k","l","la","là","laquelle","las","le","lequel","les","lès","lesquelles","lesquels","leur","leurs","longtemps","lorsque","lui","lui-même","m","ma","maint","mais","malgré","me","même","mêmes","merci","mes","mien","mienne","miennes","miens","mille","mince","moi","moi-même","moins","mon","moyennant","n","na","ne","néanmoins","neuf","neuvième","ni","nombreuses","nombreux","non","nos","notre","nôtre","nôtres","nous","nous-mêmes","nul","o","o|","ô","oh","ohé","olé","ollé","on","ont","onze","onzième","ore","ou","où","ouf","ouias","oust","ouste","outre","p","paf","pan","par","parmi","partant","particulier","particulière","particulièrement","pas","passé","pendant","personne","peu","peut","peuvent","peux","pff","pfft","pfut","pif","plein","plouf","plus","plusieurs","plutôt","pouah","pour","pourquoi","premier","première","premièrement","près","proche","psitt","puisque","q","qu","quand","quant","quanta","quant-à-soi","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelque","quelques","quelqu'un","quels","qui","quiconque","quinze","quoi","quoique","r","revoici","revoilà","rien","s","sa","sacrebleu","sans","sapristi","sauf","se","seize","selon","sept","septième","sera","seront","ses","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soit","soixante","son","sont","sous","stop","suis","suivant","sur","surtout","t","ta","tac","tant","te","té","tel","telle","tellement","telles","tels","tenant","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutes","treize","trente","très","trois","troisième","troisièmement","trop","tsoin","tsouin","tu","u","un","une","unes","uns","v","va","vais","vas","vé","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voilà","vont","vos","votre","vôtre","vôtres","vous","vous-mêmes","vu","w","x","y","z","zut","alors","aucuns","bon","devrait","dos","droite","début","essai","faites","fois","force","haut","ici","juste","maintenant","mine","mot","nommés","nouveaux","parce","parole","personnes","pièce","plupart","seulement","soyez","sujet","tandis","valeur","voie","voient","état","étions"]
textfilt=textbrut.split(' ')
textfilt2=''
for el in textfilt:
    if el not in stopwords:
        textfilt2+= ' '
        textfilt2+=el

#RAKE
rake=Rake(
    language_code='fr',
    min_freq=3
)
keywRake=rake.apply(textfilt2,text_for_stopwords=None)


#yake
yakefrench=yake.KeywordExtractor(lan="fr")
keywYake=yakefrench.extract_keywords(textbrut)

#KeyBert
kw_model=KeyBERT(model='paraphrase-multilingual-MiniLM-L12-v2')   
keywBert=kw_model.extract_keywords(textbrut, stop_words=stopwords, use_mmr=True,diversity=0.5, keyphrase_ngram_range=(1,3))


#TextRank
keywTextRank=keywords.keywords(textfilt2,language="french",split=True,words=5)
keywTR=[]
for element in keywTextRank:
    if element not in stopwords:
        keywTR.append(element)


#spacy
nlp =spacy.load("fr_core_news_sm")
doc=nlp(textbrut)
keywSpacy=doc.ents
breakpoint()