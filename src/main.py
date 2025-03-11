from modules.Get_Scrubbed_Detail import Get_Scrubbed_Detail
from modules.InsertIntoSQL import InsertIntoSQL
from modules.RenameInvoices import RenameInvoices

RenameInvoices('W:\Audit\Coty\Invoice Images\EmailStagingBay\Superdrug')

#Stores all the invoice data in a local dataframe
df = Get_Scrubbed_Detail('W:\Audit\Coty\Invoice Images\ImageStagingBay\Superdrug','CL027','SUP01')

#Inserts the data into the SQL database
InsertIntoSQL(df,'CL027','SUP01')
print("Charges in SQL server table.")

#For faster testing CSV to check the data in the dataframe
df.to_csv('W:\Audit\Coty\Invoice Images\Superdrug24022025.csv',index=False)