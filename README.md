<p align="center">
<img src="https://user-images.githubusercontent.com/24591259/155010131-b34115a5-d393-4791-ab97-763d6eeb903d.png"/>
</p>

# π€© Hey + Emoji = Heymoji π
### κ°λ°μμ νλ§λ π¨π»βπ»
λ§ν¬λμΈμμ <a href="https://medium.com/mathpresso/%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94-mathpresso%EC%9D%98-backend-web-%ED%8C%80%EC%97%90%EC%84%9C-backend-engineer%EB%A1%9C-%EC%9D%BC%ED%95%98%EA%B3%A0-%EC%9E%88%EB%8A%94-dan%EC%9E%85%EB%8B%88%EB%8B%A4-c7a0641333e8">λ§€ν λ©€λ²λ€μ΄ μλ‘ ν λ§ν λ₯Ό μ£Όλ μ΄μ λ?<a/> λΌλ κΈμ μ½κ³ , μ¬λ μ΄λͺ¨μ§(Emoji)λ‘ λ©€λ²λ€μκ² ``μΉ­μ°¬``μ΄λ ``λ¦¬μ€ν`` ν  μ μλ λ¬Ένκ° μκΈ΄λ€λ©΄ μ¬λ°κΈ°λ νκ³  κ³ λ§μλ ννν  μ μμ κ² κ°μμ΅λλ€.<br/>

κ·Έλμ μ΄λ° μ¬λ―Έλ κΈ°λ₯μ ``μ€νμμ€``λ‘ κ³΅κ°νλ©΄ μ’μ κ² κ°λ€κ³  μκ°ν΄μ ν μ΄ νλ‘μ νΈλ‘ λ§λ€μ΄ λ³΄μμ΅λλ€.<br/>
(κ·Όλ° Nodejsλ‘ λ§λ€μ΄μ§κ² μ΄λ―Έ μμλ€μ <a href="https://github.com/chralp/heyburrito">heyburrito</a>)<br/><br/>
μ’ λ ``μ¬λ―Έλ κΈ°λ₯ + μμ±λ μλ νλ‘μ νΈ``κ° λκΈ°μν΄ μ μ§λ³΄μλ μ§μμ μΌλ‘ ν  μμ μλλ€.πͺ<br/>
FastAPIμ κ΅¬μ‘°λ νλ‘μ νΈ κ΄λ ¨λ μΆκ°κΈ°λ₯, κ°μ μ¬ν­ ``PR``μ μΈμ λ νμμλλ€! <br/>

π TMI: <br/> 
μμ΄μ½μ μ΄λ¦ κ·Έλλ‘ `λ­ν¬`μμ μκ° `LoLλ­ν¬`κ° λ μ¬λκ³ , μ κ° κ³¨λλΌμ...π<br/>
λμμΈ μνμλλΆ κΈ°μ¬ν΄ μ£ΌμΈμ!γγ <br/><br/>


# Server π₯
## π  κ°μ 
``Heymoji``λ ``Python 3.7.9``, ``FastAPI`` λ‘ κ°λ°λμμ΅λλ€.<br/> 
κ·Έ μΈ λ²μ μμ ν¨ν€μ§ λ° λμμ λν νΈνμ λ³΄μ₯νμ§ μμ΅λλ€. (κ·Όλ° κ±°μ λ€ λ κ±°μμ python 3 μ΄μμ΄λ©΄...μλ§λ~π )<br/>

