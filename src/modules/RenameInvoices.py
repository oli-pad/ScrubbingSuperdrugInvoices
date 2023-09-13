from modules.SuperdrugInvoiceDetail import SuperdrugInvoiceDetail
from modules.ProduceFileList import ProduceFileList
import os
import shutil

def RenameInvoices(directory):
    FileList = ProduceFileList(directory)
    for file in FileList:
        try:
            Invoice_No = SuperdrugInvoiceDetail(os.path.join(directory,file),'123','456').Invoice_No()
        except:
            Invoice_No = 'Unknown'
        print(file)
        print(Invoice_No)
        if Invoice_No != 'Unknown' and Invoice_No != None:
            shutil.copy(os.path.join(directory,file),os.path.join("W:\Audit\Coty\Invoice Images",Invoice_No+'.pdf'))
            try:
                os.rename(os.path.join(directory,file),os.path.join("W:\Audit\Coty\Invoice Images\ImageStagingBay\Superdrug",Invoice_No+'.pdf'))
            except:
                try:
                    os.replace(os.path.join(directory,file),os.path.join("W:\Audit\Coty\Invoice Images\ImageStagingBay\Superdrug",Invoice_No+'.pdf'))
                except:
                    pass