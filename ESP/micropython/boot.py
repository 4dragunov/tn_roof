import gc, webrepl, esp, network, json, os, time
MAIN=None

#В файле config.json держим логин и пароль сети
#{"wlan_pwd": "XXXX", "wlan": "XXXX"}

def init():
    global MAIN
    lst = os.listdir()
    if 'config.json' in lst:
        try:
            with open('config.json', 'r') as x:
                cfg = json.load(x)
        except:
            return

    if 'wlan' in cfg:
        wlan = network.WLAN(network.AP_IF)
        wlan.active(False)

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(cfg['wlan'], cfg['wlan_pwd'])

        x = 0 # 10 секунд ждем соединения WiFi
        while x < 10:
            if wlan.isconnected():
                webrepl.start()
                break
            x += 1
            time.sleep(1)

    # если есть main пытаемся запустить
    if 'main.py' in lst:
        MAIN = __import__('main')
        lst = dir(MAIN)
        if 'init' in lst:
            MAIN.init()

esp.osdebug(None)
init()
gc.collect()