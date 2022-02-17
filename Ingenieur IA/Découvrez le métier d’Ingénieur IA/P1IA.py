#Importation des packages requis
import pandas
import argparse
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

#Creation des argumenbts
parser = argparse.ArgumentParser()
parser.add_argument("-t", dest="text", type = str, help = "The text to send at Azure.")
parser.add_argument("-id",dest="ID", type = str, help = "The file conteaining your Azure ID")
args = parser.parse_args()
text = args.text
ID_file = args.ID

def get_id(file):
    """
    Cette fonction recupere à partir d'un fichier texte la cle et le point de terminaison Microsft Azure
    :param file: Le chemin du fichier contenant le point de terminaison en colonne 0,
    et  la clé Azure en colonne 1
    :return: Une liste contennant le endpooint en 1, et la clé en 2
    """
    ID = pandas.read_csv(file,delimiter=";", header=0)
    endpoint = (ID.iat[0, 0])
    key = (ID.iat[0, 1])
    ID_list = [endpoint, key]
    return ID_list
    
ID_list = get_id(ID_file)

credential = AzureKeyCredential(ID_list[1])
endpoint =  ID_list[0]

text_analytics_client = TextAnalyticsClient(endpoint, credential)

documents = [text]

#requete
response = text_analytics_client.detect_language(documents)
result = [doc for doc in response if not doc.is_error]

#Parcours de la reponse et affichage
for idx, doc in enumerate(result):
    print("your text is in {lan} with a confidence score of {p}".format(lan = doc.primary_language.name, p = doc.primary_language.confidence_score))