## π   νλ‘μ νΈ κ΅¬μ‘°
μ²μ Heymojiλ₯Ό κ°λ°ν λλ DDD κ΅¬μ‘°κ° μλμμ΅λλ€. <br/> 
DDDμ λν μ€ν°λλ₯Ό μν΄ κ΅¬μ‘°λ₯Ό λ³κ²½νμΌλ©° https://github.com/Ermlab/python-ddd λ₯Ό μ°Έκ³ νμμ΅λλ€.<br/> 
λ€μ λ³΅μ‘ν  μ μμΌλ μΆν μ μ§λ³΄μμ μ¬λ¬ μνλ³κ²½μ΄ μΌμ΄λλ κ²½μ° DDDκ° μ’ λ μ μ°ν  κ±°λΌκ³  μκ°νμ΅λλ€π
```
βββ apps
|   ββ api 
|   |  βββ dependancy
|   |  βββ router
|   ββ applications 
|   |  βββ services (Application Service)
|   ββ domains
|   |  ββ user (λλ©μΈ)
|   |     ββ entities.py 
|   |     ββ services.py (Domain Service)
|   |     ββ repositories.py
|   |     ββ schemas.py	
|   ββ infrastructure (infra κ΄λ ¨ μ μ κ΅¬μ‘°)
|   ββ utils
|   ββ tests
|   ββ main.py
βββ conf
|   βββ settings.py
βββ scripts
βββ seed_work (νλ‘μ νΈμμ κΈ°λ³Έμ μΌλ‘ μ κ³΅ν΄μΌνλ μμ, μ½λ)
```

## βοΈ ν¨ν€μ§ μ€μΉ
```
pip install -r requirements
```

## πΎ  μΈν
``.env``νμΌμ ν΅ν΄ νκ²½λ³μ λ±μ μΈν ν  μ μμ΅λλ€.
``.env_sample``μ μ°Έκ³ νμμ μνμλ νμμ μ΄λͺ¨μ§λ±μ μΈνν΄ λ³΄μΈμ!
DBλ ``MySQL``μ μ¬μ©ν©λλ€. λΉλκΈ° μ²λ¦¬λ₯Ό μν΄ ``aiomysql`` μ ν¨κ» μ¬μ©ν©λλ€.<br/>
λ€λ₯Έ DB μ¬μ©νλ €λ©΄ `config` μ€μ μ΄ μ‘°κΈ λ¬λΌμ§ μ μμ΅λλ€.

|μ΄λ¦|μ€λͺ|
|----|----|
|ENV|λ°°ν¬νκ²½ μ μ|
|ALLOWED_EMOJI_TYPES|μ΄λͺ¨μ§ νμλ€μ μ μν©λλ€.|
|REACTION_LIST|μΉν λ¦¬μ‘μμΌλ‘ νμ©λ μ΄λͺ¨μ§(reaction)λ€μ μ μν©λλ€.|
|DAY_MAX_REACTION|νλ£¨ μ΅λ μ¬μ©ν  μ μλ Reaction κ°μ (μ νμμ μλλ€.)|
|SLACK_TOKEN|μ¬λ ν ν°|
|BOT_NAME|μ¬λλ΄ μ΄λ¦|
|ERROR_CHANNEL|μ¬λ μλ¬ λ¦¬ν¬ν μ±λ|
|HOST|DB νΈμ€νΈ|
|PORT|DB ν¬νΈ|
|DATABASE|DB μ΄λ¦|
|USERNAME|DB μ μ μ μ λ€μ
|PASSWORD|DB ν¨μ€μλ)|


## π‘  μ€ν 
`rootκ²½λ‘`(/emoji_rank) μ κ°μ <a href="https://www.uvicorn.org/">uvicorn</a>μΌλ‘ μλ²λ₯Ό μ€νμν΅λλ€.<br/>
λ°±κ·ΈλΌμ΄λλ‘ μ€ννκΈ° μν΄μλ `&`λ₯Ό λ§μ§λ§μ λΆμ¬μ£ΌμΈμ.
```
uvicorn app.main:app --port 8080
```
λ§μ½ λ°±κ·ΈλΌμ΄λμμ μ€νλκ³  μλ νλ‘μΈμ€λ₯Ό μ κ±°νκ³ μΆμ κ²½μ°
```
1. ps aux | grep uvicorn
2. kill -9 {PID} 
```
μλͺ»λ νλ‘μΈμ€ killμ μ£ΌμνμΈμ!<br/>

## π  API λ¬Έμ λ° νμ€νΈ
``HOST_URL/docs``λ‘ μ μνλ©΄ ``Swagger``λ‘ λ§λ€μ΄μ§ web νμ΄μ§λ₯Ό νμΈν  μ μμ΅λλ€. (FastAPIλ swagger, redoc μ§μ) 
<img src="https://user-images.githubusercontent.com/24591259/115111371-09f9d200-9fbb-11eb-8115-e0ff86d677fd.png" width="400px"/>
<br/>

