from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chrome 옵션 설정
chrome_options = Options()
# chrome_options.add_argument('--headless')  # 필요한 경우 헤드리스 모드 활성화

# WebDriver 초기화
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1) 로그인 페이지 진입
    driver.get("https://sso.kaist.ac.kr/auth/kaist/user/login/view")

    # 페이지 로딩을 위해 잠시 대기
    wait = WebDriverWait(driver, 10)

    # 현재 URL 출력 (디버깅용)
    print("현재 페이지 URL:", driver.current_url)
    print("현재 페이지 제목:", driver.title)

    # 로그인 폼 찾기
    try:
        # 여러 가능한 선택자 시도
        selectors = [
            (By.NAME, "user_id"),
            (By.ID, "user_id"),
            (By.CSS_SELECTOR, "input[name='user_id']"),
            (By.CSS_SELECTOR, "input[type='text']")
        ]
        
        username_field = None
        password_field = None
        
        for by, selector in selectors:
            try:
                username_field = wait.until(EC.presence_of_element_located((by, selector)))
                if username_field:
                    print(f"아이디 입력 필드를 찾았습니다: {selector}")
                    break
            except:
                continue

        # 비밀번호 필드 찾기
        pwd_selectors = [
            (By.NAME, "password"),
            (By.ID, "password"),
            (By.CSS_SELECTOR, "input[type='password']")
        ]
        
        for by, selector in pwd_selectors:
            try:
                password_field = wait.until(EC.presence_of_element_located((by, selector)))
                if password_field:
                    print(f"비밀번호 입력 필드를 찾았습니다: {selector}")
                    break
            except:
                continue

        if username_field and password_field:
            # 사용자에게 로그인 정보 입력 요청
            print("\n로그인 정보를 입력해주세요.")
            username = input("KAIST ID: ")
            password = input("비밀번호: ")

            # 로그인 정보 입력
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)

            # 로그인 버튼 찾기 및 클릭
            submit_selectors = [
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.ID, "submit"),
                (By.CLASS_NAME, "btn-submit"),
                (By.XPATH, "//button[contains(text(), '로그인')]")
            ]
            
            for by, selector in submit_selectors:
                try:
                    login_submit = wait.until(EC.element_to_be_clickable((by, selector)))
                    if login_submit:
                        print("로그인 버튼을 찾았습니다.")
                        login_submit.click()
                        break
                except:
                    continue

            # 로그인 후 페이지 로딩 대기
            time.sleep(5)

            print("\n로그인 시도 완료!")
            print("현재 페이지 URL:", driver.current_url)
        else:
            print("로그인 폼을 찾을 수 없습니다.")
    
    except Exception as e:
        print("에러 발생:", str(e))
    
    # 사용자 입력을 기다림
    input("\n종료하려면 엔터 키를 누르세요...")

finally:
    # 브라우저 종료
    driver.quit()