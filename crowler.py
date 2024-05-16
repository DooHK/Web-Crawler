import requests
import time
class Crowler:
    def __init__(self):
        self
    def request(self,url):
        try:
            response = requests.get(url)
        except Exception as e:
            print("오류 발생")
            print(e)
            print("5초 후 재시도")
            time.sleep(5)
            self.request(url)
            # 재귀함수 호출

        if response.status_code != 200:
            print(response.status_code)
            raise f'${response.status_code}'

        return response.text  # HTML 데이터