import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
driver.get("https://comic.naver.com/webtoon?tab=tue")

time.sleep(3)

# 화요일 페이지에서 제목, 상세링크, 작가명 가져오기
soup = BeautifulSoup(driver.page_source, 'html.parser')
titles = soup.select(".item .ContentTitle__title--e3qXt")
links = soup.select('.item  a.ContentTitle__title_area--x24vt')
authors = soup.select('.item  .ContentAuthor__author--CTAAP')

title_list = [t.text.strip() for t in titles]
link_list = ['https://comic.naver.com' + l.get('href', '') for l in links]
author_list = [a.text.strip() for a in authors]

driver.quit()

# 상세 페이지
driver = webdriver.Chrome()

summaries = []
images = []
age_ratings = []

for link in link_list:
    try:
        driver.get(link)
        time.sleep(2)  # 로딩 대기
        
        # 연령제한 웹툰 -> 로그인 페이지로 이동됨
        if "nid.naver.com/nidlogin.login" in driver.current_url:
            print(f"성인 웹툰 감지됨: {link}")
            summaries.append("성인")
            images.append("성인")
            age_ratings.append("성인")
            continue

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 줄거리
        summary_tag = soup.select_one('.EpisodeListInfo__summary--Jd1WG')
        summary = summary_tag.text.strip() if summary_tag else "줄거리 없음"
        summaries.append(summary)

        # 이미지
        img_tag = soup.select_one('.Poster__image--d9XTI')
        img_url = img_tag['src'] if img_tag else "이미지 없음"
        images.append(img_url)

        # 연령등급
        try:
            age = soup.select_one("em.ContentMetaInfo__info_item--utGrf  span.ContentMetaInfo__dot--uCVnt").next_sibling.strip()
        except:
            age = "연령 정보 없음"
        age_ratings.append(age)

    # 예외 처리
    except Exception as e:
        print(f"오류 발생: {link} → {e}")
        summaries.append("오류 발생")
        images.append("오류 발생")
        age_ratings.append("오류 발생")

driver.quit()

# 데이터 프레임 생성
webtoon_df = pd.DataFrame({
    '제목': title_list,
    '작가': author_list,
    '링크': link_list,
    '줄거리': summaries,
    '썸네일': images,
    '연령등급': age_ratings
})

# csv 파일로 저장
webtoon_df.to_csv('webtoons_tue.csv', encoding='utf-8-sig', index=False)

# mysql db에 넣기
import pymysql

conn = pymysql.connect(
    host='localhost', user='root', password='1234',  db='my_db',
    charset='utf8'
) 

cursor = conn.cursor()

for row in webtoon_df.itertuples(index=False):
    sql = """
    INSERT INTO webtoons (title, author, link, summary, thumbnail, age_rating)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        row.제목,
        row.작가,
        row.링크,
        row.줄거리,
        row.썸네일,
        row.연령등급
    ))

conn.commit()
cursor.close()
conn.close()