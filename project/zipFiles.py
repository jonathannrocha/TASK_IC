import zipfile
import os

class zipFiles():
    
    def converterZip(listPathFiles, nameZip, diretorio):
        listFiles = listPathFiles
        nameFileZip = nameZip

        if not listFiles:
            return print(f'Arquivos não informado!')
        
        if listFiles.__len__() > 0:
            with zipfile.ZipFile(nameFileZip, 'w') as zipf:
                for itemFile in listFiles:
                    item = os.path.join(  diretorio, itemFile)
                    zipf.write( item , arcname=itemFile)
    
    def extractFileZip( path, pathSave):
        try:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(pathSave)
                
        except:
            print(f"Erro ao converter o { path } no path {pathSave}")