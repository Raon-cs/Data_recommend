def gibon():
    # 최초 기본데이터 제목 및 데이터셋 링크 가지고오기
    # 필요라이브러리 불러오기
    from selenium import webdriver
    import time
    from selenium.webdriver.common.by import By
    import re
    import pandas as pd

    # 크롤링을 위한 driver옵션 설정

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')        # Head-less 설정(웹페이지 창이 별도로 사용자에게 보이지 않기 위해 설정)
    driver = webdriver.Chrome('chromedriver', options=options)

    # AI hub 전체 제목 가져오기
    ti_li_co = []
    num = 0
    # AI hub 검색페이지 접속
    url = "https://aihub.or.kr/aihubdata/data/list.do?currMenu=115&topMenu=100"
    driver.get(url)
    time.sleep(1)
    # 전체 데이터 확인을 위해 더보기 누르기
    for i in range(0,19):
        # 더보기 횟수만큼 숫자 수정 필요
        driver.find_element(By.XPATH, '//*[@id="dataSetMoreBtn"]').click()
        # 더보기 누르는 코드
        time.sleep(2)
        # 바로바로 실행시 오류발생하여 2초간의 휴식시간 지정
    popular_artist = []
    test12 = []
    # 각 제목이 포함된 줄에서 전체 텍스트 가져오기
    for artist in driver.find_elements(By.CLASS_NAME,'dataResultOL'):
        popular_artist.append(artist.text.strip())
    for i in driver.find_elements(By.TAG_NAME,'a'):
        test12.append(i.get_attribute('href'))
    test123 = ''
    for i in test12:
        if 'javascript:fnView' in i:
            test123 += i
    numbers = re.sub(r'[^0-9]', ',', test123)
    num2 = numbers.split(',')
    num1 = []
    for i in num2:
        if '' == i:
            pass
        else:
            num1.append(i)
    data_link = []
    for i in num1:
        data_link.append('https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=' + i)

    # 가져온 전체 텍스트 정리를 위해 별도 리스트로 변경
    list1 = popular_artist
    # 리스트 형식으로 되어있어 문자형태로 가져오기 위해 실행
    st1 = list1[0]
    # 제목 리스트를 '조회수'를 기준으로 분리
    li2 = st1.split('조회수')
    # 첫번째 행의 경우 다른 행들과 다른 형태라 별도로 a1으로 분리 후 '\n'을 기준으로 분리
    a1 = li2[0].split('\n')
    # 첫번째 행 및 마지막 불필요행을 제외하고 새로운 리스트에 저장
    li3 = li2[1:]
    li4 = li3[:-1]

    l3 = []
    # '\n'을 기준으로 분리한 뒤 우리에게 필요한 제목이 해당하는 부분만 빈리스트에 저장
    for i in li4:
        a6 = i.split('\n')
        l3.append(a6[-2])

    # 새로운 빈리스트를 생성하여 처음에 별도로 정리한 첫번째 행 제목을 추가하고 for문을 통해 정리한 전체 제목도 동일하게 저장
    d1 = []
    d1.append(a1[2])
    for i in l3:
        d1.append(i)
    # 중간중간 NEW라는 문구가 들어간 제목의 경우 수정
    for i in range(len(d1)):
        if 'NEW' in d1[i]:
            k1= d1[i][:-3]
            d1[i] = k1
        else:
            pass
        # NEW가 포함된 제목들의 경우 NEW앞에 빈칸(띄어씌기)가 있어서 해당하는 것도 제거하기 위하여 아래 코드 실시
        if d1[i][-1] == ' ':
            d1[i] = d1[i][:-1]
    # 안심존(온라인), 안심존(오프라인)이 존재하는 제목의 경우 해당 제목을 제거하기 위해 for문 실시시
    for i in range(len(d1)):
        if '안심존(온라인)' in d1[i]:
            k1= d1[i][:-9]
            d1[i] = k1
        if '안심존(오프라인)' in d1[i]:
            k1= d1[i][:-10]
            d1[i] = k1
        else:
            pass
        if d1[i][-1] == ' ':
            d1[i] = d1[i][:-1]

    # 공간데이터가 존재하는 제목의 경우 해당 제목을 제거하기 위해 for문 실시
    for i in range(len(d1)):
        if '공간데이터' in d1[i]:
            k1= d1[i][:-6]
            d1[i] = k1
        else:
            pass
        if d1[i][-1] == ' ':
            d1[i] = d1[i][:-1]

    df1 = pd.DataFrame(d1)


    # AI HUB 데이터셋 제목 크롤링
    data = []
    for i in df1[0]:
        data.append(i)

    return data, data_link


