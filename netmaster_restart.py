# ----------------------------------------------------------------------
# Netmaster Kablo Modem (Infinity 401) model cihaz için geliştirilmiştir.
# Diğer modellerde çalışacağının garantisi yoktur.
# Ozgur Koca / ozgurkoca@gmail.com
# ----------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

# Modem IP
IP = "192.168.0.1"

BASE = f"http://{IP}"

# Kullanıcı adı ve şifre
username = 'admin'
password = 'parola'

# Oturum başlat
session = requests.Session()

# Giriş sayfasını al
login_page = session.get(f'{BASE}/')

# HTML parse
soup = BeautifulSoup(login_page.content, 'html.parser')

# Hidden input loginid
login_id = soup.find('input', {'name': 'loginid'})['value']

# Login payload
login_data = {
    'loginUsername': username,
    'loginPassword': password,
    'loginid': login_id,
    'LanguageType': 4,
    'LoginUserApply': 1
}

# Login POST isteği
login_response = session.post(f'{BASE}/goform/login', data=login_data)

# Giriş başarılı mı?
if login_response.status_code == 200 and 'wpa' in login_response.text.lower():

    print("Giriş başarılı!")

    # Security sayfasına git → securityId al
    security_page = session.get(f'{BASE}/RgSecurity.asp')
    soup = BeautifulSoup(security_page.content, 'html.parser')
    security_id = soup.find('input', {'name': 'RgSecurityId'})['value']

    # Restart payload
    restart_data = {
      'RgSecurityId': security_id + "&#65533;",
      'ResetModem': 1,
      'Password': "",
      'PasswordReEnter': "",
      'OldPassword': "",
      'DosPreventionOn': "0x01",
      'RestoreFactoryNo': "0x00",
      'RgRouterBridgeMode': "1"
    }

    # Restart isteği
    restart_response = session.post(f'{BASE}/goform/RgSecurity', data=restart_data)

    if restart_response.status_code == 200 and 'cihaz yeniden' in restart_response.text.lower():
        print("Modem yeniden başlatıldı!")
    else:
        print("Yeniden başlatma başarısız!")

else:
    print("Giriş başarısız!")

# Oturumu kapat
session.close()
