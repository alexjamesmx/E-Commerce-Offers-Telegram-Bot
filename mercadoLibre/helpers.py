import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from consts import AFFILIATE_ID , COOKIE, X_CSRF_TOKEN

def add_emojis(header_message, category, discount):
    if discount < 60:
        return header_message
    emojis = {
        "MLM1747": "🚗", "MLM189530": "🎁", "MLM1403": "🍔",
        "MLM1071": "🐶", "MLM1367": "🕰️", "MLM1368": "🎨",
        "MLM1384": "👶", "MLM1246": "💄", "MLM1039": "📷",
        "MLM1051": "📱", "MLM1648": "💻", "MLM1144": "🎮",
        "MLM1500": "🚧", "MLM1276": "🏋️", "MLM1575": "🥃",
        "MLM1000": "🎧", "MLM186863": "🔧", "MLM1574": "🏡",
        "MLM1499": "🏢", "MLM1182": "🎸", "MLM3937": "⌚",
        "MLM1132": "🎲", "MLM3025": "📚", "MLM1168": "🎥",
        "MLM44011": "🎉", "MLM1430": "👗", "MLM187772": "🩺",
    }
    random_choice = random.choice([1, 2]) 
    if random_choice == 1: 
        exclamation_word = random.choice(["SUPER", "INCREIBLE"]) 
        discount_word = random.choice(["DESCUENTO", "OFERTA", "PRECIO"])
        final_message =  exclamation_word + " " + discount_word  
    else: 
        final_message = random.choice([ "ERROR DE PRECIO", "CORRE YAA", "CORRE YA", "EN SU PRECIO MAS BAJO" ])

    return f"📢⚠️¡{final_message}!\n\n{header_message} {emojis.get(category, '')}" 

def generate_affiliation_link(item_link, logger):
    url = 'https://www.mercadolibre.com.mx/affiliate-program/api/affiliates/v1/createUrls'
    headers = {
        "X-Csrf-Token": X_CSRF_TOKEN, 
        "Accept-Encoding": "gzip, deflate, br", 
        "Cookie": COOKIE, 
    }
    payload = {
        "tag": AFFILIATE_ID,
        "urls": [item_link],
    }
    try:
        response = requests_retry_session().post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get('urls')[0].get('short_url')
        else:
            logger.error(f"Error generating affiliation link: {response.status_code} {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None
    
def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def parse_cookies(cookie_string):
    '''
    Parse a cookie string into a dictionary 
    '''
    cookies = {}
    parts = cookie_string.split('; ')
    for part in parts:
        name, value = part.split('=', 1)
        cookies[name] = value
    return cookies