import pyodbc

def insert_into_staging(df,client_code,retailer_code):
    conn = pyodbc.connect('DRIVER=SQL Server;SERVER=UKSALAZSQL;DATABASE=Salitix_Scrubbed_Data_Staging;Trusted_Connection=Yes;UID=SALITIX\SQLSalitixAuditorUsers')
    cursor = conn.cursor()
    cols = ",".join([str(i).replace(" ","_") for i in df.columns.tolist()])
    for x,row in df.iterrows():
        row_info_0=[str(j).replace("'","") for j in row]
        row_info_0[0]=client_code
        row_info_0[1]=retailer_code
        row_info_0[8]=row_info_0[8][6:]+"-"+row_info_0[8][3:5]+"-"+row_info_0[8][:2]
        row_info_0[11]=row_info_0[11][6:]+"-"+row_info_0[11][3:5]+"-"+row_info_0[11][:2]
        row_info_0[12]=row_info_0[12][6:]+"-"+row_info_0[12][3:5]+"-"+row_info_0[12][:2]
        try:
            row_info_0[13]=str(round(row_info_0[13],2))
        except:None
        try:
            row_info_0[14]=str(round(row_info_0[14],2))
        except:None
        try:
             row_info_0[15]=str(round(row_info_0[15],2))
        except:None
        try:
             row_info_0[16]=str(round(row_info_0[16],2))
        except:None
        try:
             row_info_0[17]=str(round(row_info_0[17],2))
        except:None
        try:
            if float(row_info_0[16])>1:row_info_0[16]=str(float(row_info_0[16])/100)
        except:None
        for x in range(len(row_info_0)):
            if row_info_0[x]=="nan":row_info_0[x]="NULL"
            elif row_info_0[x]=="None":row_info_0[x]="NULL"
            else:row_info_0[x]="'"+row_info_0[x]+"'"
        row_info=",".join([str(j) for j in row_info_0])
        sql1 = "INSERT INTO [Salitix_Scrubbed_Data_Staging].[dbo].[Scrubbed_ASDA_Customer_Charges_Stg] (" +cols + ") VALUES ("+row_info+");"
        cursor.execute(sql1)
        cursor.commit()