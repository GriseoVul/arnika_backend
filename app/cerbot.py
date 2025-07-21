import subprocess
from datetime import datetime
from ..config import settings


#not used 
def renew_cert():
    try:
        result = subprocess.run([
            'certbot', 'renew',
            '--non-interactive',
            '--agree-tos',
            '--email', settings.email,
            '--webroot', '-w', '/var/www/certbot'
        ],
        capture_output=True, text=True)
        if result.returncode == 0:
            return True
        
    except Exception as e:
        print(e)
        return False