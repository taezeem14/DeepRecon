import requests
from stem import Signal
from stem.control import Controller
from config import TOR_SOCKS_PROXY, TOR_CONTROL_PORT, TOR_CONTROL_PASSWORD

def renew_ip():
    with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
        controller.authenticate(password=TOR_CONTROL_PASSWORD)
        controller.signal(Signal.NEWNYM)

def get_session():
    session = requests.Session()
    session.proxies = {
        'http': TOR_SOCKS_PROXY,
        'https': TOR_SOCKS_PROXY
    }
    return session
