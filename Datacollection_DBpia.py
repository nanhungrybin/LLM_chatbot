# 논문 이름에 사출성형이 들어가는 논문 모두 다운로드
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService

import time

#DBpia 로그인, 검색 자동화
def search_DBpia(query, username, password):

    """
    DBpia 웹사이트에서 로그인하고, 특정 쿼리를 사용하여 검색하는 함수.

    Args:
        query (str): 검색할 쿼리 문자열.
        username (str): DBpia 로그인에 사용할 사용자 이름.
        password (str): DBpia 로그인에 사용할 비밀번호.

    Returns:
        webdriver.Chrome: 검색된 페이지를 포함한 Chrome WebDriver 객체.
    """

    options = Options()
    options.add_argument('--disable-features=BlockCredentialedSubresources')
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://dbpia.co.kr/")
    time.sleep(2)  # 페이지가 로드되기를 기다립니다.

    #소속기관 버튼 클릭
    school = driver.find_element(By.XPATH, '//*[@id="dpHeaderNavWrap"]/section/a[1]')
    school.click()
    time.sleep(1)

    # 검색창에 학교명 입력 후 제출
    school_box = driver.find_element(By.ID, "dev_search")
    school_box.send_keys('서울과학기술대학교')
    school_box.send_keys(Keys.RETURN)
    
    #학교이름 클릭
    school_name = driver.find_element(By.XPATH, '//*[@id="ICST00000602"]/span')
    school_name.click()
    time.sleep(1)
    
    #학교 인증
    school_name_인증 = driver.find_element(By.XPATH, '//*[@id="b2b_login_basic"]/div[9]/div/ul[1]')
    school_name_인증.click()
    time.sleep(1)

    # 로그인 페이지에서 아이디와 비밀번호 입력
    username_field = driver.find_element(By.ID, "b2b_local_login_id")
    username_field.send_keys(username)

    password_field = driver.find_element(By.ID, "b2b_local_login_pw")
    password_field.send_keys(password)
    time.sleep(1)

    # login 버튼 클릭
    element = driver.find_element(By.XPATH, '//*[@id="local_login_btn"]/span')
    element.click()
    time.sleep(1)

    # 인증 버튼 클릭
    element2 = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/button')
    element2.click()
    time.sleep(1)
    
    # 검색하기
    search_name = driver.find_element(By.ID, "searchInput")
    search_name.send_keys(query)
    search_name.submit()
    time.sleep(5)

    return driver

# 논문 다운로드
def download_papers(driver):
    """
    DBpia 웹사이트에서 제목에 사출성형이 들어가는 논문을 다운로드하는 함수.

    Args:
        driver (webdriver.Chrome): 검색된 페이지를 포함한 Chrome WebDriver 객체.
    """
    page_num = 2
    while True:
        summary_elements = driver.find_elements(By.CLASS_NAME, 'thesisWrap')    
        for summary_element in summary_elements:
                title_element = summary_element.find_element(By.CLASS_NAME, 'thesis__tit')
                # 제목에 "사출성형"이 포함되어 있는지 확인
                if '사출성형' in title_element.text:
                    try:
                        # 다운로드 버튼이 있는지 확인
                        download_button = summary_element.find_element(By.CLASS_NAME, 'thesis__downBtn')
                        # 다운로드 버튼 클릭
                        driver.execute_script("arguments[0].click();", download_button)
                        print("다운로드 수행:", title_element.text)
                        time.sleep(1)
                    except NoSuchElementException:
                        print("다운로드 버튼이 없음:", title_element.text)

                    # 논문 다운로드 받으면 뜨는 창 x 표시 클릭
                    try:
                        X_button = driver.find_element(By.XPATH, '//*[@id="recommendedNodeWrapper"]/section[1]/button')
                        X_button.click()
                        time.sleep(1)
                    except:
                        pass

                # 권한 요청이 오는지 확인하고 클릭
                try:
                    alert_dialog = driver.find_element(By.XPATH, '//*[@id="alertDialogConfirm"]')
                    alert_dialog.click()
                    print("Alert dialog clicked.")
                except:
                    print("Alert dialog not found.")
        
        page_link = driver.find_element(By.XPATH, f'//a[contains(@onclick, "setPageNum({page_num})")]')
        page_link.click()
        time.sleep(1)

        # 다음 페이지로 이동하는 버튼 클릭 (10페이지마다)
        if page_num % 10 == 0:
            next_button = driver.find_element(By.ID, 'goNextPage')  # 다음 페이지로 이동하는 버튼의 ID
            next_button.click()
            time.sleep(5)

        # 다음 페이지 번호로 이동
        page_num += 1

# 사용
query = "사출성형"
username = "20102022"
password = "@@@"

driver = search_DBpia(query, username, password)
download_papers(driver)
