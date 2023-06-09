from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
from starlette.config import Config

config = Config(r'C:\Users\OWNER\Desktop\Django\projects\sideProject\.env')

header = {'User-Agent':config('USER_AGENT')}

def get_job_title(keyword):
  quoted_keyword = quote(keyword)
  url = f'https://www.saramin.co.kr/zf_user/search?searchword={quoted_keyword}&go=&flag=n&searchMode=1&searchType=search&search_done=y&search_optional_item=n'
  res = requests.get(url, headers=header)
  if res.status_code == 200:
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    jobs = soup.find_all('h2', 'job_tit')
    job_list = []
    for job in jobs:
      job_name = job.text.replace('\n', '')
      job_list.append(job_name)
      
    com_list = []
    comps = soup.find_all('strong', 'corp_name')
    for comp in comps:
      comp_name = comp.text.replace(' ', '')
      comp_name = comp_name.replace('\n', '')
      com_list.append(comp_name)
    
    result_list = []
    for content in zip(job_list, com_list):
      result_list.append(list(content))
    
    return result_list
    
  else:
    print(res.status_code)
    
get_job_title('python')