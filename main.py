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
    workingDataBase()
    

        
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

    TABLES = {
        "OPERADORAS": "OPERADORAS",
        "DEMONSTRACOES": "DEMONSTRACOES"
    }
   
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
    

    pathOperadoras = os.path.join(DIRETORIO, "operadorasAtivas")
    if not os.path.exists(pathOperadoras):
        os.makedirs(pathOperadoras, exist_ok=True)

    dowloadFiles( SITE_URL["operadorasAtivas"] , pathOperadoras)

    mapColumnsOPeradoras = {
        "Registro_ANS": "INTEGER",
        "CNPJ": "VARCHAR(20)",
        "Razao_Social": "VARCHAR(255)",
        "Nome_Fantasia": "VARCHAR(255)",
        "Modalidade": "VARCHAR(100)",
        "Logradouro": "VARCHAR(255)",
        "Numero": "VARCHAR(255)",
        "Complemento": "VARCHAR(255)",
        "Bairro": "VARCHAR(100)",
        "Cidade": "VARCHAR(100)",
        "UF": "VARCHAR(10)",
        "CEP": "VARCHAR(20)",
        "DDD": "VARCHAR(20)",
        "Telefone": "VARCHAR(20)",
        "Fax": "VARCHAR(20)",
        "Endereco_eletronico": "VARCHAR(255)",
        "Representante": "VARCHAR(255)",
        "Cargo_Representante": "VARCHAR(100)",
        "Regiao_de_Comercializacao": "FLOAT",
        "Data_Registro_ANS": "DATE"
    }

    
    # createTable(TABLES["OPERADORAS"], mapColumnsOPeradoras )


    itemOperadoras = os.listdir(os.path.join(DIRETORIO,"operadorasAtivas"))[0]

    extractData.uploadCSVToDatabase(os.path.join( DIRETORIO,"operadorasAtivas" ,itemOperadoras) , TABLES["OPERADORAS"])

    mapColumnsSaldoOperadoras = {
        "DATA": "DATE",
        "REG_ANS": "INTEGER",
        "CD_CONTA_CONTABIL": "INTEGER",
        "DESCRICAO": "VARCHAR(255)",
        "VL_SALDO_INICIAL": "DOUBLE PRECISION",
        "VL_SALDO_FINAL": "DOUBLE PRECISION"
    }

    filesDemonstraceos = os.listdir(os.path.join(DIRETORIO,"demosntracoes"))
    
    # createTable(TABLES["DEMONSTRACOES"], mapColumnsSaldoOperadoras )

    for i in filesDemonstraceos:
        if ".csv" in i:
            pathDemonstracoes =  os.path.join( DIRETORIO,"demosntracoes" ,i)

            extractData.convertCSVDemonstracao( pathDemonstracoes)
            
            extractData.uploadCSVToDatabase(os.path.join( DIRETORIO,"demosntracoes" ,i), TABLES["DEMONSTRACOES"])

main()

