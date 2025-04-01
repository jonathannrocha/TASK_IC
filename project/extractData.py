import os
import pdfplumber
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import create_engine

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
    
    def uploadCSVToDatabase(csvPath, table):
        DB_CONFIG = {
            "dbname": "IC",
            "user": "postgres",
            "password": "1234",
            "host": "127.0.0.1",
            "port": "5432"
        }

        engine = create_engine(f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")

        df = pd.read_csv(csvPath, delimiter=';', encoding='utf-8')
        
        df.columns = [col.strip().replace('"', '') for col in df.columns]
        df.columns = [col.lower() for col in df.columns]

        df.to_sql(table, engine, if_exists="append", index=False)

        print("Dados inseridos com sucesso!")

    def convertCSVDemonstracao(CSVpath):
        df = pd.read_csv(CSVpath, delimiter=";", dtype=str)

        df["VL_SALDO_INICIAL"] = df["VL_SALDO_INICIAL"].str.replace(",", ".").astype(float)
        df["VL_SALDO_FINAL"] = df["VL_SALDO_FINAL"].str.replace(",", ".").astype(float)
        df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')

        df.to_csv(CSVpath, index=False, sep=";")

        print("Arquivo corrigido salvo com sucesso!")

        
        