import requests
from bs4 import BeautifulSoup
import os

from project.dowloadFiles import dowloadFiles
from project.extractData import extractData
from project.zipFiles import zipFiles


DIRETORIO = "arquivos"

SITE_URL = { 
    "anexo": "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos",
    "demonstracoesContabeis": "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/",
    "operadorasAtivas": "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
}

def main():
    workingAttachments()
    

        
def workingAttachments():
    reponse = requests.get( SITE_URL["anexo"] )

    parseContent = BeautifulSoup(reponse.text, "html.parser").find_all("a", href=True )

    link_anexos = [item["href"] for item in parseContent  if "anexo" in item.text.lower() and item["href"].lower().endswith(".pdf")]

    if link_anexos.__len__() > 0:
        if not os.path.exists(DIRETORIO):
            os.makedirs(DIRETORIO, exist_ok=True)

        for link in link_anexos:
            dowloadFiles(link, DIRETORIO)

        filesPath = os.listdir(DIRETORIO)

        zipFiles.converterZip(filesPath,  os.path.join( DIRETORIO,  "arquivos_rol.zip"), DIRETORIO )
        
        pathAnexo =  [a for a in os.listdir(DIRETORIO) if "Anexo_I_Rol_" in a] 
        
        extractData.extract_pdf( os.path.join( DIRETORIO, pathAnexo[0]),DIRETORIO)

        pathCSV =  [a for a in os.listdir(DIRETORIO) if ".csv" in a] 

        zipFiles.converterZip(  pathCSV,   os.path.join( DIRETORIO,  "Teste_Jonathan.zip"), DIRETORIO)

    else:
        print(f'Não foi encontrado nenhum arquivo')


def workingDataBase(): 
    reponse = requests.get( SITE_URL["demonstracoesContabeis"] )

    parseContent = BeautifulSoup(reponse.text, "html.parser").find_all("a", href=True )

    years = []
    for i in parseContent:
        item = i["href"].replace("/", "")
        if item.isdigit():
            years.append( int( item ))
    
    years = years[-2:]
    pathDemosntraceos = os.path.join(DIRETORIO, "demosntracoes")
    if not os.path.exists(pathDemosntraceos ):
        os.makedirs(pathDemosntraceos, exist_ok=True)

    for y in years: 
        reponseYears = requests.get( SITE_URL["demonstracoesContabeis"] + str(y) )
        parseContentYears = BeautifulSoup(reponseYears.text, "html.parser").find_all("a", href=True )
        for contentYearsParse in parseContentYears:
            x = contentYearsParse["href"]
            if ".zip" in x.lower():
                dowloadFiles(  SITE_URL["demonstracoesContabeis"] + str(y) + "/" + x , pathDemosntraceos )

    for filesDemonstracoes in os.listdir(pathDemosntraceos):
        zipFiles.extractFileZip( os.path.join( pathDemosntraceos, filesDemonstracoes) , os.path.join( pathDemosntraceos ))


    for csvItens in os.listdir(pathDemosntraceos):
        if ".csv" in csvItens:
            print(csvItens)

main()
# workingDataBase()
