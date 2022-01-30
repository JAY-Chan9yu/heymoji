

def mapping_slack_command_to_dict(event_command: list) -> dict:
    mapped_attr = {}

    for cmd in event_command:
        try:
            info = cmd.split('=')
            mapped_attr[info[0].replace('--', '')] = info[1]
        except:
            continue

    return mapped_attr
