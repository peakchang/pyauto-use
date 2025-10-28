from func import *


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def trfficScript(getDict):

    pg.FAILSAFE_POINTS = [(0, 0), (1919, 0)]

    
    workType = {}
    # testWork = 'ok'
    testWork = None

    # siteLink = "http://localhost:3020"
    siteLink = "https://happy-toad2.shop"


    if getDict['group_val'] == '' or getDict['group_val'] is None:
        pg.alert('그룹을 선택 해 주세요!')
        sys.exit()
    else:
        workType['pr_group'] = getDict['group_val']

    
    

    newIp = ""
    oldIp = ""

    # 현재 날짜와 시간을 얻기 (경과된 시간을 찾기 위함)
    now = datetime.now()
    # 문자열 형식으로 변환
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

    if os.path.isfile('./work_time.txt') == False:
        with open('./work_time.txt', 'w') as file:
            file.write(f"{date_string} 시작하기!!")


    with open('./pc_id.txt', 'r') as file:
        pcId = file.read()

    errStatus = False

    workType['pr_work_type'] = ''
    
    while True:


        if getDict['workTypeVal'] == 'mix':
            # PC랑 모바일 한번씩 번갈아가면서 돌기!! (무한 루프 돌면서 바뀜)
            if workType['pr_work_type'] is None or workType['pr_work_type'] == "" or workType['pr_work_type'] == 'pc':
                workType['pr_work_type'] = 'mobile'
            else:
                workType['pr_work_type'] = 'pc'
        elif getDict['workTypeVal'] == 'pc':
            workType['pr_work_type'] = 'pc'
        elif getDict['workTypeVal'] == 'mobile':
            workType['pr_work_type'] ='mobile'

        print('전체 while문 돌기!!!!')
        # 전체 try / except!!! 작업 중간에 문제 생기면 창 닫아버림!!!!
        try:

            start_time = time.time()
            start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
            with open('./work_time.txt', 'a') as file:
                file.write(f"시작시간 : {start_time_str} ")


            # 아이피 변경 / 크롬 접속 while~~~~
            driver = ""
            retryCount = 0

            while True:
                retryCount += 1
                # 아이피 변경 부분!
                if getDict['ipval'] and retryCount == 1:
                    getIp = changeIp()
                    newIp = getIp
                    print(f"oldIp : {oldIp} / newIp : {newIp}")
                    if oldIp == newIp:
                        continue
                    oldIp = newIp

                    print('멈추는 경우? 왜?!')
                # 아이피 변경 부분 끝!!

                # 크롬 접속!! (기본 5초 주고 5초 내 접속 못하면 아이피 변경으로 돌아가기~~)
                if workType['pr_work_type'] == 'pc':
                    try:
                        # pcUser = getpass.getuser()
                        user_data_dir = tempfile.mkdtemp(prefix="selenium_profile_")
                        options = Options()
                        options.add_argument(f"--user-data-dir={user_data_dir}")  # 프로필 분리(누수 ↓)
                        service = Service()  # chromedriver PATH 잡혀있다고 가정

                        # 브라우저가 자동화된 테스트 소프트웨어에 의해 제어되고 있음을 감추기 위한 옵션
                        options.add_experimental_option("excludeSwitches", ["enable-automation"])
                        options.add_experimental_option("useAutomationExtension", False)


                        prefs = {
                            "profile.default_content_setting_values.notifications": 2,  # 1: 허용 / 2: 차단
                            # 팝업창 차단
                            "profile.default_content_setting_values.popups": 2,
                            # (선택) 침입적 광고 차단
                            "profile.managed_default_content_settings.ads": 2,
                            # (선택) 서드파티 쿠키 차단 → 광고 트래커 감소
                            "profile.block_third_party_cookies": True,
                        }

                        options.add_experimental_option("prefs", prefs)

                        # 🚫 자동 팝업 알림, 브라우저 자체 알림도 비활성화
                        options.add_argument("--disable-notifications")
                        options.add_argument("--disable-popup-blocking")

                        # 캐시 및 저장된 데이터 관련
                        options.add_argument("--disable-background-timer-throttling")
                        options.add_argument("--disable-backgrounding-occluded-windows")
                        options.add_argument("--disable-renderer-backgrounding")
                        options.add_argument("--disable-features=TranslateUI")

                        # PDH 에러 방지를 위한 추가 옵션
                        options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 사용 안함
                        options.add_argument("--no-sandbox")  # 샌드박스 비활성화
                        options.add_argument("--disable-gpu")  # GPU 가속 비활성화
                        options.add_argument("--disable-software-rasterizer")
                        
                        # 성능 모니터링 비활성화 (PDH 관련)
                        options.add_argument("--disable-background-networking")
                        options.add_argument("--metrics-recording-only")
                        options.add_argument("--disable-background-timer-throttling")
                        
                        # 쿠키 및 세션 완전 초기화
                        options.add_argument("--disable-background-networking")
                        options.add_argument("--disable-sync")

                        driver = webdriver.Chrome(options=options)
                        driver.set_page_load_timeout(3)

                        driver.get('https://www.naver.com')
                        
                        driver.set_window_size(1300, 800)
                        driver.set_window_position(0,0)
                        
                        break
                    except TimeoutException as e:

                        print(e)
                        print("❌ 1초 초과 → TimeoutException 발생")
                        print('크롬 창 오픈 실패!!')
                        if driver:
                            driver.quit()
                        pass
                else:
                    try:
                        res = requests.get(f"{siteLink}/api/v7/res_traffic_work/get_user_agent").json()
                        print(res)
                        print(res['user_agent_info']['ua_content'])
                        if res['status'] == True and res['user_agent_info']['ua_content'] is not None:
                            userAgentInfo = res['user_agent_info']['ua_content']
                            try:
                                pcUser = getpass.getuser()
                                user_data_dir = tempfile.mkdtemp(prefix="selenium_profile_")
                                options = Options()
                                options.add_argument(f"--user-data-dir={user_data_dir}")  # 프로필 분리(누수 ↓)
                                service = Service()  # chromedriver PATH 잡혀있다고 가정
                                
                                # user_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\default'
                                # options.add_argument(f"user-data-dir={user_data}")
                                # options.add_argument(f'--profile-directory=Profile {profileInfo['pl_number']}')

                                options.add_argument(f'user-agent={userAgentInfo}')

                                # 캐시 및 저장된 데이터 관련
                                options.add_argument("--disable-background-timer-throttling")
                                options.add_argument("--disable-backgrounding-occluded-windows")
                                options.add_argument("--disable-renderer-backgrounding")
                                options.add_argument("--disable-features=TranslateUI")


                                # PDH 에러 방지를 위한 추가 옵션
                                options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 사용 안함
                                options.add_argument("--no-sandbox")  # 샌드박스 비활성화
                                options.add_argument("--disable-gpu")  # GPU 가속 비활성화
                                options.add_argument("--disable-software-rasterizer")
                                
                                # 성능 모니터링 비활성화 (PDH 관련)
                                options.add_argument("--disable-background-networking")
                                options.add_argument("--metrics-recording-only")
                                options.add_argument("--disable-background-timer-throttling")
                                
                                # 쿠키 및 세션 완전 초기화
                                options.add_argument("--disable-background-networking")
                                options.add_argument("--disable-sync")
                                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                                options.add_experimental_option("useAutomationExtension", False)
                                driver = webdriver.Chrome(options=options)
                                driver.get('https://www.naver.com')
                                start_time = time.time()
                                # 모바일에서 에러가 많이 나네 30초 대기 해서 안되면 리셋!!
                                element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "HOME_SHORTCUT")))
                                # 다 불러와졌으면 4~5초 정도 대기
                                wait_float(3.8,5.2)
                                driver.set_page_load_timeout(12)
                                driver.set_window_size(1000, 800)
                                driver.set_window_position(0,0)
                                break
                            except Exception as e:
                                print(e)
                                print('크롬 창 오픈 실패!!')
                                if driver:
                                    driver.quit()
                                pass

                    except Exception as e:
                        print(str(e))
                        print('프로필 정보 불러오기 오류!!')
                        continue

                
            focus_window('NAVER - Chrome')
            
            driver.set_page_load_timeout(35)
            active_chrome(driver)

            # 중복된 키워드는 검색하기 않기 위해서~~~
            workedKeywordArr = []

            # 작업 타입 (일반 키워드 검색 (notWork) / 작업 키워드 검색 (work) / 작업 키워드 클릭 (realwork) 배열 만들기 )
            try:
                activeArrLengthArr = [6,7]
                activeArrInnerArr = [3,4]
                workArr = create_active_array(activeArrLengthArr, activeArrInnerArr)

                # activeArrLengthArr = [7,8]
                # activeArrInnerArr = [4,5]
                # realWorkRanNom = random.randint(2,3)
                # workArr = create_active_array_many(activeArrLengthArr, activeArrInnerArr, realWorkRanNom)
            except Exception as e:
                print(str(e))
                pg.alert('알수없는 오류!!')
                sys.exit(1)

            print(workArr)


            if testWork == 'ok':
                # workArr = ['notwork','realwork','work','realwork','work','notwork']
                # workArr = ['work', 'realwork']
                workArr = ['realwork', 'work']
                pass
            # 작업할 배열을 생성! workArr 은 'notWork'
            for work in workArr:
                print(f'{work} 작업 돌기!!!!!')
                if work == 'notWork':
                    # notWork 에서는 키워드에서 찾아서 검색하기!!
                    # 먼저 키워드를 불러오자!!!

                    while True:
                        print('not work 불러와야지?!')
                        try:
                            
                            res = requests.get(f"{siteLink}/api/v7/res_traffic_work/load_notwork").json()
                            if res['status'] == False:
                                continue

                            workInfo = res['get_keyword']
                            if workInfo['pk_content'] in workedKeywordArr:
                                wait_float(0.5,1.2)
                                continue
                            else:
                                break
                        except Exception as e:
                            print(str(e))
                            pass
                    print('nowWork 나옴!!!')
                    naverMainSearch(driver, workInfo['pk_content'], workType['pr_work_type'])
                    wait_float(1.2,1.9)

                    # onotherWorkNum = random.randint(1, 2)
                    onotherWorkNum = 1
                    if workType['pr_work_type'] == 'mobile':
                        searchStatus = searchMobileAnotherList(driver, onotherWorkNum, testWork, workInfo['pk_content'])
                    else:
                        searchStatus = searchPcAnotherList(driver, onotherWorkNum, testWork, workInfo['pk_content'])

                    
                    if searchStatus == False:
                        break

                elif work == 'work':
                    # 먼저 작업 내용 불러오기!! clickStatus 가 false 인거 아무거나 하나 불러오기!!

                    errCount = 0
                    refresh = False # 아래 while 문에서만 쓰는 변수, 중복이 계속 있을시 1개밖에 안남았다고 판단, True 값을 넘겨서 조회 상태 전체 초기화
                    while True:
                        errCount += 1
                        print(workedKeywordArr)
                        wait_float(0.3,0.5)
                        while True:
                            print('work 정보 가지고 오기!!!!')
                            try:
                                res = requests.post(f"{siteLink}/api/v7/res_traffic_work/load_work",
                                { 'group' : workType['pr_group'], 'refresh' : refresh }).json()
                                print(res)
                                refresh = False
                                if res['status'] and res['get_work']:
                                    print(res)
                                    workInfo = res['get_work']
                                    break

                            except Exception as e:
                                print(str(e))
                                pass
                            
                        if workInfo['st_subject'] in workedKeywordArr:
                            if errCount > 5:
                                refresh = True
                            continue
                        else:
                            workedKeywordArr.append(workInfo['st_subject'])
                            break
                    
                    naverMainSearch(driver, workInfo['st_subject'], workType['pr_work_type'])

                    # 먼저 아무거나 클릭 하나!!!
                    # onotherWorkNum = random.randint(1, 2)
                    onotherWorkNum = 1
                    if workType['pr_work_type'] == 'mobile':
                        searchStatus = searchMobileAnotherList(driver, onotherWorkNum, testWork)
                    else:
                        searchStatus = searchPcAnotherList(driver, onotherWorkNum, testWork)

                    
                    if searchStatus == False:
                        break


                    
                    

                    # 본 조회 작업 GOGO!!!
                    # 아래 함수에서 workInfo['work_type'] 가 click 이면 클릭 / 아니면 조회만 하게 해놨음
                    # 여기는 그냥 조회니까 check로 맞춰주기~
                    workInfo['work_type'] = 'check'
                    if workType['pr_work_type'] == 'mobile':
                        targetWork = searchMobileContent(driver ,workInfo ,workType ,testWork)
                    else:
                        targetWork = searchPcContent(driver ,workInfo ,workType ,testWork)

                    print(targetWork)
                    while True:
                        wait_float(0.3,0.9)
                        # chkRateStatus 는 st_use가 FALSE 인 값을 찾아서 한것이므로 TRUE로 업데이트!!
                        try:
                            res = requests.post(f"{siteLink}/api/v7/res_traffic_work/update_traffic_work", {'status' : targetWork['status'], 'rate' : f"{targetWork['page']}/{targetWork['rate']}", 'st_id' : workInfo['st_id']}).json()

                            print(res)
                            if res['status'] == True:
                                break
                        except Exception as e:
                            print(str(e))
                            continue

                elif work =='realwork':
                    errCount = 0
                    while True:
                        errCount += 1
                        try:
                            res = requests.get(f"{siteLink}/api/v7/res_traffic_work/load_realwork?group={workType['pr_group']}&work_type={workType['pr_work_type']}").json()
                            print('realwork 정보 가지고 오기!!')
                            print(res)
                            if res['status']:
                                workInfo = res['get_realwork']
                                if workInfo['st_subject'] not in workedKeywordArr:
                                    workedKeywordArr.append(workInfo['st_subject'])
                                    break
                                else:
                                    if errCount > 5:
                                        errCount = 0
                                        workedKeywordArr = []
                                    print('중복된 키워드!!!')

                            
                        except Exception as e:
                            print(str(e))
                            pass

                    # # 조회하는 리스트에 추가하기~~
                    # while True:
                    #     try:
                    #         res = requests.post(f"{siteLink}/api/v7/res_traffic_work/update_chk_realwork", {'st_id' : workInfo['st_id'], 'type' : workType['pr_work_type']}).json()
                    #         print(res)
                    #         if res['status']:
                    #             break
                    #     except:
                    #         pass
                    
                    naverMainSearch(driver, workInfo['st_subject'], workType['pr_work_type'])

                    # 모바일은 나중에~~~~ 안할 가능성도 크고~~~~
                    # 먼저 아무거나 클릭 하나!!!
                    # onotherWorkNum = random.randint(1, 2)
                    onotherWorkNum = 1
                    if workType['pr_work_type'] == 'mobile':
                        searchStatus = searchMobileAnotherList(driver, onotherWorkNum, testWork)
                    else:
                        searchStatus = searchPcAnotherList(driver, onotherWorkNum, testWork)
                    
                    if searchStatus == False:
                        break


                    # 본 조회 작업 GOGO!!!
                    # 아래 함수에서 workInfo['work_type'] 가 click 이면 클릭 / 아니면 조회만 하게 해놨음
                    # 여기는 그냥 클릭이니까 click 으로 맞춰주기~
                    workInfo['work_type'] = 'click'
                    if workType['pr_work_type'] == 'mobile':
                        targetWork = searchMobileContent(driver ,workInfo ,workType ,testWork)
                    else:
                        targetWork = searchPcContent(driver ,workInfo ,workType ,testWork)

                    
                    print(targetWork)
                    while True:
                        wait_float(0.3,0.9)
                        # chkRateStatus 는 st_use가 FALSE 인 값을 찾아서 한것이므로 TRUE로 업데이트!!
                        try:
                            res = requests.post(f"{siteLink}/api/v7/res_traffic_work/update_traffic_realwork", {'status' : targetWork['status'], 'rate' : f"{targetWork['page']}/{targetWork['rate']}", 'st_id' : workInfo['st_id'], 'work_type' : workType['pr_work_type']}).json()

                            if res['status'] == True:
                                break
                        except Exception as e:
                            print(str(e))
                            continue

            
            # 작업이 끝났으면 마지막 트래픽 에다가 현재 시간 업데이트
            while True:
                wait_float(0.3,0.9)
                try:
                    res = requests.get(f"{siteLink}/api/v7/res_traffic_work/update_last_traffic?sl_id={pcId}").json()
                    if res['status'] == True:
                        break
                except Exception as e:
                    print(str(e))
                    continue
            end_time = time.time()
            end_time_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
            elapsed_time = end_time - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            with open('./work_time.txt', 'a') as file:
                file.write(f"종료시간 : {end_time_str} / 프로그램 실행 시간: {minutes}분 {seconds}초\n")
            close_driver(driver, service, user_data_dir)

            continue
        except Exception as e:
            print(str(e))
            close_driver(driver, service, user_data_dir)
            