def all_career(user_input1):
    # 올인원 패키지
    from selenium import webdriver
    import time
    from selenium.webdriver.common.by import By

    a13 = user_input1

    # 크롤링을 위한 driver옵션 설정

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')        # Head-less 설정(웹페이지 창이 별도로 사용자에게 보이지 않기 위해 설정)
    driver = webdriver.Chrome('chromedriver', options=options)

    # 커리어에 접속하여 사용자가 입력한 회사명으로 검색시 나오는 항목이 있는지 확인
    try:
        url1 = 'https://search.career.co.kr/biz?kw='
        url2 = url1 + a13
        driver.get(url2)
        time.sleep(1)
        a123 = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div').text
        list123 = a123.split('\n')
        num87 = list123.index('주요사업')
        a125 = list123[num87 + 1]
        a126 = a125.split(',')
        list12 = a126[0]
        num12 = 0
    except:
        num12 = 1
        list12 = ''

    return list12, num12

def all_nocareer(user_input2):
    
    # 사용자가 입력한 회사명이 커리어에 미등록 되어있을 경우 추가로 사용자에게 주요 사업관련 내용을 입력받기
    list1 = user_input2.replace('.',',')
    list2 = list1.replace('(',',')
    list3 = list2.replace(')',',')
    if list3[-1] == ',':
        list4 = list3[:-1].split(',')
    else:
        list4 = list3.split(',')
    if len(list4)==1:
        list12 = list4
    else:
        list12 = list4[0]
    # 커리어에서 확인한 주요사업 또는 사용자가 직접 입력한 주요 사업관련 내용을 추후 활용을 위해 별도의 변수명에 저장

    
    return list12

def all_next(list12,data,data_link):
    from sentence_transformers import SentenceTransformer, util
    import numpy as np
    import pandas as pd
    import time
    
    time1 = time.time()
    queries = list12
    # 사용자 입력내용 유사도 측정(ko sroberta multitask 이용)
    embedder = SentenceTransformer("jhgan/ko-sroberta-multitask")
    corpus_embeddings = embedder.encode(data, convert_to_tensor=True)

    # 최적의 유사도를 보이는 제목 몇가지를 찾을지 top_k 변수에 저장
    top_k = 3

    # 제목, 유사도를 기준으로 정리할 딕셔너리 필요수만큼 생성
    dict_list = [{} for i in range(len(queries))]

    # 주요사업내용을 제목들과 유사도 비교후 3가지 선정
    num97 = 0
    top_re = []
    query_embedding = embedder.encode(queries, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    cos_scores = cos_scores.cpu()
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
    top_re.append(top_results)
    # 딕셔너리에 저장
    for i in top_re:
        for idx in i: 
            dict_list[num97][data[idx].strip()] = cos_scores[idx].tolist()
    num97 += 1

    title = []
    score = []
    for i in dict_list[0].keys():
        title.append(i)
    for i in dict_list[0].values():
        score.append(str(int(np.round(i,2)*100)) + '%')
    
    time2 = time.time()
    time3 = time2-time1

    # 선정한 데이터셋 3가지에 대하여 별도의 변수에 저장 및 해당 웹페이지 연결후 필요 내용 크롤링
    total = []
    for i in range(3):
        total.append([title[i],data_link[data.index(title[i])], score[i]])
    
    return total, time3