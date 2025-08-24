from func import *

def trfficScript(getDict):


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
            # PC랑 모바일 한번씩 번갈아가면서 돌기!!
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
                        pcUser = getpass.getuser()
                        options = Options()
                        # user_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\default'
                        # options.add_argument(f"user-data-dir={user_data}")
                        # options.add_argument(f'--profile-directory=Profile {profileInfo['pl_number']}')
                        options.add_experimental_option("excludeSwitches", ["enable-automation"])
                        driver = webdriver.Chrome(options=options)
                        driver.get('https://www.naver.com')
                        driver.set_page_load_timeout(12)
                        driver.set_window_size(1300, 800)
                        driver.set_window_position(0,0)
                        break
                    except Exception as e:
                        print(e)
                        print('크롬 창 오픈 실패!!')
                        if driver:
                            driver.quit()
                        pass
                else:
                    try:
                        res = requests.get(f"{siteLink}/api/v7/res_traffic_loop/get_user_agent").json()
                        print(res)
                        print(res['user_agent_info']['ua_content'])
                        if res['status'] == True and res['user_agent_info']['ua_content'] is not None:
                            userAgentInfo = res['user_agent_info']['ua_content']
                            try:
                                pcUser = getpass.getuser()
                                options = Options()
                                # user_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\default'
                                # options.add_argument(f"user-data-dir={user_data}")
                                # options.add_argument(f'--profile-directory=Profile {profileInfo['pl_number']}')

                                options.add_argument(f'user-agent={userAgentInfo}')
                                options.add_experimental_option("excludeSwitches", ["enable-automation"])
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

            try:
                activeArrLengthArr = [6,7]
                activeArrInnerArr = [3,4]
                workArr = create_active_array(activeArrLengthArr, activeArrInnerArr)
            except:
                pg.alert('알수없는 오류!!')
                sys.exit(1)


            if testWork == 'ok':
                workArr = ['notWork','work','realwork','work']
            # 작업할 배열을 생성! workArr 은 'notWork'
            for work in workArr:
                print(f'{work} 작업 돌기!!!!!')
                if work == 'notWork':
                    # notWork 에서는 키워드에서 찾아서 검색하기!!
                    # 먼저 키워드를 불러오자!!!



                    while True:
                        print('not work 불러와야지?!')
                        try:
                            
                            res = requests.get(f"{siteLink}/api/v7/res_traffic_loop/load_notwork").json()
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

                    if workType['pr_work_type'] == 'mobile':
                        searchMobileAnotherList(driver, 1, testWork)
                    else:
                        searchPcAnotherList(driver, 1, testWork)

                elif work == 'work':
                    duplicateErrCount = 0
                    # 먼저 작업 내용 불러오기!! clickStatus 가 false 인거 아무거나 하나 불러오기!!
                    while True:
                        print(workedKeywordArr)
                        wait_float(0.3,0.5)
                        while True:
                            print('work 정보 가지고 오기!!!!')
                            try:
                                res = requests.get(f"{siteLink}/api/v7/res_traffic_loop/load_work?group={workType['pr_group']}").json()
                                if res['status']:
                                    print(res)
                                    workInfo = res['get_work']
                                    break

                            except Exception as e:
                                print(str(e))
                                pass
                            
                        if workInfo['st_subject'] not in workedKeywordArr:
                            break
                        else:
                            while True:
                                wait_float(0.3,0.5)
                                print('중복 있으면')
                                try:
                                    res = requests.post(f"{siteLink}/api/v7/res_traffic_loop/duplicate_work_chk", {'work_id' : workInfo['st_id']}).json()
                                    if res['status']:
                                        break

                                except Exception as e:
                                    print(str(e))
                                    pass


                    # 조회하는 리스트에 추가하기~~
                    while True:
                        try:
                            res = requests.post(f"{siteLink}/api/v7/res_traffic_loop/update_chk_work", {'st_id' : workInfo['st_id']}).json()
                            print(res)
                            if res['status'] == False:
                                continue
                            else:
                                workedKeywordArr.append(workInfo['st_subject'])
                                break
                        except:
                            pass
                    
                    naverMainSearch(driver, workInfo['st_subject'], workType['pr_work_type'])

                    # 먼저 아무거나 클릭 하나!!!
                    if workType['pr_work_type'] == 'mobile':
                        searchMobileAnotherList(driver, 1, testWork)
                    else:
                        searchPcAnotherList(driver, 1, testWork)

                    # 본 조회 작업 GOGO!!!
                    # 아래 함수에서 workInfo['work_type'] 가 click 이면 클릭 / 아니면 조회만 하게 해놨음
                    # 여기는 그냥 조회니까 check로 맞춰주기~
                    workInfo['work_type'] = 'check'
                    if workType['pr_work_type'] == 'mobile':
                        targetWorkStatus = searchMobileContent(driver ,workInfo ,workType ,testWork)
                    else:
                        targetWorkStatus = searchPcContent(driver ,workInfo ,workType ,testWork)

                    
                    while True:
                        wait_float(0.3,0.9)
                        # chkRateStatus 는 st_use가 FALSE 인 값을 찾아서 한것이므로 TRUE로 업데이트!!
                        try:
                            res = requests.post(f"{siteLink}/api/v7/res_traffic_loop/update_traffic_work", {'work_status' : targetWorkStatus, 'st_id' : workInfo['st_id']}).json()
                            if res['status'] == True:
                                break
                        except Exception as e:
                            print(str(e))
                            continue

                elif work =='realwork':
                    realworkErrCount = 0
                    while True:
                        realworkErrCount += 1
                        if realworkErrCount > 10:
                            pg.alert('더이상 할 작업이 없습니다! 종료합니다!')
                            sys.exit(1)
                        try:
                            res = requests.get(f"{siteLink}/api/v7/res_traffic_loop/load_realwork_mix?group={workType['pr_group']}&work_type={workType['pr_work_type']}").json()
                            print('realwork 정보 가지고 오기!!')
                            print(res)
                            if res['status']:
                                workInfo = res['get_realwork']
                                if workInfo['st_subject'] not in workedKeywordArr:
                                    workedKeywordArr.append(workInfo['st_subject'])
                                    break
                                else:
                                    break

                            
                        except Exception as e:
                            print(str(e))
                            pass

                    # 조회하는 리스트에 추가하기~~
                    while True:
                        try:
                            res = requests.post(f"{siteLink}/api/v7/res_traffic_loop/update_chk_realwork", {'st_id' : workInfo['st_id'], 'type' : workType['pr_work_type']}).json()
                            print(res)
                            if res['status']:
                                break
                        except:
                            pass
                    
                    naverMainSearch(driver, workInfo['st_subject'], workType['pr_work_type'])

                    # 모바일은 나중에~~~~ 안할 가능성도 크고~~~~
                    # 먼저 아무거나 클릭 하나!!!
                    if workType['pr_work_type'] == 'mobile':
                        searchMobileAnotherList(driver, 1, testWork)
                    else:
                        searchPcAnotherList(driver, 1, testWork)

                    # 본 조회 작업 GOGO!!!
                    # 아래 함수에서 workInfo['work_type'] 가 click 이면 클릭 / 아니면 조회만 하게 해놨음
                    # 여기는 그냥 클릭이니까 click 으로 맞춰주기~
                    workInfo['work_type'] = 'click'
                    if workType['pr_work_type'] == 'mobile':
                        targetWorkStatus = searchMobileContent(driver ,workInfo ,workType ,testWork)
                    else:
                        targetWorkStatus = searchPcContent(driver ,workInfo ,workType ,testWork)
                    while True:
                        wait_float(0.3,0.9)
                        # chkRateStatus 는 st_use가 FALSE 인 값을 찾아서 한것이므로 TRUE로 업데이트!!
                        try:
                            res = requests.post(f"{siteLink}/api/v7/res_traffic_loop/update_traffic_realwork", {'work_status' : targetWorkStatus, 'st_id' : workInfo['st_id']}).json()
                            if res['status'] == True:
                                break
                        except Exception as e:
                            print(str(e))
                            continue

            # 작업이 끝났으면 마지막 트래픽 에다가 현재 시간 업데이트
            while True:
                wait_float(0.3,0.9)
                try:
                    res = requests.get(f"{siteLink}/api/v7/res_traffic_loop/update_last_traffic?sl_id={pcId}").json()
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
            driver.quit()

            continue
        except Exception as e:
            print(str(e))
            driver.quit()
            




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


