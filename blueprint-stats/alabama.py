import requests
from bs4 import BeautifulSoup as bs
from xlwt import Workbook
from time import time

base_url = ["http://www.ahsaa.org/schools?id=", "&school="]
url = "http://www.ahsaa.org/schools?id=523&school="

res = requests.get(url) 
cont = bs(res.text, "lxml")

headers = ['SCHOOL NAME', 'MAILING ADDRESS', 'CITY', 'COUNTY', 'SCHOOL WEBSITE', 'COLOR', 'MASCOT', 'AD NAME', 'AD PHONE', 'AD EMAIL', 'BOYS COACH', 'GIRLS COACH']
all_urls = []
school_names = []
address =[] 
city = []
county = []
website = []
ad_name = []
ad_phone = []
ad_email = []
boys_coach = []
girls_coach = [] 
mascot = []
color = []
for info in cont.findAll("option", value=True):
    all_urls.append(base_url[0] + info['value'] + base_url[1])
    school_names.append(info.get_text())

all_urls = all_urls[1:]
school_names = school_names[1:]
print("Total: "+str(len(all_urls)))
start = time()
for i in range(len(all_urls)):
    res = requests.get(all_urls[i])
    content = bs(res.text, "lxml")
    cont = content.findAll("td")
    address.append("-" if cont[5].get_text() == '' else cont[5].get_text()[:-21]+" "+cont[5].get_text()[-21:-16])
    city.append("-" if cont[9].get_text() == '' else cont[9].get_text())
    county.append("-" if cont[11].get_text() == '' else cont[11].get_text())
    website.append("-" if cont[15].get_text() == '' else "https://"+cont[15].get_text())
    color.append("-" if cont[25].get_text() == '' else cont[25].get_text())
    mascot.append("-" if cont[27].get_text() == '' else cont[27].get_text())
    ad_name.append("-" if cont[49].get_text() == '' else cont[49].get_text())
    ad_phone.append("-" if cont[51].get_text() == '' else cont[51].get_text())
    ad_email.append("-" if cont[53].get_text() == '' else cont[53].get_text())
    boys_coach.append("-" if cont[59].get_text() == '' else cont[59].get_text())
    girls_coach.append("-" if cont[61].get_text() == '' else cont[61].get_text())
    print(str(i) + " took " + str(time()-start))

wb = Workbook()
page = wb.add_sheet('All Data')
for i in range(len(school_names)):
    if(i<12): page.write(0,i, headers[i])
    page.write(i+1,0, school_names[i])
    page.write(i+1,1, address[i])
    page.write(i+1,2, city[i])
    page.write(i+1,3, county[i])
    page.write(i+1,4, website[i])
    page.write(i+1,5, color[i])
    page.write(i+1,6, mascot[i])
    page.write(i+1,7, ad_name[i])
    page.write(i+1,8, ad_phone[i])
    page.write(i+1,9, ad_email[i])
    page.write(i+1,10, boys_coach[i])
    page.write(i+1,11, girls_coach[i])
    print(str(i) + " took " + str(time()-start))

wb.save('info/alabama.xls')
