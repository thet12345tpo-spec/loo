import os
import asyncio
import re
import base64
import time
import hashlib
import random
import requests
import aiohttp
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin

# Terminal Color Codes
bcyan = "\033[1;36m"
reset = "\033[0m"
white = "\033[0;37m"
bgreen = "\033[1;32m"
bred = "\033[1;31m"
yellow = "\033[0;33m"

r = "\033[1;31m"
g = "\033[1;32m"
w = "\033[0m"

# Global variables
SUCCESS = 0
TIMEOUT_SEC = 10

def show_banner():
    try:
        os.system('clear' if os.name == 'posix' else 'cls')
    except:
        pass
    print(f"{bcyan}="*55)
    print(f"   ⚡ ALL RUIJIE HACK (KEEP-ALIVE) ⚡   ")
    print(f"{bcyan}="*55 + f"{reset}")

# --- Ruijie Login Manager Class ---
class RuijieLoginManager:
    def __init__(self):
        self.ip = None
        self.mac = None
        self.current_sid = None
        self.load_saved_ip()
        self.load_saved_mac()
        self.phone_number = "12345678901"

    def load_saved_ip(self):
        if os.path.exists(".ip"):
            try:
                with open(".ip", "r") as f:
                    self.ip = f.read().strip()
            except:
                self.ip = None

    def load_saved_mac(self):
        if os.path.exists(".mac"):
            try:
                with open(".mac", "r") as f:
                    self.mac = f.read().strip()
            except:
                self.mac = None

    async def check_internet(self, session):
        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        try:
            async with session.get(test_url, timeout=5, allow_redirects=False) as resp:
                if resp.status == 204:
                    return True
                return False
        except:
            return False

    async def auto_detect_gateway(self, session):
        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile'
        }
        
        try:
            async with session.get(test_url, headers=headers, timeout=5, allow_redirects=False) as resp:
                if resp.status in (301, 302):
                    location = resp.headers.get('Location', '')
                    parsed_url = urlparse(location)
                    query_params = parse_qs(parsed_url.query)
                    
                    gw_addr_list = query_params.get('gw_address')
                    if gw_addr_list:
                        self.ip = gw_addr_list[0]
                        with open(".ip", "w") as f:
                            f.write(self.ip)

                    mac_list = query_params.get('mac') or query_params.get('umac') or query_params.get('usermac')
                    if mac_list:
                        self.mac = mac_list[0]
                        with open(".mac", "w") as f:
                            f.write(self.mac)

                    if gw_addr_list:
                        return True
                else:
                    if self.ip and self.mac:
                        return True
        except Exception:
            if self.ip and self.mac:
                return True
        return False

    async def _fetch_sid(self, session):
        if not self.ip or not self.mac:
            return None

        step1_url = "https://portal-as.ruijienetworks.com/auth/wifidogAuth/login/?gw_id=4c496809aa9c&gw_sn=H1U826N00439B&gw_address=192.168.110.1&gw_port=2060&ip=192.168.110.118&mac=d2:95:18:6f:b7:d8&slot_num=16&nasip=192.168.1.220&ssid=VLAN233&ustate=0&mac_req=1&url=http%3A%2F%2Fconnectivitycheck%2Egstatic%2Ecom%2Fgenerate%5F204&chap_id=%5C176&chap_challenge=%5C331%5C216%5C362%5C140%5C112%5C240%5C136%5C233%5C324%5C127%5C375%5C062%5C221%5C340%5C220%5C005"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; 22101316C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.120 Mobile',
            'X-Requested-With': 'mark.via.gp',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        }
        
        try:
            async with session.get(step1_url, headers=headers, timeout=TIMEOUT_SEC) as r1:
                if r1.status != 200:
                    return None
                
                body = await r1.text()
                js_match = re.search(r"self\.location\.href\s*=\s*['\"]([^'\"]+)['\"]", body)
                if not js_match:
                    return None
                
                api_path = js_match.group(1)
                base_url = "https://portal-as.ruijienetworks.com"
                step2_url = urljoin(base_url, api_path)

            async with session.get(step2_url, headers=headers, timeout=TIMEOUT_SEC, allow_redirects=False) as r2:
                if r2.status == 302:
                    location = r2.headers.get('Location', '')
                    parsed_url = urlparse(location)
                    query_params = parse_qs(parsed_url.query)
                    sid_list = query_params.get('sessionId')
                    
                    if sid_list:
                        sid = sid_list[0]
                        self.current_sid = sid
                        return sid
                        
        except Exception:
            return None

    async def login_voucher(self, session, voucher):
        if not self.current_sid:
            self.current_sid = await self._fetch_sid(session)
            
        if not self.current_sid:
            return False

        data = {
            "accessCode": voucher,
            "sessionId": self.current_sid,
            "apiVersion": 1
        }
        
        post_url = base64.b64decode(b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3ZvdWNoZXIvP2xhbmc9ZW5fVVM=').decode()
        
        headers = {
            "authority": "portal-as.ruijienetworks.com",
            "accept": "*/*",
            "content-type": "application/json",
            "origin": "https://portal-as.ruijienetworks.com",
            "referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?RES=./../expand/res/kunji5dg96teooiimnl&IS_EG=0&sessionId={self.current_sid}",
            "user-agent": 'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        }
        
        try:
            async with session.post(post_url, json=data, headers=headers) as req:
                response = await req.text()
                if 'logonUrl' in response:
                    return True
                return False 
        except Exception:
            return False

    async def send_request(self, session):
        if not self.current_sid:
            sid = await self._fetch_sid(session)
            if not sid:
                return False
        else:
            sid = self.current_sid

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        }
        
        params = {
            'token': sid,
            'phoneNumber': self.phone_number,
        }

        try:
            auth_url = f'http://{self.ip}:2060/wifidog/auth'
            async with session.post(auth_url, params=params, headers=headers, timeout=TIMEOUT_SEC) as response:
                if response.status == 200:
                    return True
                return False
        except Exception:
            return False

    async def run_auth_flow(self, session, voucher):
        if await self.check_internet(session):
            print(f"{g}[+] Internet is active. Monitoring...{reset}")
            return True

        print(f"{yellow}[*] Connection lost or not active. Re-authenticating...{reset}")
        detected = await self.auto_detect_gateway(session)
        if not detected:
            print(f"{r}[!] Gateway not detected.{reset}")
            return False

        sid = await self._fetch_sid(session)
        if not sid:
            print(f"{r}[!] Failed to fetch Session ID.{reset}")
            return False

        login_success = await self.login_voucher(session, voucher)
        if login_success:
            final_auth = await self.send_request(session)
            if final_auth:
                print(f"{g}[+] Successfully Logged In!{reset}")
                return True
        
        print(f"{r}[!] Authentication failed.{reset}")
        return False

# --- Tool Executor Flow ---
async def start_tool():
    show_banner()
    user_voucher = input(f"\n{yellow} Enter Voucher Code : {reset}").strip()

    if not user_voucher:
        print(f"{r}[!]Need Voucher code{reset}")
        return

    manager = RuijieLoginManager()
    async with aiohttp.ClientSession() as session:
        print("\n[ * ] Starting Keep-Alive flow. Press Ctrl+C to stop.")
        while True:
            try:
                await manager.run_auth_flow(session, voucher=user_voucher)
                # Check every 60 seconds
                await asyncio.sleep(15)
            except KeyboardInterrupt:
                print("\n[!] Program stopped by user.")
                break
            except Exception as e:
                print(f"{r}[!] Loop Error: {e}{reset}")
                await asyncio.sleep(10)

def run():
    try:
        asyncio.run(start_tool())
    except KeyboardInterrupt:
        print("\n[!] Program stopped by user.")

if __name__ == "__main__":
    run()
