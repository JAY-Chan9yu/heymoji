<p align="center">
<img src="https://user-images.githubusercontent.com/24591259/115119824-565a0780-9fe5-11eb-9d40-e150771b9b8b.png" width="200px"/>
</p>

# 🤩🏆 emoji_rank 🏆👋
### 개발자의 한마디 👨🏻‍💻
링크드인에서 <a href="https://medium.com/mathpresso/%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94-mathpresso%EC%9D%98-backend-web-%ED%8C%80%EC%97%90%EC%84%9C-backend-engineer%EB%A1%9C-%EC%9D%BC%ED%95%98%EA%B3%A0-%EC%9E%88%EB%8A%94-dan%EC%9E%85%EB%8B%88%EB%8B%A4-c7a0641333e8">매프 멤버들이 서로 토마토를 주는 이유는?<a/> 라는 글을 읽고, 슬랙 이모지(Emoji)로 멤버들에게 ``칭찬``이나 ``리스펙`` 할 수 있는 문화가 생긴다면 재밌기도 하고 고마움도 표현할 수 있을 것 같았습니다.<br/><br/>
그래서 이런 재미난 기능은 ``오픈소스``로 공개하면 좋을 것 같다고 생각해서 토이 프로젝트로 만들어 보았습니다.<br/>
(근데 Nodejs로 만들어진게 이미 있었네요 <a href="https://github.com/chralp/heyburrito">heyburrito</a>)<br/><br/>
그래도 만들어 보면 재밌을 것 같아서 ``FastAPI``를 한번 공부해볼 겸 해서 이틀정도 삽질 하면서 만들었습니다.😅 <br/>
(Django에 스며들어 있어서, 생각보다 어려웠네요) <br/><br/>
좀 더 ``재미난 기능 + 완성도 있는 프로젝트``가 되기위해 유지보수는 지속적으로 할 예정입니다.💪<br/>
FastAPI에 구조나 프로젝트 관련된 추가기능, 개선사항 ``PR``은 언제나 환영입니다! <br/>
TMI: 아이콘은 이모지 랭크라서... 갑자기 LoL랭크가 떠올랐고, 제가 골드라서...😂 디자인 잘하시는분...기여 해주십쇼! <br/>
<br/>

# Server 🖥
### 1. 개요 👋
``emoji_rank``는 ``Python 3.7.9``, ``FastAPI`` 로 개발되었습니다.<br/> 
그 외 버전에서 패키지 및 동작에 대한 호환은 보장하지 않습니다. (근데 거의 다 될거에요 python 3 이상이면...아마두~😁 )<br/>


### 2. 패키지 설치 ⚙️
```
pip install -r requirements
```

### 3. 세팅 💾
``.env``파일을 통해 환경변수 등을 세팅 할 수 있습니다.
``.env_sample``을 참고하셔서 원하시는 타입의 이모지등을 세팅해 보세요! 
``settings.py``에서 DB세팅 및 환경변수등을 수정할 수 있습니다<br/>
DB는 ``MySQL``을 사용합니다. 비동기 처리를 위해 ``aiomysql`` 와 함께 사용합니다.<br/>
다른 DB 사용하려면 `config` 설정이 조금 달라질 수 있습니다.

|이름|설명|
|----|----|
|BEST_TYPES|emoji를 가장 많이 받은 멤버를 추출할때 사용합니다.|
|REACTION_LIST|reaction 카운트 허용할 Emoji list|
|DAY_MAX_REACTION|하루 최대 사용할 수 있는 Reacion 개수 (현재 버전에서는 사용하지 않습니다)|
|HOST|DB 호스트|
|PORT|DB 포트|
|DATABASE|DB 이름|
|USERNAME|DB 접속 유저네임
|PASSWORD|DB 패스워드)|


### 4. 실행 💡
main.py가 있는 root경로에 가서 <a href="https://www.uvicorn.org/">uvicorn</a>으로 서버를 실행시킵니다.<br/>
백그라운드로 실행하기 위해서는 `&`를 마지막에 붙여주세요.
```
uvicorn app.main:app --port 8080
```
만약 백그라운드에서 실행되고 있는 프로세스를 제거하고싶은 경우
```
1. ps aux | grep uvicorn
2. kill -9 {PID} 
```
잘못된 프로세스 kill을 주의하세요!<br/>

### 5. 프로세스 Live 체크 🧟‍♂️
shell script로 간단하게 Live 체크를 진행 할 수 있습니다.. 크론탭에 1분마다 실행하도록 등록.<br/>
로깅도 추가하면 좋습니다.
```
#! /bin/bash
PYTHON_PATH=/{{ path }}/venv/bin/python
SCRIPT_PATH=/{{ path }}/emoji_rank/app

checker=`ps aux | grep -v "grep" | grep "{{ 검색할 이름}}" | wc -l`

if [ "$checker" == "0" ]; then
	source '{{ path }}/venv/bin/activate'
	cd $SCRIPT_PATH && `uvicorn main:app --port 8080 &`
fi
```

### 6. API 문서 및 테스트 📝
``HOST_URL/docs``로 접속하면 ``Swagger``로 만들어진 web 페이지를 확인할 수 있습니다. (FastAPI는 swagger, redoc 지원) 
<img src="https://user-images.githubusercontent.com/24591259/115111371-09f9d200-9fbb-11eb-8115-e0ff86d677fd.png" width="400px"/>
<br/>

### 7. 슬랙 커맨드 👾
|이름|설명|
|----|----|
|help|커멘드 관련 help|
|create_user|user 생성|
|update_user|user 정보 업데이트|
|show_user|유저 is_display = True (노출)|
|hide_user|유저 is_display = False (숨김)|
|show_best_member|해당월 베스트 멤버 추출|


```
ex) 실제 사용시 '{{ }}' 는 제거해주세요
@슬랙봇 --create_user --name={{이름}} --slack_id={{슬랙ID}} --avatar_url={{이미지URL}}
```

### 8. 배치 스크립트 크론탭 등록 🏃🏻‍♂️
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

# Slack Bot 🤖
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


# 프론트 예제 📲
![vllo 5](https://user-images.githubusercontent.com/24591259/115112136-0405f000-9fbf-11eb-8fcf-9527d0bc5188.GIF)

간단하게 ``vue``프로젝트에서 `emoji_rank`의 api를 호출해 **User list**를 보여주도록 만들어 봤습니다.<br/>
이모지 추가, 제거 event에 따라 서버에서 count 로직을 처리해주는걸 확인 할 수 있습니다.
<a href="https://github.com/JAY-Chan9yu/emoji_rank_web">Emoji rank web<a/> 프로젝트를 **clone** 해서 확인해보세요😃
