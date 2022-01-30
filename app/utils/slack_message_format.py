

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
            "block_id": "section567",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 가장 많은 사랑을 받은 크루는?! *{best_users.get('❤️')}*\n:heart:"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://i.pinimg.com/originals/bf/88/4c/bf884cb9b29803db712b77f1bce4f462.jpg",
                "alt_text": "Haunted hotel image"
            }
        },
        {
            "type": "section",
            "block_id": "section568",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 개그맨 보다 더 많은 웃음을 준 크루는?! *{best_users.get('🤣')}*\n:kkkk: :기쁨:"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://t1.daumcdn.net/cfile/tistory/99E10D3F5ADC079602",
                "alt_text": "Haunted hotel image"
            }
        },
        {
            "type": "section",
            "block_id": "section569",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 많은 크루를 도와준 천사 크루는?! *{best_users.get('🙏️')}*\n:pray: :기도:"
            },
            "accessory": {
                "type": "image",
                "image_url": "http://images.goodoc.kr/images/article/2018/08/20/428733/43bedd6ad60a_3bbaf99a964d.png",
                "alt_text": "Haunted hotel image"
            }
        },
        {
            "type": "section",
            "block_id": "section570",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 가장 많은 이슈를 처리해 준 크루는?! *{best_users.get('👍')}*\n"
                        f":+1: :wow: :wonderfulk: :천재_개발자:"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://cdn.clien.net/web/api/file/F03/11193449/82140da86eecc4.jpg?w=500&h=1000",
                "alt_text": "Haunted hotel image"
            }
        },
        {
            "type": "section",
            "block_id": "section571",
            "text": {
                "type": "mrkdwn",
                "text": f"이번 달 가장 많은 크루를 당황시킨 크루는?! *{best_users.get('👀️')}*\n:eye_shaking:"
            },
            "accessory": {
                "type": "image",
                "image_url": "https://d2u3dcdbebyaiu.cloudfront.net/uploads/atch_img/693/6ebb2cf8ed8a3f6cdebe2f6aedc640e6.jpeg",
                "alt_text": "Haunted hotel image"
            }
        }
    ]
