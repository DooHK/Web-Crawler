from bs4 import BeautifulSoup
from PySide6 import QtWidgets, QtCore
from crowler import Crowler
import requests
import time
import csv
import random
from selenium import webdriver
import pandas as pd
import queue
import threading
# from request import request

class coupang(Crowler):

    def __init__(self):
        super().__init__()
        self.header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
            ,"Accept-Language":"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}
        self.my_arr = []      # 정제된 데이터를 저장할 array
        self.is_first = True  # 프로그램을 처음 실행시켰는지 여부
        self.target = ["물", "생수"]  # 1개라도 포함되어야함
        self.excepts = []  # 1개라도 포함되면 안됨

    def request(self,page_num,url,header,writer):
        response = requests.get(url,headers=header)
        if response.status_code != 200:
            print(response.status_code)
            raise f'${response.status_code}'
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("[class=search-product]")  # 광고제거

        link_list = []

        rank = 1
        for item in items:
            name = item.select_one(".name")
            price = item.select_one(".price-value")  # 리퍼상품일 경우 None
            if not price:
                continue

            link = f"https://www.coupang.com{item.a['href']}"
            thumb = item.select_one(".search-product-wrap-img")

            name = "" if not name else name.text
            price = "" if not price else price.text
            if thumb.get("data-img-src"):
                img_url = f"https:{thumb.get('data-img-src')}"
            else:
                img_url = f"https:{thumb.get('src')}"
            img_url = img_url.replace("230x230ex", "700x700ex")

            writer.writerow([name, price, link, img_url])

            print(f"{page_num}페이지: {rank}위 {name} {price}원, {link}")
            print()

            link_list.append(link)

            rank += 1

        return link_list
            
    def pdp(self,url,header,writer,instance):
        response = requests.get(url, headers=header)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        brand = soup.select_one(".prod-brand-name")
        title = soup.select_one(".prod-buy-header__title").text.strip()
        seller = soup.select_one(".prod-sale-vendor-name")
        prod_other_seller_count = soup.select_one(".prod-other-seller-count")

        offer_badge_item = soup.select_one(".offer-badge-item")  # 리퍼 제품에 붙음

        prod_sale_price = soup.select_one(".prod-sale-price")  # 현재 판매가. text로 추출할것
        prod_coupon_price = soup.select_one(".prod-coupon-price")  # 회원 할인가. text로 추출할것

        prod_option_item = soup.select(".prod-option__item")  # 옵션

        prod_description = soup.select(".prod-description .prod-attr-item")  # 상세정보

        brand = "" if not brand else brand.text.strip()
        seller = "로켓배송" if not seller else seller.text.strip()

        if offer_badge_item:
            print(f"{offer_badge_item.string} 입니다.\n")

        prod_info_text = ""

        if brand:
            prod_info_text += f"브랜드: {brand}, "

        if title:
            prod_info_text += f"제품명: {title}"

        # 현재 판매가
        if prod_sale_price:
            prod_sale_price = prod_sale_price.select_one(".total-price").text.strip()
            prod_info_text += f", 현재 판매가: {prod_sale_price}"

        # 회원 할인가
        if prod_coupon_price:
            prod_coupon_price = prod_coupon_price.select_one(".total-price").text.strip()
            prod_info_text += f", 회원 할인가: {prod_coupon_price}"

        if seller:
            prod_info_text += f", 판매자: {seller}"

        if prod_other_seller_count:
            prod_other_seller_count = (
                "없음"
                if not prod_other_seller_count.text
                else prod_other_seller_count.text.strip()
            )
            prod_info_text += f", 다른 판매자: {prod_other_seller_count}"

        print(prod_info_text)
        instance.update_log(prod_info_text)

        # 옵션
        if prod_option_item:
            option_list = []
            for i in prod_option_item:
                option_list.append(
                    f'{i.select_one(".title").string.strip()}: {i.select_one(".value").string.strip()}'
                )
            prod_option_item = ", ".join(option_list)
            print(prod_option_item)
            # instance.log_text.append(prod_option_item)
        else:
            prod_option_item = None

        # 상세정보
        if prod_description:
            description_list = []
            for text in prod_description:
                description_list.append(text.string)
            prod_description = ", ".join(description_list)
            print(prod_description)
            # instance.log_text.append(prod_description)
        else:
            prod_description = None

        writer.writerow(
            [
                brand,
                title,
                prod_sale_price,
                prod_coupon_price,
                seller,
                prod_other_seller_count,
                prod_option_item,
                prod_description,
                url,
            ]
        )

    def excute(self,mall_name:str, keyword:str,sorting_type:str,total_page:int,is_exel:bool, instance ):
        
        
        link_list = []

        with open(
            f"coupang_discovery_{keyword}.csv", "w", newline="", encoding="utf-8"
        ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Price", "Link", "Img_url"])
            
            for page_num in range(1, total_page+1):
                if sorting_type == "판매량 순":
                    url = f"https://www.coupang.com/np/search?rocketAll=false&searchId=41e6c4846ffd4eb2953c13ba69d61a6d&q={keyword}&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page={page_num}&trcid=&traid=&filterSetByUser=true&channel=&backgroundColor=&searchProductCount=798215&component=&rating=0&sorter=saleCountDesc&listSize=72"
                elif sorting_type == "쿠팡 추천순":
                    url = f"https://www.coupang.com/np/search?component=&q={keyword}&page={page_num}&listSize=72"
                if not page_num:
                    break
                print(page_num)
                #term 두기
                sleeptime= random.uniform(3,6)
                time.sleep(sleeptime)
                link_list += self.request(page_num, url,self.header,writer)

        print(link_list)
        
        time.sleep(1)
        print(f"{len(link_list)}개 {keyword} 상세페이지 스크랩 시작")
       
        print()

        print(1111)
        with open(f"coupang_pdp_{keyword}.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            print(2222)
            writer.writerow(
                ["브랜드", "제품명", "현재 판매가", "회원 할인가", "판매자", "다른 판매자", "옵션", "상세정보", "URL"]
            )
            print(3333)
            for e, url in enumerate(link_list,1):
                sleeptime= random.uniform(3,6)
                time.sleep(sleeptime)
                print(f"<<<<<{e}>>>>>")
                instance.log_text.append(f"<<<<<{e}>>>>>") ##인터페이스 logging
                print(url)
                instance.log_text.append(url)
                pdp_thread = threading.Thread(target=self.pdp, args=(url,self.header,writer,instance))
                pdp_thread.start()
                # pdp_thread.join()
                print()
                instance.log_text.append("\n")

        #엑셀로 저장할건지의 여부
        if is_exel == True:
            # 결과를 DataFrame으로 저장
            df = pd.DataFrame(link_list, columns=["Link"])
            
            # Excel 파일로 저장
            excel_file_name = f"coupang_discovery_{keyword}.xlsx"
            df.to_excel(excel_file_name, index=False)

            with pd.ExcelWriter(excel_file_name) as writer:
                df.to_excel(writer, index=False)
                writer.save()

            print(f"엑셀파일 {excel_file_name} 저장되었습니다.")
        print("finished")