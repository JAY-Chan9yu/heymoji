<p align="center">
<img src="https://user-images.githubusercontent.com/24591259/210239909-7dab9b9a-f796-4495-a58d-091d25e0dc7c.png"/>
</p>

<img src="https://img.shields.io/badge/coverage-93%25-green"><img src="https://img.shields.io/badge/python-3.10-orange">

# Hey + Emoji = Heymoji

### 개발자의 한마디 👨🏻‍💻

링크드인에서 <a href="https://medium.com/mathpresso/%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94-mathpresso%EC%9D%98-backend-web-%ED%8C%80%EC%97%90%EC%84%9C-backend-engineer%EB%A1%9C-%EC%9D%BC%ED%95%98%EA%B3%A0-%EC%9E%88%EB%8A%94-dan%EC%9E%85%EB%8B%88%EB%8B%A4-c7a0641333e8">
매프 멤버들이 서로 토마토를 주는 이유는?<a/> 라는 글을 읽고, 슬랙 이모지(Emoji)로 멤버들에게 ``칭찬``이나 ``리스펙`` 할 수 있는 문화가 생긴다면 재밌기도 하고 고마움도 표현할 수 있을 것
같았습니다.<br/>

그래서 이런 재미난 기능은 오픈소스로 공개하면 좋을 것 같다고 생각해서 토이 프로젝트로 만들어 보았습니다.<br/>
(근데 Nodejs로 만들어진게 이미 있었네요 <a href="https://github.com/chralp/heyburrito">heyburrito</a>)<br/><br/>
좀 더 `재미난 기능 + 완성도 있는 프로젝트`가 되기위해 유지보수는 지속적으로 할 예정입니다.💪<br/>
FastAPI에 구조나 프로젝트 관련된 추가기능, 개선사항 `PR`은 언제나 환영입니다! <br/>

<br/>

## 👋 개요

<img width="2247" alt="헤이모지" src="https://user-images.githubusercontent.com/24591259/210266806-1782cc63-7303-4f85-804f-f6d6fbe81647.png">

`Heymoji` API서버는 `Python 3.10`, `FastAPI` 로 개발되었습니다.<br/>
그 외 버전에서 패키지 및 동작에 대한 호환은 보장하지 않습니다. (근데 거의 다 될거에요 python3.7 이상이면...아마두~😁 )<br/>
프론트엔드는 `vuejs`를 사용해서 간단히 만들어 봤습니다!

<br/>

## 🛠 프로젝트 구조

처음 `Heymoji`를 개발할때는 DDD 구조가 아니었습니다. <br/>
DDD에 대한 스터디를 위해 구조를 변경했으며 https://github.com/Ermlab/python-ddd 를 참고하였습니다.<br/>
다소 복잡할 수 있으니 추후 유지보수와 여러 상태변경이 일어나는 경우 DDD가 좀 더 유연할 거라고 생각했습니다😁

```
├── apps
|   ├─ api 
|   |  ├── dependancy
|   |  └── router
|   ├─ applications 
|   |  └── services (Application Service)
|   ├─ domains
|   |  └─ user (도메인)
|   |     ├─ entities.py 
|   |     ├─ services.py (Domain Service)
|   |     ├─ repositories.py
|   |     └─ schemas.py	
|   ├─ infrastructure (infra 관련 정의 구조)
|   ├─ utils
|   ├─ tests
|   └─ main.py
├── conf
|   └── settings.py
├── scripts
├── migrations (alembic DB 마이그레이션 설정)
├── seed_work (프로젝트에서 기본적으로 제공해야하는 작업, 코드)
├── alembic.ini
├── requirements.txt
├── docker-compose.yaml
├── Dockerfile
├── web.Dockerfile
├── .env_sample
└── frontend (heymoji 웹페이지 관련 코드)
```

<br/>

## 💾 세팅

`.env_sample`을 참고해서 `.env`파일을 생성합니다.<br/>
원하시는 세팅으로 환경변수들을 세팅합니다.<br/>
DB는 `MySQL`을 사용하며 비동기 처리를 위해 `aiomysql`라이브러리를 함께 사용합니다.<br/>
다른 DB 사용하려면 `config` 설정이 조금 달라질 수 있습니다.

