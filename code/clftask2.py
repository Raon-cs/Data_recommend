def all_next(list12,data,data_link):
    # import numpy as np
    import pandas as pd
    import time
    import rhinoMorph
    import gensim
    from gensim.models import Word2Vec, KeyedVectors

    time1 = time.time()
    # 출력문으로 나올 데이터셋 이름
    dataset_name = data
    # 사용할 사전학습 모델 로드
    model_2 = Word2Vec.load('jhsm_model')
    rn = rhinoMorph.startRhino()
    # 회사 정보 입력
    input_data = list12
    # 회사 정보 출력 데이터셋 형태소 분석
    data1 = rhinoMorph.onlyMorph_list(rn, input_data, pos=['NNG', 'NNP'] , xrVv=True, eomi=True)
    data2 = []
    for i in dataset_name:
        morphed_text = rhinoMorph.onlyMorph_list(rn, i, pos=['NNG', 'NNP'])
        data2.append(morphed_text)
    # 단어 간 유사도 분석 후 문장 간 나누어 이중 리스트로 담기
    simil_list = []
    for i in data2:
        for j in data1:
            my_list = []
            for t in i:
                simil = model_2.wv.similarity(j,t)
                my_list.append(simil)
            simil_list.append(my_list)
    def divide_list(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]
    n = len(data1)
    result = list(divide_list(simil_list, n))
    # 단어 간 최고 유사도 값 뽑은 후 문장 간 평균 내기
    mean_list = []
    for i in range(len(result)):  # 384개
        for j in range(len(data1)):  # input의 형태소 개수
            num = result[i][j]
            similmaxword = max(num)
            mean_list.append(similmaxword)
    sumnum_list = []
    for i in range(0, len(mean_list), len(data1)):
        num = mean_list[i]
        sumnum = sum(mean_list[i:i+3])/len(data1)
        sumnum_list.append(sumnum)
    num_ser = pd.Series(sumnum_list)
    max3_ser = num_ser.nlargest(3)
    max3_idx = max3_ser.index[(max3_ser >= 0)]
    # 연관성 가장 높은 타이틀 제목과 점수 저장
    title = []
    score = []
    for i in range(3):
        nm = dataset_name[max3_idx[i]]
        sc = num_ser[max3_idx[i]]
        title.append(nm)
        score.append(sc)

    time2 = time.time()
    time3 = time2-time1

    # 선정한 데이터셋 3가지에 대하여 별도의 변수에 저장 및 해당 웹페이지 연결후 필요 내용 크롤링
    total = []
    for i in range(3):
        total.append([title[i],data_link[data.index(title[i])], score[i]])
    
    time2 = time.time()
    time3 = time2-time1

    # 선정한 데이터셋 3가지에 대하여 별도의 변수에 저장 및 해당 웹페이지 연결후 필요 내용 크롤링
    total = []
    for i in range(3):
        total.append([title[i],data_link[data.index(title[i])], score[i]])
    
    return total, time3