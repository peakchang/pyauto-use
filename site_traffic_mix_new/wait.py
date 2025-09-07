def check_file_exists(directory, filename):
    
    # Construct the full file path
    file_path = os.path.join(directory, filename)
    
    # Check if the file exists
    if os.path.isfile(file_path):
        return True
    else:
        return False


def process_array(data, dataStr, type = "free"):

    # 1. 배열을 랜덤하게 섞기
    random.shuffle(data)
    
    # 2. cw_work_count 값에 따라 정렬하기 (작은 순서)
    sorted_data = sorted(data, key=lambda x: x[dataStr])

    if len(sorted_data) == 0:
        return False
    if type == "free":
        maxNum = len(sorted_data)
        ranNum = 0
        if maxNum > 15:
            ranNum = random.randrange(13,16)
        else:
            result = math.ceil(maxNum / 2)
            ranNum = random.randrange(result,maxNum)
        # 3. 상위 15개 항목 추출
        topValue = sorted_data[:ranNum]
    else:
        topValue = sorted_data[0]

    return topValue

def create_ready_array():
    # 랜덤으로 3 또는 4를 선택합니다.
    num = random.choice([3, 4])
    # 'test' 값이 num_tests 개수만큼 들어가는 배열을 생성합니다.
    ready_array = ['notWork'] * num
    return ready_array


def searchCafeContent(driver, workInfo, test = None):

    targetWorkStatus = False

    try:
        print('여기서는 카페 작업!!!')
        scrollRanVal = random.randrange(5, 12)
        errCount = 0
        while True:
            errCount += 1
            wait_float(1.2,1.9)

            try:
                topBtns = driver.find_elements(by=By.CSS_SELECTOR, value=".flick_bx")
                for topBtn in topBtns:
                    if "카페" in topBtn.text:
                        topBtn.click()
                        targetWorkStatus = True
                        break
            except:
                pass


            try:
                moreCafeBtns = driver.find_elements(by=By.CSS_SELECTOR, value=".mod_more_wrap a")
                for moreCafeBtn in moreCafeBtns:
                    if "카페" in moreCafeBtn.text:
                        moreCafeBtn.click()
                        break
            except Exception as e:
                print(str(e))
                print('카페 더보기 클릭 에러!!')
                pass

            try:
                cafeListChk = driver.find_element(By.XPATH, '//*[@id="snb"]/div[1]/div/div[1]/a[1]')
                if "관련도" in cafeListChk.text:
                    break
            except Exception as e:
                print(str(e))
                print('카페 더보기 클릭 후 관련도 못찾는 에러!!')
                if errCount > 4:
                    break
                pass
        
        for i in range(2):
            pg.press('end')
            wait_float(2.1,2.9)
        

        while True:
            try:
                titleList = driver.find_elements(by=By.CSS_SELECTOR, value=".title_link")
                if len(titleList) > 0:
                    break
            except Exception as e:
                print(str(e))
                print('카페 글 리스트 못찾는 에러!!')
                pass

        # 본격적으로 게시물 찾기 없을때를 대비해 noSearchCount / noSearchStatus 준비
        noSearchCount = 0
        noSearchStatus = False

        oddCount = 0
        while True:
            oddCount += 1
            noSearchCount += 1
            if noSearchCount > 5:
                noSearchStatus = True
                return 'noSearch'
            searchSuccess = False
            try:
                for title in titleList:
                    print(f"찾을 링크 : {workInfo['st_link']} / 찾은 링크 : {title.get_attribute('href')}")
                    if workInfo['st_link'] in title.get_attribute('href'):
                        title.click()
                        searchSuccess = True
                        wait_float(1.2,1.9)
                        break
            except:
                pg.moveTo(300,400)
                print('링크 클릭 안됨! 스크롤 올리기!')
                if oddCount % 2 == 0:
                    pg.scroll(200)
                else:
                    pg.scroll(-200)
            if searchSuccess == True:
                break
        if noSearchStatus == False:
            # noSearchStatus 가 False로 정상 작업 GOGO!!

            for k in range(scrollRanVal):
                pg.moveTo(300,400)
                pg.scroll(-150)
                if test == 'ok':
                    wait_float(0.1,0.4)
                else:
                    wait_float(2.5,3.5)

            if workInfo['st_addlink']:

                aTagClickSuccess = False
                oddCount = 0
                while True:
                    oddCount += 1
                    aTagList = driver.find_elements(by=By.CSS_SELECTOR, value="a")

                    try:
                        for aTag in aTagList:
                            print(aTag)
                            print(aTag.get_attribute('href'))
                            if aTag.get_attribute('href') is not None:
                                if workInfo['st_addlink'] in aTag.get_attribute('href'):
                                    aTag.click()
                                    aTagClickSuccess = True
                                    wait_float(1.2,1.9)
                                    break
                    except:
                        print('링크 클릭 안됨! 스크롤 올리기!')
                        if oddCount % 2 == 0:
                            pg.scroll(200)
                        else:
                            pg.scroll(-200)

                    try:
                        closeBtn = driver.find_element(by=By.CSS_SELECTOR, value=".btns .ButtonBase--gray")
                        closeBtn.click()
                    except:
                        pass

                    if aTagClickSuccess == True:
                        break

                driver.switch_to.window(driver.window_handles[1])
                for k in range(scrollRanVal):
                    pg.moveTo(300,400)
                    pg.scroll(-150)
                    if test == 'ok':
                        wait_float(0.1,0.4)
                    else:
                        wait_float(2.5,3.5)

        targetWorkStatus = True

    except Exception as e:
        print(e)
        targetWorkStatus = False
    
    return targetWorkStatus