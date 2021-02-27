import os
import urllib.request
import xlrd
import csv

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
        for i in range(3,nrows):
            date = sh.cell_value(i, 0)
            price = sh.cell_value(i, 1)
            dt = xlrd.xldate_as_datetime(date, 0)
            date_object = dt.date()
            writer.writerow({'date':date_object, 'price': price})


def monthly_prices ():
    fieldnames = ['month', 'price']
    with open('daily_prices.csv', 'r', newline='') as csvfile:
        reader  = csv.DictReader(csvfile)
        m=''
        d=''
        i = 0
        with open('monthly_prices.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                date = row["date"].split("-")
                month = date[1]
                day = date[2]
                if (i==0):
                    writer.writerow({'month':row["date"], 'price': row["price"]})
                    i+=1
                    last_month = month
                    continue
                if (last_month == month):
                    continue
                else:
                    writer.writerow({'month':row["date"], 'price': row["price"]})
                    last_month = month


                



csv_from_excel(get_xls_file(daily_url))

monthly_prices()
