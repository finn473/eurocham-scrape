import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
company_name = []
company_site = []
company_num = []
company_email = []

def extract_numeric_characters(string):
    numeric_chars = ''.join(filter(str.isdigit, string))
    return numeric_chars

for x in range(0, 19): 
    url='https://www.eurocham.my/members-directory/?pageno='+str(x)
    responses = requests.get(url, headers=headers)
    s = BeautifulSoup(responses.content, 'html.parser')
    result = s.find_all('a', class_='btn-morph')
    id_code = ""
    id_list = []
    for y in range(0, len(result)):
        for x in range(str(result[y]).find('data-itemid=')+13, len(str(result))):
            if str(result)[x] != ' ':
                id_code += str(result[y])[x]
            else:
                id_code = extract_numeric_characters(id_code)
                id_list.append(id_code)
                id_code = ""
                break
        url='https://www.eurocham.my/script?html&section=pagedetail&osp=610&type=osp&itemid='+str(id_list[y])
        responses2 = requests.get(url, headers=headers)
        s2 = BeautifulSoup(responses2.text, 'html.parser')
        company_name.append(s2.h3.text)
        company_site.append(s2.find_all('a')[0].text)
        company_num.append(extract_numeric_characters(s2.find_all('a')[1].text))
        company_email.append(s2.find_all('a')[2].text)

df = pd.DataFrame()    
df['NAME'] = company_name
df['WEBSITE'] = company_site
df['TELEPHONE'] = company_num
df['EMAIL'] = company_email
df.to_csv('eurocham_site_list.csv')