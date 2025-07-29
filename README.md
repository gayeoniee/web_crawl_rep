# web_crawl_rep


# 네이버 웹툰 화요일 작품 정보 크롤링

이 프로젝트는 네이버 웹툰 화요일 탭의 웹툰 목록에서    
각 웹툰의 제목, 작가, 링크, 줄거리, 썸네일 이미지, 연령등급을 크롤링하여 CSV 파일로 저장하고   
이를 MySQL 데이터베이스에 저장하는 파이프라인을 구현한 코드입니다.

## 주요 기능

1. 웹툰 목록 페이지 크롤링
  - URL: https://comic.naver.com/webtoon?tab=tue
  - Selenium으로 웹 페이지에 접근한 후 BeautifulSoup으로 파싱
  - 추출 항목:
    - 제목 (.item .ContentTitle__title--e3qXt)
    - 링크 (.item  a.ContentTitle__title_area--x24vt)
    - 작가명 (.item  .ContentAuthor__author--CTAAP)
   

2. 웹툰 상세 페이지에서 추가 정보 수집
  - 각 웹툰 링크를 하나씩 열어 다음 정보 수집:
    - 줄거리: .EpisodeListInfo__summary--Jd1WG
    - 썸네일 이미지 URL: .Poster__image--d9XTI
    - 연령등급: '15세 이용가', '전체 이용가' 등 텍스트 정보

  - 성인 웹툰인 경우 로그인 페이지(nid.naver.com)로 리디렉션되므로 해당 조건을 감지하여 "성인"으로 처리


3. CSV 파일 저장
  - 최종 수집된 데이터는 pandas의 DataFrame 형태로 저장
  - webtoons_tue.csv 파일로 출력 (utf-8-sig 인코딩)

4. MySQL 데이터베이스에 저장
  - DB 연결 설정:
    - host: localhost
    - user: root
    - password: 1234
    - db: my_db

  - webtoons 테이블에 다음 컬럼 순서로 저장:
    - title, author, link, summary, thumbnail, age_rating
   
## 테이블 구조 예시 (MySQL)

```
CREATE TABLE webtoons (   
    title VARCHAR(100) PRIMARY KEY,   
    author VARCHAR(100),   
    link TEXT,   
    summary TEXT,   
    thumbnail TEXT,   
    age_rating VARCHAR(20)   
);   
```

## 사용 라이브러리
selenium   
beautifulsoup4   
pymysql   
pandas   