| 이름                                | 설명                                  |
|-----------------------------------|-------------------------------------|
| ENV                               | 배포환경 정의                             |
| ALLOW_ORIGINS                     | CORS를 허용할 ORIGIN 리스트                |
| DB_HOST                           | DB 호스트                              |
| DB_PORT                           | DB 포트                               |
| DATABASE                          | DB 이름                               |
| DB_USERNAME                       | DB 접속 유저네임                          |
| DB_PASSWORD                       | DB 패스워드                             |
| SLACK_TOKEN                       | 슬랙 토큰                               |
| BOT_NAME                          | 슬랙봇 이름                              |
| ERROR_CHANNEL                     | 슬랙 에러 리포팅 채널                        |
| SPECIAL_EMOJI                     | 특별한 의미를 가진 이모지                      |
| LIMIT_GIVE_COUNT_OF_SPECIAL_EMOJI | 하루에 남길수 있는 SPECIAL_EMOJI 최대 개수      |
| ALLOWED_REACTION_LIST             | 웹훅 리액션으로 허용된 이모지(reaction)들을 정의합니다. |
| ALLOWED_EMOJI_TYPES               | 핸들링할 이모지들을 정의합니다.                   |
| RANK_URL                          | 랭킹 웹페이지 URK                         |
| DEFAULT_AVATAR_URL                | 기본 프로필 이미지 URL                      |

<br/>

## 🐳 Docker-Compose 실행

`.env_sample`을 참고하여`.env`파일을 생성한 뒤 `docker-compose up -d` 를 실행합니다.<br/>
api, web, db 컨테이너가 모두 실행 된 후 http://127.0.0.1:8080 에 접속하여 동작을 확인합니다.<br/>
❗️주의: 컨테이너가 뜨고 패키지 설치에 시간이 걸릴수 있어서 애플리케이션 실행까지 몇분이 소요 될 수 있습니다.

<img width="352" alt="스크린샷 2023-01-02 오후 10 54 35" src="https://user-images.githubusercontent.com/24591259/210240727-139572eb-5874-4fb9-8cd5-fdbc4761cea7.png">

`docker-comopse` 실행 전에 README 하단에 있는 <a href="https://github.com/JAY-Chan9yu/heymoji#-slack-bot-%EC%84%A4%EC%A0%95">
Slack Bot 설정</a>을 먼저 보시고 `SlackToken` 같은 환경변수를 먼저 주입해주세요!

<br/>

## 💡 로컬 실행

```
pip install -r requirements
```

`root경로`(/heymoji) 에 가서 <a href="https://www.uvicorn.org/">uvicorn</a>으로 서버를 실행시킵니다.<br/>
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

<br/>

## 📝 API 문서 및 테스트

``HOST_URL/docs``로 접속하면 ``Swagger``로 만들어진 web 페이지를 확인할 수 있습니다. (FastAPI는 swagger, redoc 지원)

<img width="580" alt="API 문서 및 테스트" src="https://user-images.githubusercontent.com/24591259/222969592-d4a57642-62dd-49d6-805f-3c3031b9a46b.png">

<br/>

<br/>

## 👾 슬랙 맨션 명령어

| 이름               | 설명                         |
|------------------|----------------------------|
| help             | 커멘드 관련 help                |
| create_user      | user 생성                    |
| update_user      | user 정보 업데이트               |
| show_user        | 유저 is_display = True (노출)  |
| hide_user        | 유저 is_display = False (숨김) |
| show_best_member | 해당월 베스트 멤버 추출              |

```
🥳 멤버 등록
이름은 필수 입니다!
@EmojiBot --create_user --name=이름 --avatar_url=이미지URL --department=부서

🛠 멤버 정보 업데이트
업데이트할 정보만 적어주세요!
@EmojiBot --update_user --avatar_url=이미지URL

🎖 이번달 베스트 멤버 리스트 추출
@EmojiBot --show_best_member --year=2022 --month=1

🙈 유저 숨기기
@EmojiBot --hide_user --slack_id=슬랙ID

🙉 유저 보이기
@EmojiBot --show_user --slack_id=슬랙ID
```
### 🎖 show_best_member 예시

<img width="499" alt="show_best_member 예시" src="https://user-images.githubusercontent.com/24591259/222969485-290c6d9d-841c-4a01-bd77-12af62db63da.png">

