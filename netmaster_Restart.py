import requests
from bs4 import BeautifulSoup

# Kullanıcı adı ve şifre
username = 'admin'
password = 'parola'

# Giriş sayfasını alma
session = requests.Session()
login_page = session.get('http://192.168.0.1/')

# Giriş sayfasının HTML'ini çözümleme
soup = BeautifulSoup(login_page.content, 'html.parser')

# Hidden input değerini çıkarma
login_id = soup.find('input', {'name': 'loginid'})['value']

# Oturum açma verileri
login_data = {
    'loginUsername': username,
    'loginPassword': password,
    'loginid': login_id,
    'LanguageType': 4,
    'LoginUserApply': 1
}


# Oturum açma isteği gönder
login_response = session.post('http://192.168.0.1/goform/login', data=login_data)

# Giriş başarılıysa otomatik olarak (HTTP 302) Wi-Fi ayar sayfasına yönlendirilir
if login_response.status_code == 200 and 'wpa' in login_response.text.lower():

    print("Giriş başarılı!")

    # Security sayfasına git ve formdaki random securityid'yi al
    security_page = session.get('http://192.168.0.1/RgSecurity.asp')
    soup = BeautifulSoup(security_page.content, 'html.parser')
    security_id = soup.find('input', {'name': 'RgSecurityId'})['value']

    # Yeniden başlatma verileri
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

    # Yeniden başlatma isteği
    restart_response = session.post('http://192.168.0.1/goform/RgSecurity', data=restart_data)

    if restart_response.status_code == 200 and 'cihaz yeniden' in restart_response.text.lower():
        print("Modem yeniden başlatıldı!")
    else:
        print("Yeniden başlatma başarısız!")
else:
    print("Giriş başarısız!")

# Oturumu kapat
session.close()
