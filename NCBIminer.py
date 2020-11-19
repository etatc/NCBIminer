import time
import csv
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import re

#list of urls
fasta_urls = []
urls = []
genome = []
i=0
#establish a driver for scraping for all the urls
#!!!CHANGE ME!!!
DRIVER_PATH = "path/to/driver"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get("https://www.ncbi.nlm.nih.gov/nuccore/"+"change for the species you want")
#Clicks to the mrna section for the user
Mrna = driver.find_element_by_xpath("""//*[@data-value_id="mrna"]""").click()
only_nucleotides = driver.find_element_by_xpath("""//*[@data-value_id="nuccore"]""").click()
click_the_box = driver.find_element_by_xpath("""//*[@id="pageno"]""").click()
clear_the_box = driver.find_element_by_xpath("""//*[@id="pageno"]""").send_keys(Keys.BACKSPACE)
#!!!CHANGE ME!!!
no_for_box = driver.find_element_by_xpath("""//*[@id="pageno"]""").send_keys("whatever_page_to_start_on")
enter_the_no = driver.find_element_by_xpath("""//*[@id="pageno"]""").send_keys(Keys.ENTER)
#scrape the urls
totaltime =time.time()
#!!!change the i value to scrape all pages up to that point!!!
while i < 1:
    sscrape_time = time.time()
    time.sleep(5)
    page = driver.find_element_by_xpath("//html").get_attribute('outerHTML')
    soup = BeautifulSoup(''.join(page), "lxml")
    for link in soup.find_all(id="ReportShortCut6"):
        f = link.get('href')
        fasta_urls.append(f)
        s = re.sub(r'\?report=fasta', '', f)
        urls.append(s)
    next_page = driver.find_element_by_xpath("""//*[@class="active page_link next"]""").click()
    i = i+1
escrape_time = time.time() - sscrape_time
print(escrape_time)
with open('links.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for number, row in enumerate(urls):
        writer.writerow(urls[number])
driver.quit()

write_this_csv = []
for url in urls:
    sg_time = time.time()
    webpage = 'https://www.ncbi.nlm.nih.gov' + url
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(webpage)
    time.sleep(1)

    page = driver.find_element_by_xpath("//html").get_attribute('outerHTML')
    soup = BeautifulSoup(''.join(page), "lxml")
    stuff = []
    things = []
    for link in soup.find_all("a", attrs={"sfeat": "CDS"}):
        f = link.find_parent('span')
        q = f.contents[3]
        stuff.append(q)
        s = f.contents[7]
        things.append(s)
    mrna = []
    for thing in soup.find_all("span", attrs={"class": "ff_line"}):
        line = thing.contents[0]
        mrna.append(line)
    driver.quit()
    gene = ""
    for index, item in enumerate(mrna):
        fix = re.sub(" ", "", item)
        gene = gene + fix

    what = re.search('/gene=(.*)\n', stuff[0]).group(1)
    gene_name= re.sub(r'\"', "", what)

    h = re.search('  (.*)\n', stuff[0]).group(1)
    cds = re.sub(r'<', " ", h)

    almost = re.search('/product=(.*)\n', stuff[0]).group(1)
    product = re.sub(r'\"', "", almost)

    test1 = re.sub(r'\n*? ', '', things[0])
    test2 = re.sub(r'/translation="', '', test1)
    test3 = re.sub(r'\n', "", test2)
    amino_seq = re.sub(r'"', "", test3)

    start = re.search(' (.*)\.\.', cds).group(1)
    end = re.search('\.\.(.*)', cds).group(1)

    cds_region = gene[int(start) - 1:int(end)]
    promoter = gene[0:int(start) - 1]
    terminator = gene[int(end):len(gene)]

    write_this = [url, gene_name, product, gene, promoter, cds_region, terminator, amino_seq]
    write_this_csv.append(write_this)

    print(write_this)
    driver.quit()
    eg_time = time.time() - sg_time

    print(eg_time)

with open('yourcsvname.csv', 'w', newline='') as f:
    s_time = time.time()
    writer = csv.writer(f)
    for number, row in enumerate(write_this_csv):
        writer.writerow(write_this_csv[number])
e_time = time.time() - s_time
print(e_time)
print("Done")
totale_time = time.time() - totaltime
print(totale_time)