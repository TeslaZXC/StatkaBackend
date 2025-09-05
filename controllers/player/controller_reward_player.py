from services.player.service_reward_player import find_json_by_name as service_find_json

def get_json(name: str):
    return service_find_json(name)