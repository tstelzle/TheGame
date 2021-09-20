GAMES = []


def get_game(game_id: str):
    for game in GAMES:
        if str(game["id"]) == game_id:
            return game["game"], True

    return None, False
