import os
import pdfplumber
import pandas as pd
import pandas as pd
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.exc import ProgrammingError


class extractData():
    def  extract_pdf(pdfPath, diretorio):
        data = []
        pdfPath = pdfPath
        with pdfplumber.open(pdfPath) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        data.append(row)
        
        df = pd.DataFrame(data)
        df = df.dropna(how='all')  
        df.columns = df.iloc[0] 
        df = df[1:].reset_index(drop=True)  
    

        df = df.rename( columns={"OD" : "Seg. Odontológica"})
        df = df.rename( columns={"AMB" : "Seg. Ambulatorial"})
        
        df.to_csv(os.path.join( diretorio, "teste.csv"), index=False)
    
    def uploadCSVToDatabase(csvPath):
       print("parei aquit")

        
        