### 🚀 Postman 으로 유저 등록 예시

<img width="712" alt="포스트맨 등록 예시" src="https://user-images.githubusercontent.com/24591259/210569063-1c007cd0-28bd-459f-9694-90f1615f5f1f.png">
<br/>
<br/>

## 🧟‍♂️ 프로세스 Live 체크 (선택)

shell script로 간단하게 Live 체크를 진행 할 수 있습니다! 크론탭에 1분마다 실행하도록 등록.<br/>
로깅도 추가하면 좋습니다.

```
#! /bin/bash
PYTHON_PATH=/{{ path }}/venv/bin/python
SCRIPT_PATH=/{{ path }}/heymoji/app

checker=`ps aux | grep -v "grep" | grep "{{ 검색할 이름}}" | wc -l`

if [ "$checker" == "0" ]; then
	source '{{ path }}/venv/bin/activate'
	cd $SCRIPT_PATH && `uvicorn main:app --port 8080 &`
fi
```
<br/>

# 🤖 Slack Bot 설정

<img src="https://user-images.githubusercontent.com/24591259/114943304-bf743a80-9e80-11eb-85ad-30cb26591ea3.png" width="400px"/>

https://api.slack.com/apps 에 접속하여 create app 버튼을 클릭한 후, <br/>
원하는 ``workspace``에 ``app``을 생성해주세요!

<img src="https://user-images.githubusercontent.com/24591259/114943770-78d31000-9e81-11eb-84fc-3e5964591eed.png" width="400px"/>

`Basic Information` 탭을 클릭후 하단에서 app의 ``프로필 이미지``를 추가하고 Save 해줍니다.<br/>
이건 안해도 되지만 하는게 좋아요. 왜냐하면 멋있거든요😎

<img src="https://user-images.githubusercontent.com/24591259/114944994-84bfd180-9e83-11eb-9ee8-f6c8929dd099.png" width="400px"/>

`Add features and functionality`에서 `Event Subscriptions`을 클릭합니다.

<img src="https://user-images.githubusercontent.com/24591259/114944379-71603680-9e82-11eb-84fc-3f0aacfb1890.png" width="400px"/>

`Event`를 Enable(활성화) 시킨후 `Requst URL`을 넣어서 인증을 합니다. <br/>

<img width="400" alt="스크린샷 2023-01-02 오후 10 12 32" src="https://user-images.githubusercontent.com/24591259/210241355-8add5de3-b9ea-4156-a500-682b04a4040b.png">

위 화면에서 슬랙토큰을 copy하여 ``.env`` 파일에 추가합니다.

<img src="https://user-images.githubusercontent.com/24591259/114944830-45918080-9e83-11eb-9bfa-01c86bd8f9bd.png" width="400px"/>

로컬에서 테스트 하기 위해 <a href="https://dashboard.ngrok.com/get-started/setup">ngrok<a/>을 사용하시면 편합니다.실제 prod
환경에서는 `Nginx + uvicorn`으로 실행하면 되요!
<br/>Nginx Config 에서 `proxy_pass` 만 uvicorn으로 실행한 로컬 서버로 연결해주면 됩니다!<br/>

<img src="https://user-images.githubusercontent.com/24591259/114946460-2811e600-9e86-11eb-8cc5-bbb8bcf7db42.png" width="400px"/>

`Heymoji`는 슬랙 멤버들의 `reaction_added`, `reaction_removed` 이벤트와 bot을 호출하는 `app_mention` 이렇게 3가지 이벤트를 받습니다.

<img src="https://user-images.githubusercontent.com/24591259/153050733-875d2f7a-da23-42b6-a4a2-bbb35e6d2f82.png" width="400px"/>
<img src="https://user-images.githubusercontent.com/24591259/153050405-191203ea-3a0c-450e-bac2-fb66aef7e3ab.png" width="400px"/>

슬랙봇과 DM을 통해 명령어를 실행하기 위해서는 `message.im`을 선택하고 Message Tab 기능을 on 시켜주셔야 합니다.<br/>

마지막으로 `app`을 `workspace`에 설치(install)하면 설정한 이벤트가 일어날때마다 `slack`에서 `Heymoji`서버로 웹훅 api를 호출합니다.
