from func import *



def trfficScript(getDict):
    pg.alert('잠깐만?!')

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
                        driver.set_page_load_timeout(15)

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
                                driver.set_page_load_timeout(15)
                                driver.get('https://www.naver.com')
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
                

            
            wait_float(180.0, 200.0)
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

            # 코드 실행 라인
        except Exception as e:
            print(str(e))
            pg.alert('체크점!!')
            pass

    
