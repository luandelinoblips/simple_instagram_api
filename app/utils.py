import requests
import re
import unicodedata

proxies = {
    'http': None,
    'https': None,
}


def fetch_user_data(username: str) -> dict:
    URL_BASE = 'https://www.instagram.com/api/v1/users/web_profile_info'
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        ),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
    }
    try:
        response = requests.get(
            URL_BASE,
            params={'username': username},
            headers=headers,
            proxies=proxies,
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