def goRateChkScript():

    # 주소 정보 담긴 엑셀 불러오기
    rateExFile = load_workbook('./etc/rate_work.xlsx')
    rateEx = rateExFile.active

    rateExCount = 0
    while True:
        rateExCount += 1
        keyword = rateEx.cell(rateExCount,1).value
        link = rateEx.cell(rateExCount,2).value
        sameLinkVal = rateEx.cell(rateExCount,3).value
        if keyword is None:
            for i in range(3):
                fr = 1600    # range : 37 ~ 32767
                du = 500     # 1000 ms ==1second
                sd.Beep(fr, du)
            pg.alert('순위 체크가 끝났습니다.')
            sys.exit(0)

        pageCount = 1
        
        while True:
            wait_float(1.2,1.9)
            pageCount += 1
            print(pageCount)
            if pageCount > 10:
                rateEx.cell(rateExCount,4).value = "못찾음!"
                # rateEx.cell(rateExCount,4).value = getHrefonClick
                rateExFile.save('./etc/rate_work.xlsx')
                break

            startCount = (pageCount - 2) * 15 + 1
            # encoded_keyword = urllib.parse.quote(keyword)
            encoded_keyword = keyword.replace(" ", "+")
            
            
            url = f"https://search.naver.com/search.naver?nso=&page={pageCount}&query={encoded_keyword}&sm=tab_pge&start={startCount}&where=web"
            
            print(url)
            try:
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                articles = soup.find_all(class_='link_tit')

                if len(articles) == 0:
                    rateEx.cell(rateExCount,4).value = "없음!"
                    rateExFile.save('./etc/rate_work.xlsx')
                    print(html)
                    for i in range(3):
                        fr = 1800    # range : 37 ~ 32767
                        du = 500     # 1000 ms ==1second
                        sd.Beep(fr, du)
                        print('에러발생!!')
                    break
            except Exception as e:
                print(str(e))

            searchSeccessStatus = False
            for idx, article in enumerate(articles):
                linkTag = article['href']
                print(f"link : {link} // linkTag : {linkTag}")
                if sameLinkVal:
                    if link == linkTag:
                        searchSeccessStatus = True
                        rate = idx + 1
                        break
                else:
                    if link in linkTag:
                        searchSeccessStatus = True
                        rate = idx + 1
                        break
            
            if searchSeccessStatus == True:
                rateEx.cell(rateExCount,4).value = f"{pageCount} P / {rate}"
                # rateEx.cell(rateExCount,4).value = getHrefonClick
                rateExFile.save('./etc/rate_work.xlsx')
                break


