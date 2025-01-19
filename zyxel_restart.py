# Bu betik Zyzel VMG3312-B10B cihazlarını yeniden başlatmak için kullanılır
# Özgür Koca - Ocak / 2024

import requests
from bs4 import BeautifulSoup

# Cihaz IP adresi
cihaz_ip = '192.168.0.5'  # Bu değeri istediğiniz gibi değiştirebilirsiniz

# Kullanıcı adı ve şifre
username = 'admin'
password = 'parola'

# Giriş sayfasını alma
session = requests.Session()

# Oturum açma verileri
login_data = {
    'AuthName': username,
    'AuthPassword': password
}

# Oturum açma isteği gönder
login_url = f'http://{cihaz_ip}/login/login-page.cgi'
response = session.post(login_url, data=login_data)

# Session anahtarını al
cookies = response.headers.get('Set-Cookie')
session_value = None
if cookies:
    for cookie in cookies.split(';'):
        if cookie.strip().startswith('SESSION='):
            session_value = cookie.split('=')[1]
            break

if 'ifre yanl' in response.text.lower():
    print(f"Kullanici adı ({username}) veya parola ({password}) hatalı. Bitiriliyor.")
    exit()

if 'a user exist.' in response.text.lower():  
    print("Halihazırda bir kullanıcı oturumu açık. Bitiriliyor.")
    exit()
    
# Session anahtarı kullanılarak cihaz yeniden başlatılıyor
restart_url = f"http://{cihaz_ip}/pages/tabFW/reboot-rebootpost.cgi?sessionKey={session_value}"
response = session.get(restart_url)

print("Cihaz yeniden başlatıldı.")