## 개요

[Django REST framework tutorial](https://www.django-rest-framework.org/tutorial/1-serialization/)을 진행하며 작성한 소스코드이다.

튜토리얼과 더불어 찾아보고 정리한 내용은 [Notion](https://www.notion.so/DRF-tutorial-453cc2ab039e49d8b2150dd112fd8703)에 있다.



## 환경

* python 3.9.7
* Django 4.0.2
* Django REST framework 3.13.1
* mysqlclient 2.1.0
* pygments 2.11.2



## 추가점

튜토리얼에서 제공된 코드에 아래 요소를 추가했다.

* SECRET_KEY를 외부 파일로 분리
* MySQL 연동
* 회원가입 기능 ([블로그](https://velog.io/@azzurri21/DRF-tutorial-%EC%BD%94%EB%93%9C%EC%97%90-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85-%EA%B8%B0%EB%8A%A5-%EC%B6%94%EA%B0%80%ED%95%98%EA%B8%B0))
* Test Code 작성 ([코드](https://github.com/jseop-lim/drf-tutorial/blob/main/snippets/tests.py))
* commit 메시지에 튜토리얼 작업 분류를 포함한 git repository 제작 ([git log](https://github.com/jseop-lim/drf-tutorial/commits/main) / [참고](https://xtring-dev.tistory.com/entry/Git-%EA%B7%9C%EC%B9%99%EC%A0%81%EC%9D%B8-Commit-%EB%A9%94%EC%84%B8%EC%A7%80%EB%A1%9C-%EA%B0%9C%EB%B0%9C%ED%8C%80-%ED%98%91%EC%97%85%ED%95%98%EA%B8%B0-%F0%9F%91%BE))
