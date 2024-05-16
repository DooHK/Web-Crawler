from bs4 import BeautifulSoup
from crowler import Crowler
# from request import request

class nara(Crowler):
        # 전역변수 선언 및 초기화
    
    # 요청을 보내는 행위를 추상화한 function
    def __init__(self):
        super().__init__()
        self.URL = "https://cafe.naver.com/ArticleList.nhn?search.clubid=10050146&search.menuid=334&search.boardtype=L"
        self.my_arr = []      # 정제된 데이터를 저장할 array
        self.is_first = True  # 프로그램을 처음 실행시켰는지 여부
        self.target = ["삼성", "갤럭시북", "LG", "gram", "엘지", "그램"]  # 1개라도 포함되어야함
        self.excepts = ["삽니다", "매입", "구매", "구입"]  # 1개라도 포함되면 안됨
    
    
    def excute(self,URL):
        
        html = self.request(URL)
        #html 싹다 가져옴
        # 서버에 요청을 보내고 응답으로 HTML string 데이터를 받음

        soup = BeautifulSoup(html, 'html.parser')
        #print("soup : ",soup)
        #비슷한 느낌인듯
        # 파이썬 라이브러리 BeautifulSoup 를 이용해서 html 데이터를 파싱

        tr_arr = soup.select('#main-area > div.article-board:not([id="upperArticleList"]) > table > tbody > tr')
        # print("tr_arr", tr_arr)
        print(tr_arr[0])

        # 파싱된 html 데이터의 내부 tag 에 CSS Selector 로 순차적으로 접근해서,
        # 'tbody' 태그 하위의 모든 'tr' 태그들을 가져옴 (array 형태로)
        # 이 tr 태그가 바로 게시판 목록의 한줄, 한줄을 표현하는 태그! ('tr' 은 table row 의 줄임)
        # 목록의 한줄(row)에는 게시물 번호, 제목, 판매/구매 여부, 판매자닉네임, 시간, 조회수 등이 들어있음

        # tr 태그들을 for loop 을 이용해서 하나씩 분석
        for tr in tr_arr:
            is_new_item = True
            # 새로운 상품인지 여부를 표현하는 변수 생성
            # 기본적으로 '새로운 상품이 있을 것이다' 라는 접근으로 True 값을 넣음

            a_tag = tr.select_one('td.td_article a')
            # tr 태그 내부에 CSS Selector 로 접근해서 'a' 태그를 가져옴 ('a' 는 anchor 의 줄임)
            # a 태그에는 우리가 원하는 '제목' 이 들어있음

            map = {
                "title": a_tag.text.strip(),
                "url": a_tag["href"],
                "is_checked": False,
            }
            # 우리에게 딱 필요한 데이터만 정제하여 map 으로 만듦

            # 나의 데이터목록을 for loop 으로 확인
            for element in self.my_arr:
                # 기존에 확인했던 element 와 방금 새로 확인한 map 데이터가 같은지 비교
                if element["url"] == map["url"]:
                    is_new_item = False
                    # url 값이 같다면 새로운 데이터가 아님!
                    break

            # 만약 새로운 데이터라면
            if is_new_item:
                self.my_arr.insert(0, map)
                # 나의 데이터목록에 추가

        print("--------------")
        print(self.my_arr[0])
        