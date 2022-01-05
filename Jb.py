import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    #url = f'https://www.indeed.com/jobs?q=python%20developer&l=New%20York%2C%20NY&start={page}&vjk=e8379b3f84a77edf'
    #url = f'https://www.indeed.com/jobs?q=AI%20&l=New%20York%2C%20NY&start={page}&vjk=7ea584a878202545'
    url = f'https://nl.indeed.com/jobs?q=Machine+Learning&l=Amsterdam&radius=50&start={page}'
    #url = f'https://nl.indeed.com/jobs?q=AI+&l=Amsterdam&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content,'html.parser')
    return soup

def transform(soup):
    #divs = soup.find_all('table', class_ = 'jobCard_mainContent big6_visualChanges')
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    for item in divs:
        title = item.find('h2', class_ ='jobTitle').text.strip()
        company = item.find('span', class_ ='companyName').text.strip()
        try:
            #salary = item.find('span', class_ ='estimated-salary').text.strip()
            salary = item.find('div', class_ ='salary-snippet').text.strip()
        except:
            salary = ''
        summary = item.find('div',{'class' : 'job-snippet'}).text.strip().replace('\n','')
        #summary = item.find('div',{'class' : 'heading6'}).text.strip().replace('\n','')
        job = {
            'title': title,
            'company':company,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return

joblist =[]

for i in range(0,91,10):
    print(f'Getting page, {i}')
    c = extract(i) 
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('MLjobsinAmsterdam1.csv')