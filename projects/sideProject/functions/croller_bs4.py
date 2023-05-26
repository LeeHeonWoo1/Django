from bs4 import BeautifulSoup
import requests
from urllib.parse import quote

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}


def get_job_title(keyword):
  quoted_keyword = quote(keyword)
  url = f'https://www.saramin.co.kr/zf_user/search?searchword={quoted_keyword}&go=&flag=n&searchMode=1&searchType=search&search_done=y&search_optional_item=n'
  res = requests.get(url, headers=header)
  if res.status_code == 200:
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('h2', 'job_tit')
    job_list = []
    for job in results:
      job_list.append(job.text)
      
    return job_list
    
  else:
    print(res.status_code)