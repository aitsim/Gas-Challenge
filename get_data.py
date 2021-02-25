import requests
import cgi
import shutil
import os
import urllib
import pandas as pd
import xlrd
import csv

monthly_url = 'https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDm.xls'
daily_url = 'https://www.eia.gov/dnav/ng/hist_xls/RNGWHHDd.xls'
dir_path = os.path.dirname(os.path.realpath(__file__))

def get_xls_file(url):
    file_name, headers = urllib.request.urlretrieve(url)
    return file_name



def csv_from_excel(file):
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_name('Data 1')
    fieldnames = ['date', 'price']
    nrows = sh.nrows

    with open('daily_prices.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(3,10):
            date = sh.cell_value(i, 0)
            price = sh.cell_value(i, 1)
            dt = xlrd.xldate_as_datetime(date, 0)
            date_object = dt.date()
            writer.writerow({'date':date_object, 'price': price})
            print(date_object,price)



csv_from_excel(get_xls_file(monthly_url))