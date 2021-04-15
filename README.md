# emoji_rank
### 개발자의 한마디 👨🏻‍💻
링크드인에서 <a href="https://medium.com/mathpresso/%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94-mathpresso%EC%9D%98-backend-web-%ED%8C%80%EC%97%90%EC%84%9C-backend-engineer%EB%A1%9C-%EC%9D%BC%ED%95%98%EA%B3%A0-%EC%9E%88%EB%8A%94-dan%EC%9E%85%EB%8B%88%EB%8B%A4-c7a0641333e8">매프 멤버들이 서로 토마토를 주는 이유는?<a/> 라는 글을 읽고, 슬랙 이모지(Emoji)로 멤버들에게 ``칭찬``이나 ``리스펙`` 할 수 있는 문화가 생긴다면 재밌기도 하고 고마움도 표현할 수 있을 것 같았습니다.<br/>
그래서 이런 재미난 기능은 ``오픈소스``로 공개하면 좋을 것 같기도 했고, 개인적으로 ``FastAPI``를 한번 공부해볼 겸 해서 하루동안 삽질 하면서 만들어 봤습니다.😅 
좀 더 ``재미난 기능 + 완성도 있는 프로젝트``가 되기위해 유지보수는 지속적으로 할 예정입니다.💪<br/>
FastAPI에 구조나 프로젝트 관련된 추가기능, 개선사항 ``PR``은 언제나 환영입니다! 
<br/>

## Server 구성
### 1. 개요 👋
``emoji_rank``는 ``Python 3.7.9``, ``FastAPI`` 로 개발되었습니다.<br/> 
그 외 버전에서 패키지 및 동작에 대한 호환은 보장하지 않습니다. (근데 거의 다 될거에요 python 3 이상이면...아마두~😁 )


### 2. 패키지 설치 ⚙️
```
pip install -r requirements
```

### 3. DB 세팅 🗂
DB는 ``MySQL``을 사용합니다. 다른 DB 사용하려면 config 설정이 조금 달라질 수 있습니다.
`conf/database.py`, `scripts/update` 에서 HOST, PORT, DATABASE, USER, PASSWORD 로컬 환경에 맞게 변경합니다.

### 4. 실행 💡
main.py가 있는 root경로에 가서 <a href="https://www.uvicorn.org/">uvicorn</a>으로 서버를 실행시킵니다.
```
uvicorn main:app --port 8080
```

### 5. 배치 스크립트 크론탭 등록 🏃🏻‍♂️
멤버당 하루에 5개씩 지정한 Emoji를 다른 멤버에게 줄 수 있도록 했습니다.<br/>
매일 자정에 다시 5개로 리셋하는 배치 스크립트를 ``크론탭``에 등록합니다.<br/>
저는 ``쉘스크립트``를 만들어서 ``크론탭``에 등록했습니다.
```
#!/bin/bash

PYTHON_PATH=/{{ path }}/venv/bin/python
SCRIPT_PATH=/{{ path }}/emoji_rank/scripts/update_emoji_count.py

source '{{ path }}/venv/bin/activate'

$PYTHON_PATH $SCRIPT_PATH
```
<br/>

❤️ 가 아닌 다른 ``Emoji``를 사용하려면 ``services.py``의 ``REACTION = 'heart'``를 변경하세요!

## Slack Bot 설정 🤖
<img src="https://user-images.githubusercontent.com/24591259/114943304-bf743a80-9e80-11eb-85ad-30cb26591ea3.png" width="400px"/>

https://api.slack.com/apps에 접속하여 create app 버튼을 클릭한 후, <br/>
원하는 ``workspace``에 ``app``을 생성해주세요!


<img src="https://user-images.githubusercontent.com/24591259/114943770-78d31000-9e81-11eb-84fc-3e5964591eed.png" width="400px"/>

`Basic Information` 탭을 클릭후 하단에서 app의 ``프로필 이미지``를 추가하고 Save 해줍니다.<br/>
이건 안해도 되지만 하는게 좋아요. 왜냐하면 멋있거든요😎 

<img src="https://user-images.githubusercontent.com/24591259/114944994-84bfd180-9e83-11eb-9ee8-f6c8929dd099.png" width="400px"/>

`Add features and functionality`에서 'Event Subscriptions'을 클릭합니다.

<img src="https://user-images.githubusercontent.com/24591259/114944379-71603680-9e82-11eb-84fc-3f0aacfb1890.png" width="400px"/>

``Event``를 Enable(활성화) 시킨후 ``Requst URL``을 넣어서 인증을 합니다. <br/>
로컬에서 테스트 하기 위해 <a href="https://dashboard.ngrok.com/get-started/setup">ngrok<a/>을 사용하시면 편합니다.실제 prod 환경에서는 `Nginx + uvicorn`으로 실행하면 되요! 
<br/>Nginx Config 에서 `proxy_pass` 만 uvicorn으로 실행한 로컬 서버로 연결해주면 됩니다!<br/>

<img src="https://user-images.githubusercontent.com/24591259/114944830-45918080-9e83-11eb-9bfa-01c86bd8f9bd.png" width="400px"/>

`ngrok`을 통해 외부망에서 로컬로 연결이 된 모습

<img src="https://user-images.githubusercontent.com/24591259/114946460-2811e600-9e86-11eb-8cc5-bbb8bcf7db42.png" width="400px"/>

`emoji_rank`는 슬랙 멤버들의 `reaction_added`, `reaction_removed` 이벤트와 bot을 호출하는 `app_mention` 이렇게 3가지 이벤트를 받습니다.
<br/> 마지막으로 app을 workspace에 **install** 하면 설정한 이벤트가 일어날때마다 `slack` 서버에서 `emoji_rank`서버로 api를 호출합니다.(WebHook)


## 프론트 예제 📲
![vllo](https://user-images.githubusercontent.com/24591259/114949520-29461180-9e8c-11eb-9639-1f79e4dea4a3.GIF)

간단하게 ``vue``프로젝트에서 `emoji_rank`의 api를 호출해 **User list**를 보여주도록 만들어 봤습니다.<br/>
이모지 추가, 제거 event에 따라 서버에서 count 로직을 처리해주는걸 확인 할 수 있습니다.
<a href="https://github.com/JAY-Chan9yu/emoji_rank_web">Emoji rank web<a/> 프로젝트를 **clone** 해서 확인해보세요😃



