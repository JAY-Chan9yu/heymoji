## 테스트 코드 작성 주의사항
#### 1. Test Database
Test DB 사용을 위해 `pytest.ini`에서 환경변수 세팅을 해준다.

#### 2. @pytest.mark.asyncio 사용
테스트할때 `event_loop(fixture)`에서 제공하는 `Event Loop`를 사용하기 위해서 필수로 선언해줘야 한다.


#### 3. DB 데이터 삭제
`truncate_tables()` 함수를 사용
```
ex) truncate_tables(["users", "reactions"])
```

