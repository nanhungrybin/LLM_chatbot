from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# 모든 키워드 검색할 때 주석 해제
# from urllib.parse import quote

import requests
import time
import datetime

# google scholar 웹사이트 접근 -> 검색 함수
def search_google_scholar(query):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://scholar.google.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.submit()
    return driver

# pdf 링크가 있는 링크만 추출 함수
def extract_pdf_links(html):
    soup = BeautifulSoup(html, "html.parser")
    pdf_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.startswith("http") and href.endswith(".pdf"):
            pdf_links.append(href)
    return pdf_links

# pdf 다운로드 함수
def download_pdf(pdf_links):
    for i, pdf_link in enumerate(pdf_links, start=1):
        try:
            response = requests.get(pdf_link)
            # 논문의 제목 가져오기
            title = pdf_link.split("/")[-1].split(".pdf")[0]
            # PDF 파일 이름 설정
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{title}_{timestamp}.pdf"
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Failed to download PDF: {e}")

# 나중에 모든 키워드 대상으로 할 경우 주석 해제
# language_label = "Korean" # or "English"
# TopicKeywords = {
#     "Korean": ["사출성형", "용접", "단조", "프레스"],
#     "English": ["Injection Molding", "Welding", "Forging", "Pressing"]
# }
# selected_keywords = TopicKeywords[language_label]

start_page = 0
query = '사출성형'
driver = search_google_scholar(query)
# current_url = f"https://scholar.google.com/scholar?start={start_page}&q={'사출성형'}&hl=ko&as_sdt=0,5"
# # 페이지 열기
# driver.get(current_url)
# print(f"현재 페이지: {current_url}")
# html = driver.page_source
# pdf_links = extract_pdf_links(html)
# # PDF 다운로드
# download_pdf(pdf_links)
try:
    while True:
        # 현재 페이지 URL
        current_url = f"https://scholar.google.com/scholar?start={start_page}&q={query}&hl=ko&as_sdt=0,5"
        # 페이지 열기
        driver.get(current_url)
        print(f"현재 페이지: {current_url}")
        html = driver.page_source
        pdf_links = extract_pdf_links(html)
        # PDF 다운로드
        download_pdf(pdf_links)
        time.sleep(3)
        # 페이지 번호 증가
        start_page += 10
except Exception as e:
    print(f"An error occurred: {e}")
    
# # 모든 키워드 검색 시에 주석 해제(error 존재)
# # 페이지 넘기면서 작동
# for keyword_idx, keyword in enumerate(selected_keywords):
#     driver = search_google_scholar(keyword)
#     encoded_query = quote(keyword)
#     try:
#         while True:
#             # 현재 페이지 URL
#             current_url = f"https://scholar.google.com/scholar?start={start_page}&q={encoded_query}&hl=ko&as_sdt=0,5"
#             # 페이지 열기
#             driver.get(current_url)
#             print(f"현재 페이지: {current_url}")
#             html = driver.page_source
#             pdf_links = extract_pdf_links(html)
#             # PDF 다운로드
#             download_pdf(pdf_links)
#             # 페이지 번호 증가
#             start_page += 10
#             #마지막 페이지에서 pdf 다운로드 진행하고 break 걸어서 다음 keyword로 넘어가게 만들어야함!!!!!!!!!!!!!!!!!!!!!!!!
#     except Exception as e:
#         print(f"An error occurred: {e}")
    
#     # 현재 키워드의 모든 페이지를 탐색한 후 다음 키워드로 이동
#     start_page = 0
    
#     # 3초 대기
#     time.sleep(3)

