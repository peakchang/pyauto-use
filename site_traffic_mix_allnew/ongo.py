from func import *



def trfficScript(getDict):
    testWork = 'ok'
    workType = {}
    # testWork = None
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

    workType['pr_work_type'] = ''
    workInfo = {} # 1회 돌아갈때 작업 할 정보 담는 객체
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
                        options.add_experimental_option("excludeSwitches", ["enable-automation"])
                        driver = webdriver.Chrome(options=options)
                        driver.set_page_load_timeout(15)

                        driver.get('https://www.naver.com')
                        
                        driver.set_window_size(1300, 800)
                        driver.set_window_position(0,0)
                        
                        break
                    except Exception as e:
                        print(e)
                        print('크롬 창 오픈 실패!!')
                        driver.quit()
                        pass
                else:
                    try:
                        res = requests.get(f"{siteLink}/api/v7/res_traffic_work/get_user_agent").json()
                        print(res['user_agent_info']['ua_content'])
                        if res['status'] == True and res['user_agent_info']['ua_content'] is not None:
                            userAgentInfo = res['user_agent_info']['ua_content']
                            try:
                                user_data_dir = tempfile.mkdtemp(prefix="selenium_profile_")
                                options = Options()
                                options.add_argument(f"--user-data-dir={user_data_dir}")  # 프로필 분리(누수 ↓)
                                service = Service()  # chromedriver PATH 잡혀있다고 가정
                                options.add_argument(f'user-agent={userAgentInfo}')

                                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                                options.add_experimental_option("useAutomationExtension", False)
                                driver = webdriver.Chrome(options=options)
                                driver.set_page_load_timeout(15)
                                driver.get('https://www.naver.com')
                                driver.set_window_size(1000, 800)
                                driver.set_window_position(0,0)
                                break
                            except Exception as e:
                                print(e)
                                print('크롬 창 오픈 실패!!')
                                driver.quit()
                                pass

                    except Exception as e:
                        print(str(e))
                        print('프로필 정보 불러오기 오류!!')
                        continue

            
            # >>>>>>>>>>>>>>> 작업 라인 START!!!!!!

            # while True:
            #     x, y = pg.position()  # 현재 마우스 좌표 (x, y)
            #     print(f"X: {x}, Y: {y}", end="\r")  # 같은 줄에서 갱신 출력
            #     time.sleep(0.1)  # 0.1초마다 갱신

            activeArrLengthArr = [6,7]
            activeArrInnerArr = [3,4]
            workArr = create_active_array(activeArrLengthArr, activeArrInnerArr)
            print(workArr)


            # not work 불러오기!!!!
            while True:
                print('not work 불러와야지?!')
                try:
                    res = requests.get(f"{siteLink}/api/v7/res_traffic_work/load_notwork").json()
                    print('now work 정보!')
                    print(res)
                    if res['status'] == False:
                        continue

                    if res['status'] == True:
                        workInfo = res['get_keyword']
                        break
                    else:
                        continue
                except Exception as e:
                    print(str(e))
                    pass

            # 시작!!! 네이버 검색!!
            while True:
                print('네이버 검색 시작!')
                while True:
                    wait_float_timer(0,1)
                    pg.moveTo(160,160)
                    pg.leftClick()
                    print('검색 start!!')
                    focusChk = focus_window_and_tab(driver, ['NAVER'])
                    if focusChk:
                        break
                    else:
                        wait_float(1.2,1.9)
                        pg.press('F5')
                        

                try:
                    wait_float(0.5,0.8)
                    mainSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#MM_SEARCH_FAKE")
                    mainSearchTab.click()
                except Exception as e:
                    # print(str(e))
                    pass

                try:
                    wait_float(0.5,0.8)
                    subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#query")
                    subSearchTab.click()
                except Exception as e:
                    # print(str(e))
                    pass

                try:
                    wait_float(0.5,0.8)
                    subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#nx_query")
                    subSearchTab.click()
                except Exception as e:
                    # print(str(e))
                    pass

                try:
                    wait_float(1.2,1.9)
                    pg.hotkey('ctrl', 'a')
                    pg.press('delete')
                    wait_float(1.2,1.9)
                    cb.copy(workInfo['pk_content'])
                    pg.hotkey('ctrl', 'v')
                    wait_float(1.2,1.9)
                except:
                    pass

                print('검색 붙여넣기 완료~')

                # 검색 완료 엔터!!!
                try:
                    subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#query")
                    searchVal = subSearchTab.get_attribute('value')
                    if searchVal is not None and searchVal == workInfo['pk_content']:
                        pg.press('enter')
                except Exception as e:
                    # print(str(e))
                    pass

                try:
                    subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#nx_query")
                    searchVal = subSearchTab.get_attribute('value')
                    if searchVal is not None and searchVal == workInfo['pk_content']:
                        pg.press('enter')
                except Exception as e:
                    # print(str(e))
                    pass

                print('검색 엔터 완료!!')

                for i in range(7):
                    wait_float_timer(1,2)
                    print('검색 확인 START!!!')
                    focusChk = focus_window_and_tab(driver, [workInfo['pk_content'], '네이버', '검색'])
                    if focusChk:
                        break
                if focusChk:
                    break
                else:
                    pg.press('F5')

                    
            print('검색 완료 체크!!!')

            if workType['pr_work_type'] == 'pc':
                # PC 버전으로 작업시!!
                while True:
                    try:
                        sections = driver.find_elements(by=By.CSS_SELECTOR, value=".api_subject_bx")
                        if len(sections) > 0:
                            break
                    except:
                        pass

                onotherList = []  # [(text, WebElement), ...] 형태로 저장
                for sec in sections:
                    # 1) 섹션 안에 fds-web-root 가 있으면 제외 (웹문서 영역)
                    if sec.find_elements(By.CSS_SELECTOR, ".fds-web-root"):
                        continue

                    # 2) 없으면 타이틀 후보들 수집
                    elems = sec.find_elements(
                        By.CSS_SELECTOR,
                        ".fds-comps-right-image-text-title, .sds-comps-text-type-headline1"
                    )


                    keywords = ["더보기", "찾는", "콘텐츠", "인기글", "지식", "동영상"]
                    for el in elems:
                        addStatus = True
                        for keyword in keywords:
                            if keyword in el.text:
                                addStatus = False
                            
                        if addStatus == True:
                            onotherList.append(el)

                for data in onotherList:
                    print(data.text)

                pg.alert('PC 버전 잠깐만?!')

            else:
                # 모바일 버전으로 작업시!!

                while True:
                    try:
                        sections = driver.find_elements(by=By.CSS_SELECTOR, value=".fds-default-mode")
                        if len(sections) > 0:
                            break
                    except:
                        pass
                    
                onotherList = []  # [(text, WebElement), ...] 형태로 저장
                for sec in sections:
                    # 1) 섹션 안에 fds-web-root 가 있으면 제외
                    if sec.find_elements(By.CSS_SELECTOR, ".fds-web-root"):
                        continue

                    # 2) 없으면 타이틀 후보들 수집
                    elems = sec.find_elements(
                        By.CSS_SELECTOR,
                        ".fds-comps-right-image-text-title, .sds-comps-text-type-headline1"
                    )


                    keywords = ["더보기", "찾는", "콘텐츠", "인기글", "지식", "동영상"]
                    for el in elems:
                        addStatus = True
                        for keyword in keywords:
                            if keyword in el.text:
                                addStatus = False
                            
                        if addStatus == True:
                            onotherList.append(el)
                for data in onotherList:
                    print(data.text)

                workOnotherVal = random.randrange(0, len(onotherList) - 1)
                forClickEle = onotherList.pop(workOnotherVal)
                driver.set_page_load_timeout(15)
                forClickEle.click()
                pg.alert('모바일 버전 잠깐만?!')

                
                

            wait_float_timer(30,33)


            # 작업이 끝났으면 마지막 트래픽 에다가 현재 시간 업데이트
            max_retries = 30  # 최대 재시도 횟수 설정
            retry_count = 0

            while retry_count < max_retries:
                print(f'작업 끝 마지막 작업 시간 업데이트! (시도 {retry_count + 1}/{max_retries})')
                wait_float_timer(0, 1)
                
                try:
                    # timeout 설정 추가 (5초)
                    print('마지막 작업 시간 저장!!')
                    res = requests.get(
                        f"{siteLink}/api/v7/res_traffic_work/update_last_traffic?sl_id={pcId}",
                        timeout=5  # 5초 타임아웃
                    ).json()

                    print(res)
                    
                    if res.get('status') == True:  # res['status'] 대신 res.get('status') 사용
                        print('[SUCCESS] 마지막 작업 시간 업데이트 완료!')
                        break
                    else:
                        print(f'[WARNING] API 응답: {res}')
                        retry_count += 1
                        
                except requests.exceptions.Timeout:
                    print(f'[ERROR] 타임아웃 발생 (5초 초과)')
                    retry_count += 1
                    
                except requests.exceptions.ConnectionError:
                    print(f'[ERROR] 네트워크 연결 오류')
                    retry_count += 1
                    
                except requests.exceptions.RequestException as e:
                    print(f'[ERROR] 요청 오류: {str(e)}')
                    retry_count += 1
                    
                except Exception as e:
                    print(f'[ERROR] 예상치 못한 오류: {str(e)}')
                    retry_count += 1
                    
                # 재시도 간격 (점진적으로 증가)
                if retry_count < max_retries:
                    wait_time = min(retry_count * 2, 10)  # 최대 10초
                    print(f'[INFO] {wait_time}초 후 재시도...')
                    time.sleep(wait_time)

            # 최대 재시도 초과 시
            if retry_count >= max_retries:
                print(f'[CRITICAL] 최대 재시도 횟수({max_retries})를 초과했습니다!')
                # 여기서 알림을 보내거나, 로그를 남기거나, 프로그램을 종료할 수 있습니다.

            # 시간 기록
            end_time = time.time()
            end_time_str = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
            elapsed_time = end_time - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)

            try:
                with open('./work_time.txt', 'a', encoding='utf-8') as file:
                    file.write(f"종료시간 : {end_time_str} / 프로그램 실행 시간: {minutes}분 {seconds}초\n")
                print(f'[INFO] 작업 시간 기록 완료: {minutes}분 {seconds}초')
            except Exception as e:
                print(f'[ERROR] 파일 저장 실패: {str(e)}')

            close_driver(driver, service, user_data_dir)

            # 코드 실행 라인
        except Exception as e:
            print(str(e))
            if driver:
                driver.quit()
            pass