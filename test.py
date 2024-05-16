import requests
import time

url = 'https://www.coupang.com/'

try:
    response = requests.get(url)
except Exception as e:
    print("오류 발생")
    print(e)
    
    

if response.status_code != 200:
    print(response.status_code)
    raise f'${response.status_code}'

print('연결됨')