## πΎ  μ¬λ λ§¨μ λͺλ Ήμ΄
|μ΄λ¦|μ€λͺ|
|----|----|
|help|μ»€λ©λ κ΄λ ¨ help|
|create_user|user μμ±|
|update_user|user μ λ³΄ μλ°μ΄νΈ|
|show_user|μ μ  is_display = True (λΈμΆ)|
|hide_user|μ μ  is_display = False (μ¨κΉ)|
|show_best_member|ν΄λΉμ λ² μ€νΈ λ©€λ² μΆμΆ|


```
ex) μ€μ  μ¬μ©μ '{{ }}' λ μ κ±°ν΄μ£ΌμΈμ
@μ¬λλ΄ --create_user --name={{μ΄λ¦}} --avatar_url={{μ΄λ―Έμ§URL}}
```

## π§ββοΈ  νλ‘μΈμ€ Live μ²΄ν¬ (μ ν)
shell scriptλ‘ κ°λ¨νκ² Live μ²΄ν¬λ₯Ό μ§ν ν  μ μμ΅λλ€! ν¬λ‘ ν­μ 1λΆλ§λ€ μ€ννλλ‘ λ±λ‘.<br/>
λ‘κΉλ μΆκ°νλ©΄ μ’μ΅λλ€.
```
#! /bin/bash
PYTHON_PATH=/{{ path }}/venv/bin/python
SCRIPT_PATH=/{{ path }}/emoji_rank/app

checker=`ps aux | grep -v "grep" | grep "{{ κ²μν  μ΄λ¦}}" | wc -l`

if [ "$checker" == "0" ]; then
	source '{{ path }}/venv/bin/activate'
	cd $SCRIPT_PATH && `uvicorn main:app --port 8080 &`
fi
```

## ππ»β λ°°μΉ μ€ν¬λ¦½νΈ ν¬λ‘ ν­ λ±λ‘ (μ ν)
λ©€λ²λΉ νλ£¨μ νμ©λ ``DAY_MAX_REACTION`` λ§νΌ μ΄λͺ¨μ§(Emoji)λ₯Ό λ€λ₯Έ λ©€λ²μκ² μ€ μ μλλ‘ νμ΅λλ€.<br/>
λ§€μΌ μμ μ λ€μ ``DAY_MAX_REACTION``λ§νΌ μΉ΄μ΄νΈλ₯Ό λ¦¬μνλ λ°°μΉ μ€ν¬λ¦½νΈλ₯Ό ``ν¬λ‘ ν­``μ λ±λ‘ν©λλ€.<br/>
μ λ ``μμ€ν¬λ¦½νΈ``λ₯Ό λ§λ€μ΄μ ``ν¬λ‘ ν­``μ λ±λ‘νμ΅λλ€.
```
#!/bin/bash

PYTHON_PATH=/{{ path }}/venv/bin/python
SCRIPT_PATH=/{{ path }}/emoji_rank/scripts/update_emoji_count.py

source '{{ path }}/venv/bin/activate'

$PYTHON_PATH $SCRIPT_PATH
```
<br/>

# π€ Slack Bot μ€μ  
<img src="https://user-images.githubusercontent.com/24591259/114943304-bf743a80-9e80-11eb-85ad-30cb26591ea3.png" width="400px"/>

https://api.slack.com/apps μ μ μνμ¬ create app λ²νΌμ ν΄λ¦­ν ν, <br/>
μνλ ``workspace``μ ``app``μ μμ±ν΄μ£ΌμΈμ!


<img src="https://user-images.githubusercontent.com/24591259/114943770-78d31000-9e81-11eb-84fc-3e5964591eed.png" width="400px"/>

`Basic Information` ν­μ ν΄λ¦­ν νλ¨μμ appμ ``νλ‘ν μ΄λ―Έμ§``λ₯Ό μΆκ°νκ³  Save ν΄μ€λλ€.<br/>
μ΄κ±΄ μν΄λ λμ§λ§ νλκ² μ’μμ. μλνλ©΄ λ©μκ±°λ μπ 

