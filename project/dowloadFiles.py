import requests
import os

def dowloadFiles(link, DIRETORIO):
    response = requests.get(link)
   
    pdfFilename = os.path.join(  DIRETORIO, link.split("/")[-1])

    try:
        with open(pdfFilename, "wb") as pdfFileItem:
            pdfFileItem.write(response.content)
    except():
        print(f'Não foi possível baixar arquivo ${pdfFileItem}')