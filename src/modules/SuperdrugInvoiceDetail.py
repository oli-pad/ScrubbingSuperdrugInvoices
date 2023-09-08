import pytesseract
from PIL import Image
import os
import re
import pdfplumber
from collections import namedtuple
import sys
import pandas as pd
from modules.ConvertPDFtoText import ConvertPDFtoText

Months={'JAN':'01','FEB':'02','MAR':'03','APR':'04','MAY':'05','JUN':'06','JUL':'07','AUG':'08','SEP':'09','OCT':'10','NOV':'11','DEC':'12'}

Line = namedtuple('Line','Salitix_Client_Number Salitix_Customer_Number SAL_Invoice_type Unit_Funding_Type Line_Description Deal_Type Invoice_No Invoice_Date Promotion_No Product_No Start_Date End_Date Quantity Unit_Price Net_Amount VAT_Amount Gross_Amount Store_Format Invoice_Description Acquisition_Ind')

class SuperdrugInvoiceDetail:

    def __init__(self,filename,Salitix_Client_Number,Salitix_Customer_Number):
        self.filename=filename
        self.pdf_text=ConvertPDFtoText(filename)
        self.lines=self.pdf_text.split('\n')
        self.Salitix_Client_Number=Salitix_Client_Number
        self.Salitix_Customer_Number=Salitix_Customer_Number
        self.Superdrug_Invoice_Detail=self.Full_Invoice()

    def SAL_Invoice_type(self):
        PR=['Cash Margin Support']
        if self.Deal_Type() in PR:
            return 'PR'
    
    def Unit_Funding_Type(self):
        if self.SAL_Invoice_type() == 'PR':
            return 'E'
        else:
            return ''
    
    def Line_Description(self):
        Line_Description=[]
        if self.SAL_Invoice_type() == 'PR':
            for line in self.lines:
                if re.search('(\d{6})(\s)(.*)(\s)(\d{2})[/](\d{2})[/](\d{4})',line):
                    Line_Description.append(re.search('(\d{6})(\s)(.*)(\s)(\d{2})[/](\d{2})[/](\d{4})',line).group(3))
            return Line_Description
        
    def Deal_Type(self):
        for line in self.lines:
            if re.search('REASON(\s?):(\s?)(.*)',line):
                return re.search('REASON(\s?):(\s?)(.*)',line).group(3)

    def Invoice_No(self):
        for line in self.lines:
            if re.search('INVOICE(\s?):(\s?)(\d+)',line):
                return re.search('INVOICE(\s?):(\s?)(\d+)',line).group(3)

    def Invoice_Date(self):
        for line in self.lines:
            if re.search('INVOICE DATE(\s?):(\s?)(\d{2})[-](.*)[-](\d{2})',line):
                return re.search('INVOICE DATE(\s?):(\s?)(\d{2})[-](.*)[-](\d{2})',line).group(3)+'/'+Months[re.search('INVOICE DATE(\s?):(\s?)(\d{2})[-](.*)[-](\d{2})',line).group(4)]+'/20'+re.search('INVOICE DATE(\s?):(\s?)(\d{2})[-](.*)[-](\d{2})',line).group(5)
            
    def Promotion_No(self):
        for line in self.lines:
            if re.search('/Event ID (\d+) /',line):
                return re.search('/Event ID (\d+) /',line).group(1)
    
    def Product_No(self):
        Product_No=[]
        if self.SAL_Invoice_type() == 'PR':
            for line in self.lines:
                if re.search('(\d{6})(\s)(.*)(\s)(\d{2})[/](\d{2})[/](\d{4})',line):
                    Product_No.append(re.search('(\d{6})(\s)(.*)(\s)(\d{2})[/](\d{2})[/](\d{4})',line).group(1))
            return Product_No

    def Start_Date(self):
        for line in self.lines:
            if re.search('For Invoice Create Date(\s?)(\d{2})/(\d{2})/(\d{4})(\s?)To(\s?)(\d{2})/(\d{2})/(\d{4})',line):
                return re.search('For Invoice Create Date(\s?)(\d{2})/(\d{2})/(\d{4})(\s?)To(\s?)(\d{2})/(\d{2})/(\d{4})',line).group(2)+'/'+re.search('For Invoice Create Date(\s?)(\d{2})/(\d{2})/(\d{4})(\s?)To(\s?)(\d{2})/(\d{2})/(\d{4})',line).group(3)+'/'+re.search('For Invoice Create Date(\s?)(\d{2})/(\d{2})/(\d{4})(\s?)To(\s?)(\d{2})/(\d{2})/(\d{4})',line).group(4)

    def End_Date(self):
        for line in self.lines:
            if re.search('For Invoice Create Date(\s?)(\d{2})/(\d{2})/(\d{4})(\s?)To(\s?)(\d{2})/(\d{2})/(\d{4})',line):
                return re.search('For Invoice Create Date(\s?)(\d{2})/(\d{2})/(\d{4})(\s?)To(\s?)(\d{2})/(\d{2})/(\d{4})',line).group(7)+'/'+re.search('For Invoice Create Date(\s?)(\d{2})/(\d{2})/(\d{4})(\s?)To(\s?)(\d{2})/(\d{2})/(\d{4})',line).group(8)+'/'+re.search('For Invoice Create Date(\s?)(\d{2})/(\d{2})/(\d{4})(\s?)To(\s?)(\d{2})/(\d{2})/(\d{4})',line).group(9)

    def Quantity(self):
        Quantity=[]
        subtotal=0
        Quantity_status=False
        if self.SAL_Invoice_type() == 'PR':
            for line in self.lines:
                if re.search('^(\d{6})(\s)(.*)(\s)(\d{2})[/](\d{2})[/](\d{4})(\s)(\d+)(\s)([0-9.,]*)(\s)([0-9.,]*)(\s)(.*)(\s)([0-9.,]*)$',line):
                    Quantity_status=True
                    subtotal += float(re.search('^(\d{6})(\s)(.*)(\s)(\d{2})[/](\d{2})[/](\d{4})(\s)(\d+)(\s)([0-9.,]*)(\s)([0-9.,]*)(\s)(.*)(\s)([0-9.,]*)$',line).group(9))
                elif Quantity_status and re.search('^(\d{2})[/](\d{2})[/](\d{4})(\s)(\d+)(\s)([0-9.,]*)(\s)([0-9.,]*)(\s)(.*)(\s)([0-9.,]*)$',line):
                    subtotal += float(re.search('^(\d{2})[/](\d{2})[/](\d{4})(\s)(\d+)(\s)([0-9.,]*)(\s)([0-9.,]*)(\s)(.*)(\s)([0-9.,]*)$',line).group(5))
                elif Quantity_status and re.search('^Item total ',line):
                    Quantity.append(subtotal)
                    subtotal=0
                    Quantity_status=False             
            return Quantity
    
    def Unit_Price(self):
        Unit_Price=[]
        for line in self.lines:
            if re.search('^(\d{6})(\s)(.*)(\s)(\d{2})[/](\d{2})[/](\d{4})(\s)(\d+)(\s)([0-9.,]*)(\s)([0-9.,]*)(\s)(.*)(\s)([0-9.,]*)$',line):
                Unit_Price.append(re.search('^(\d{6})(\s)(.*)(\s)(\d{2})[/](\d{2})[/](\d{4})(\s)(\d+)(\s)([0-9.,]*)(\s)([0-9.,]*)(\s)(.*)(\s)([0-9.,]*)$',line).group(13))
        return Unit_Price
    
    def Net_Amount(self):
        Net_Amount=[float(i)*float(j) for i,j in zip(self.Quantity(),self.Unit_Price())]
        return Net_Amount
    
    def VAT_Amount(self):
        VAT_Status = False
        for line in self.lines:
            if re.search('VAT CODE COST EXCL VAT VAT RATE COST INCL VAT',line):
                VAT_Status = True
            elif VAT_Status and re.search('(.*) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',line):
                VAT_Rate = float(re.search('(.*) ([0-9,.]*) ([0-9,.]*) ([0-9,.]*)',line).group(3))/100
                VAT_Amount = [float(i)*VAT_Rate for i in self.Net_Amount()]
                return VAT_Amount
    
    def Gross_Amount(self):
        Gross_Amount=[float(i)+float(j) for i,j in zip(self.Net_Amount(),self.VAT_Amount())]
        return Gross_Amount
        
    def Store_Format(self):
        Store_Format=[]
        for line in self.lines:
            if re.search('^(\d{6})(\s)(.*)(\s)(\d{2})[/](\d{2})[/](\d{4})(\s)(\d+)(\s)([0-9.,]*)(\s)([0-9.,]*)(\s)(.*)(\s)([0-9.,]*)$',line):
                Store_Format.append(re.search('^(\d{6})(\s)(.*)(\s)(\d{2})[/](\d{2})[/](\d{4})(\s)(\d+)(\s)([0-9.,]*)(\s)([0-9.,]*)(\s)(.*)(\s)([0-9.,]*)$',line).group(15))
        return Store_Format
    
    def Invoice_Description(self):
        for line in self.lines:
            if re.search('COMMENTS (.*)$',line):
                return re.search('COMMENTS : (.*)$',line).group(1)
            
    def Acquisition_Ind(self):
        return 'A'
    
    def Full_Invoice(self):
        df=pd.DataFrame()
        Invoice_Details = [Line(self.Salitix_Client_Number,self.Salitix_Customer_Number,self.SAL_Invoice_type(),self.Unit_Funding_Type(),self.Line_Description()[i],self.Deal_Type(),self.Invoice_No(),self.Invoice_Date(),self.Promotion_No(),self.Product_No()[i],self.Start_Date(),self.End_Date(),self.Quantity()[i],self.Unit_Price()[i],self.Net_Amount()[i],self.VAT_Amount()[i],self.Gross_Amount()[i],self.Store_Format()[i],self.Invoice_Description(),self.Acquisition_Ind()) for i in range(len(self.Line_Description()))]
        for i in range(len(Invoice_Details)):
            df2=pd.DataFrame([Invoice_Details[i]],columns=Line._fields)
            df=pd.concat([df,df2])
        return df
