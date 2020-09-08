from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import urllib.request
import re
from nltk.tokenize.regexp import regexp_tokenize

cList = open('나라이름.txt', 'r', encoding='UTF8').read().split('\n')

# 토크나이저
def rawToken(raw, rawSet):
    # 특수문자(-제외)를 구분자로
    t1 = regexp_tokenize(raw, "[\w\-']+")
    for i in t1 :
        # 숫자 제외
        t2 = regexp_tokenize(i, "[\D']+")
        if t2 :
            rawSet.add(t2[0])
    return rawSet

# 특수한 경우 처리
def setUpdate(rawSet, remove, add) :
    try:
        rawSet.remove(remove)
        rawSet.add(add)
    except:
        return

#나라, 나라~산 삭제
def deleteToken(raw, rawSet):

    findc=[]
    
    for j in range(len(cList)):
        p = re.compile(
            f'(\({cList[j]}산?\))|' + f'(\({cList[j]}산?/.*?\))|' + f'(\(.*?/{cList[j]}산?\))|' + f'(\(.*?/{cList[j]}산?/.*?\))')
        if cList[j] in raw:
            q = re.sub(p, "", raw)
            findc.append(q)
            raw = q
        else:
            findc.append(0)
            continue
        
    print(findc[-1])
    rawSet.add(findc[-1])        
    return rawSet

# db에서 성분 가져오기
g = open("db_raw.txt","r",encoding='UTF8')
# 중복 제거 위해 set으로
rawSet = set()
cnt = 0
while True:
    wordList = g.readline()
    if not wordList :
        break
    deleteToken(wordList, rawSet)
    rawToken(wordList, rawSet)
    ''' 테스트 범위 설정
    if cnt > 100 :
        break
    cnt = cnt+1
    '''
g.close()

# 특수한 경우 처리
setUpdate(rawSet,'\'-이노신산이나트륨','5\'-이노신산이나트륨')
setUpdate(rawSet,'그린색소PKS-','그린색소PKS-3')
setUpdate(rawSet,'인절미맛시즈닝JM-','인절미맛시즈닝JM-0920')
setUpdate(rawSet,'그식물성분해단백-','식물성분해단백-1')



g = open("원성분.txt","w")
for i in rawSet :
    g.write(i+'\n')
g.close()
