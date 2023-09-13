from modules.SuperdrugInvoiceDetail import SuperdrugInvoiceDetail
from modules.ProduceFileList import ProduceFileList
from modules.RenameInvoices import RenameInvoices
import pandas as pd

print(SuperdrugInvoiceDetail('W:\Audit\Coty\Invoice Images\EmailStagingBay\Superdrug\\834932.pdf','123','456').Net_Amount())

#RenameInvoices('W:\Audit\Coty\Invoice Images\EmailStagingBay\Superdrug')