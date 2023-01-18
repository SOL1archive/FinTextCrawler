# KironCrawler

> A Crawler for financial text data

`spider-designation.yaml`만을 설정하여 크롤러의 대부분의 기능을 설정할 수 있는 것을 목표로 함. 객체지향형 DB인터페이스인 `Table`과 `Row` 클래스와 그 파생 클래스들을 활용하여 손쉽게 DB에 데이터를 저장할 수 있음.

`requests`, `bs4` 기반으로 작성됨. 기사 수집 크롤러인 `ArticleScraper`, 트윗 수집 크롤러인 `TwitterScraper`와 커뮤니티 데이터 수집 크롤러인 `CommunityScraper`로 나뉨. 세 크롤러 모두 기본적인 크롤러 구조인 `BasicScraper`의 자식 클래스로, `ArticleScraper`, `TwitterScraper`, `CommunityScraper`는 모두 각 타겟 사이트의 특성에 따라 상속을 통한 세부조정이 가능하도록 설계되었음.

|||
|-|-|
|Version|0.0.2|

||||
|-|-|-:|
|OS Platform|Ubuntu-Linux|20.04 LTS or Later|
|Database|MySQL|8.0.31|
|Python|CPython|3.10.x|

> **주의**: 기본적으로 내장된 mysql 객체지향형 인터페이스는 SQL Injection에 대한 대응이 되어있지 않으므로, 안전한 값들에 대해서만 사용할 것을 권장함.

If there is any Issues or Question, feel free to add issue on this repository or contact to enlightkorean@gmail.com

## How-To-Execute
1. \
    mysql 설치. 계정 및 DB 설정
2. \
    터미널에 `pip install -r requirments.txt` 실행
3. \
    `python3 <적절한 main>.py` 실행

## Requirements
|Libraries or Frameworks|Version|
|-|-:|
|w3lib|2.1.1|
|selenium|4.6.1|
|requests|2.28.1|
|beautifulsoup4|4.11.1|
|MySQLdb|1.4.6|
|PyYAML|5.4.1|

## Contributors
- [Subin Park](https://sol1archive.github.io/)
    - email: enlightkorean@gmail.com
- [Hyunjin Park](https://github.com/HeIIowrld)
    - email: parkhyunjin365@gmail.com
    
