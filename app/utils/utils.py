

def mapping_slack_command_to_dict(event_command: list) -> dict:
    mapped_attr = {}

    for cmd in event_command:
        try:
            # todo: 커맨드 형태 개선하기
            if '--avatar_url' in cmd:
                info = cmd.split('--avatar_url=')
                key = 'avatar_url'
                value = info[1].strip('<>')
            else:
                info = cmd.split('=')
                key = info[0].replace('--', '')
                value = info[1]

            mapped_attr[key] = value

        except:
            continue

    return mapped_attr