<img src="https://user-images.githubusercontent.com/24591259/114944994-84bfd180-9e83-11eb-9ee8-f6c8929dd099.png" width="400px"/>

`Add features and functionality`μμ 'Event Subscriptions'μ ν΄λ¦­ν©λλ€.

<img src="https://user-images.githubusercontent.com/24591259/114944379-71603680-9e82-11eb-84fc-3f0aacfb1890.png" width="400px"/>

``Event``λ₯Ό Enable(νμ±ν) μν¨ν ``Requst URL``μ λ£μ΄μ μΈμ¦μ ν©λλ€. <br/>
λ‘μ»¬μμ νμ€νΈ νκΈ° μν΄ <a href="https://dashboard.ngrok.com/get-started/setup">ngrok<a/>μ μ¬μ©νμλ©΄ νΈν©λλ€.μ€μ  prod νκ²½μμλ `Nginx + uvicorn`μΌλ‘ μ€ννλ©΄ λμ! 
<br/>Nginx Config μμ `proxy_pass` λ§ uvicornμΌλ‘ μ€νν λ‘μ»¬ μλ²λ‘ μ°κ²°ν΄μ£Όλ©΄ λ©λλ€!<br/>

<img src="https://user-images.githubusercontent.com/24591259/114944830-45918080-9e83-11eb-9bfa-01c86bd8f9bd.png" width="400px"/>

`ngrok`μ ν΅ν΄ μΈλΆλ§μμ λ‘μ»¬λ‘ μ°κ²°μ΄ λ λͺ¨μ΅

<img src="https://user-images.githubusercontent.com/24591259/114946460-2811e600-9e86-11eb-8cc5-bbb8bcf7db42.png" width="400px"/>

`Heymoji`λ μ¬λ λ©€λ²λ€μ `reaction_added`, `reaction_removed` μ΄λ²€νΈμ botμ νΈμΆνλ `app_mention` μ΄λ κ² 3κ°μ§ μ΄λ²€νΈλ₯Ό λ°μ΅λλ€.

<img src="https://user-images.githubusercontent.com/24591259/153050733-875d2f7a-da23-42b6-a4a2-bbb35e6d2f82.png" width="400px"/>
<img src="https://user-images.githubusercontent.com/24591259/153050405-191203ea-3a0c-450e-bac2-fb66aef7e3ab.png" width="400px"/>

μ¬λλ΄κ³Ό DMμ ν΅ν΄ λͺλ Ήμ΄λ₯Ό μ€ννκΈ° μν΄μλ `message.im`μ μ ννκ³  Message Tab κΈ°λ₯μ on μμΌμ£ΌμμΌ ν©λλ€.<br/>

λ§μ§λ§μΌλ‘ `app`μ `workspace`μ μ€μΉ(install)νλ©΄ μ€μ ν μ΄λ²€νΈκ° μΌμ΄λ λλ§λ€ `slack`μμ `Heymoji`μλ²λ‘ μΉν apiλ₯Ό νΈμΆν©λλ€.


# νλ‘ νΈ μμ  π²
![vllo 5](https://user-images.githubusercontent.com/24591259/115112136-0405f000-9fbf-11eb-8fcf-9527d0bc5188.GIF)

κ°λ¨νκ² ``vue``νλ‘μ νΈμμ `Heymoji`μ apiλ₯Ό νΈμΆν΄ **User list**λ₯Ό λ³΄μ¬μ£Όλλ‘ λ§λ€μ΄ λ΄€μ΅λλ€.<br/>
μ΄λͺ¨μ§ μΆκ°, μ κ±° eventμ λ°λΌ μλ²μμ count λ‘μ§μ μ²λ¦¬ν΄μ£Όλκ±Έ νμΈ ν  μ μμ΅λλ€.
<a href="https://github.com/JAY-Chan9yu/emoji_rank_web">Emoji rank web<a/> νλ‘μ νΈλ₯Ό **clone** ν΄μ νμΈν΄λ³΄μΈμπ
