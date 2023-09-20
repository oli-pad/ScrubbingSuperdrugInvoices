from modules.SuperdrugInvoiceDetail import SuperdrugInvoiceDetail
from modules.ProduceFileList import ProduceFileList
from modules.RenameInvoices import RenameInvoices
from modules.Get_Scrubbed_Detail import Get_Scrubbed_Detail
import pandas as pd

#RenameInvoices('W:\Audit\Coty\Invoice Images\EmailStagingBay\Superdrug')

df = SuperdrugInvoiceDetail('W:\Audit\Coty\Invoice Images\ImageStagingBay\Superdrug\\5944702.pdf','CL027','SUP01').Full_Invoice()

print(df[["Line_Description","Invoice_No", "Net_Amount", "VAT_Amount", "Gross_Amount"]])
print(df["Gross_Amount"].sum())

#df = Get_Scrubbed_Detail('W:\Audit\Coty\Invoice Images\ImageStagingBay\Superdrug','CL027','SUP01')

#df.to_csv('W:\Audit\Coty\Invoice Images\Superdrug.csv',index=False)
