from modules.Get_Scrubbed_Detail import Get_Scrubbed_Detail
from modules.InsertIntoSQL import InsertIntoSQL

#Stores all the invoice data in a local dataframe
df = Get_Scrubbed_Detail('W:\Audit\Coty\Invoice Images\ImageStagingBay\Superdrug','CL027','SUP01')

#Inserts the data into the SQL database
InsertIntoSQL(df,'CL027','SUP01')

#For faster testing CSV to check the data in the dataframe
df.to_csv('W:\Audit\Coty\Invoice Images\Superdrug.csv',index=False)
