from modules.ProduceFileList import ProduceFileList
from modules.SuperdrugInvoiceDetail import SuperdrugInvoiceDetail
import pandas as pd
import os

def Get_Scrubbed_Detail(folder_path,Salitix_Client_Number,Salitix_Customer_Number):
    files = ProduceFileList(folder_path)
    df = pd.DataFrame()
    for file in files:
        try:
            print(os.path.join(folder_path,file))
            df2 = SuperdrugInvoiceDetail(os.path.join(folder_path,file),Salitix_Client_Number,Salitix_Customer_Number).Full_Invoice()
            df=pd.concat([df,df2])
        except:
            None
    return df