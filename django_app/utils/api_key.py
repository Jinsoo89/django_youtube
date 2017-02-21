import json
import os


def call_api_key():
    current_file_path = os.path.abspath(__file__)

    go_to_parent_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    go_to_child_path_or_file = os.path.join(go_to_parent_path,
                                            '.conf/settings_local.json')

    with open(go_to_child_path_or_file, 'r') as f:
        config_str = f.read()

    config = json.loads(config_str)

    youtube_api_key = config['youtube']['API_KEY']

    return youtube_api_key
