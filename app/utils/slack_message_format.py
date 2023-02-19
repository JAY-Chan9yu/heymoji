from conf import settings


def get_best_user_format(title: str, best_users: dict) -> list:
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*{}*".format(title)
            }
        },
        {
            "type": "section",
            "block_id": "section560",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 우리회사 최고의 크루는?! *{best_users.get('🏆️', '🙈')}*\n:trophy:"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://storage.googleapis.com/jjalbot/2018/12/SJIet6EMlE/20180120_5a62ff609dd71.gif",
                "alt_text": "Haunted hotel image"
            }
        },
        {
            "type": "section",
            "block_id": "section567",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 가장 많은 사랑을 받은 크루는?! *{best_users.get('❤️', '🙈')}*\n:heart:"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://storage.googleapis.com/jjalbot/2018/12/SklaU6EzxN/20180920_5ba2faf231e8d.gif",
                "alt_text": "Haunted hotel image"
            }
        },
        {
            "type": "section",
            "block_id": "section568",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 개그맨 보다 더 많은 웃음을 준 크루는?! *{best_users.get('🤣', '🙈')}*\n"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://storage.googleapis.com/jjalbot/2018/12/H1U2e0EMgN/20161011_57fc9949dc934.gif",
                "alt_text": "Haunted hotel image"
            }
        },
        {
            "type": "section",
            "block_id": "section569",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 많은 크루를 도와준 천사 크루는?! *{best_users.get('🙏️', '🙈')}*\n:pray:"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://storage.googleapis.com/jjalbot/2019/01/HzRhFU0V79/GFA042s4h.gif",
                "alt_text": "Haunted hotel image"
            }
        },
        {
            "type": "section",
            "block_id": "section570",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 가장 많은 이슈를 처리해 준 크루는?! *{best_users.get('👍', '🙈')}*\n"
                        f":+1:"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://storage.googleapis.com/jjalbot/2016/10/BkZLvLpI0/20160901_57c79d42cb647.gif",
                "alt_text": "Haunted hotel image"
            }
        },
        {
            "type": "section",
            "block_id": "section571",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 가장 많은 크루를 당황시킨 크루는?! *{best_users.get('👀️', '🙈')}*\n"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://storage.googleapis.com/jjalbot/2018/12/L0XKZHmhX/zzal.gif",
                "alt_text": "Haunted hotel image"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"📊 통계 링크: {settings.config.RANK_URL or '링크를 설정해주세요!'}"
            }
        },
    ]


def get_help_msg() -> list:
    bot_name = settings.config.BOT_NAME
    return [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "🤖 저에게 DM을 보내셔도 아래 명령어들을 실행 할 수 있어요!\n"
                    "아래 명령어를 복사해서 사용하실 경우 코드블럭을 제거하시고 사용하세요~\n"
                    "```"
                    f"🏆 이모지 랭킹 URL\n"
                    f"{settings.config.RANK_URL or '링크를 설정해주세요!'}\n\n"
                    "🥳 멤버 등록\n"
                    "이름은 필수 입니다!\n"
                    f"<@{bot_name}> --create_user --name=이름 --avatar_url=이미지URL --department=부서\n\n"
                    "🛠 멤버 정보 업데이트\n"
                    "업데이트할 정보만 적어주세요!\n"
                    f"<@{bot_name}> --update_user --avatar_url=이미지URL\n\n"
                    "🎖 이번달 베스트 멤버 리스트 추출\n"
                    f"<@{bot_name}> --show_best_member --year=2022 --month=1\n\n"
                    "🙈 유저 숨기기\n"
                    f"<@{bot_name}> --hide_user --slack_id=슬랙ID\n\n"
                    "🙉 유저 보이기\n"
                    f"<@{bot_name}> --show_user --slack_id=슬랙ID"
                    f"```"
        }
    }]


def get_error_msg(err: str) -> list:
    return [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*오류가 생겼습니다!*\n"
                    f"관리자에게 문의해주세요 😢\n{err}"
        }
    }]


def get_command_error_msg() -> list:
    return [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*잘못된 명령어 입니다!*\n"
                    f"[<@{settings.config.BOT_NAME}> --help] 확인해보세요!🤪"
        }
    }]
