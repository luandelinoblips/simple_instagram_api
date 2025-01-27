import requests
import re
import unicodedata


def fetch_user_data(username: str) -> dict:
    URL_BASE = 'https://www.instagram.com/api/v1/users/web_profile_info'
    headers = {
        'User-Agent': (
            'Mozillpair_0904ee679049452db29a988acdbffecaa/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'
        )
    }
    try:
        response = requests.get(
            URL_BASE, params={'username': username}, headers=headers
        )
        response.raise_for_status()
        return response.json().get('data', {}).get('user', {})
    except requests.RequestException:
        return {}


def normalize_username(username: str) -> str:
    normalized = ''.join(
        c
        for c in unicodedata.normalize('NFD', username)
        if unicodedata.category(c) != 'Mn'
    )
    return normalized.lower()


def try_username_with_strategies(base_username: str, strategies: list) -> dict:
    base_username = normalize_username(base_username)

    user_data = fetch_user_data(base_username)
    if user_data:
        return user_data

    for strategy in strategies:
        username_variant = strategy(base_username)
        user_data = fetch_user_data(username_variant)
        if user_data:
            return user_data

    return {}


def strategy_remove_spaces(username: str) -> str:
    """Remove all spaces from the username."""
    return username.replace(' ', '')


def strategy_remove_inner_underscores(username: str) -> str:
    match = re.match(r'(.*?)(_+)$', username)
    if match:
        name_part, trailing_underscores = match.groups()
        name_part = name_part.replace('_', '')
        return name_part + trailing_underscores
    return username.replace('_', '')
