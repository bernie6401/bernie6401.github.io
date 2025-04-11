---
title: Fastbot Android
tags: [Tools]

category: "Tools > Others > Android App Crawler"
---

# Fastbot Android
以下流程皆是參考[CSDN-Android APP穩定性測試工具Fastbot](https://blog.csdn.net/u010698107/article/details/127347704)和[官方中文教學](https://github.com/bytedance/Fastbot_Android/blob/main/handbook-cn.md)
## 一般使用
1. 把repo clone下來，並且把一些檔案複製到手機
    ```bash
    $ git clone https://github.com/bytedance/Fastbot_Android.git
    $ cd Fastbot_Android
    $ adb push fastbot-thirdpart.jar /sdcard
    $ adb push framework.jar /sdcard
    $ adb push monkeyq.jar /sdcard
    $ adb push libs/. /data/local/tmp/
    ```
2. dump apk內部會使用到的strings，並且複製到手機
    ```bash
    $ aapt2 dump strings <your apk name> > max.valid.strings
    $ adb push max.valid.strings /sdcard 
    ```
3. 獲取device number和package name
    ```bash
    $ adb devices
    List of devices attached
    24121JEGR04513  device
    $ aapt2 dump badging "Spotify_ Music and Podcasts_8.9.60.560_APKPure.apk" | findstr "package"
    package: name='com.spotify.music' versionCode='116920144' versionName='8.9.60.560' platformBuildVersionName='14' platformBuildVersionCode='34' compileSdkVersion='34' compileSdkVersionCodename='14'
    uses-permission: name='com.sec.android.app.clockpackage.permission.READ_ALARM'
5. 實際測試
    ```bash
    $ adb shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p <package name> --agent reuseq --running-minutes <遍歷時長> --throttle <事件頻率> -v -v
    ---
    $ adb shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p com.spotify.music --agent reuseq --running-minutes 1 --throttle 500 -v -v --output-directory /sdcard/fastbot_results&adb pull /sdcard/fastbot_results D:\Downloads
    ```
## 輸入自訂Strings
1. Download ADBKeyBoard，安裝後設定預設keyboard為ADBKeyboard
    ```bash
    $ wget https://github.com/senzhk/ADBKeyBoard/raw/master/ADBKeyboard.apk
    $ adb install ADBKeyboard.apk
    $ adb shell ime enable com.android.adbkeyboard/.AdbIME
    $ adb shell ime set com.android.adbkeyboard/.AdbIME
    ```
2. 設定config並push到手機
    ```bash
    $ echo "max.randomPickFromStringList = true" > max.config
    $ adb push max.config /sdcard
    ```
3. 設定像要輸入的strings並push到手機
    ```bash
    $ echo "test string" > max.strings
    $ adb push max.strings /sdcard
    ```
:::info
* 如何設定成原本的keyboard
    ```bash
    $ adb shell ime reset
    ```
* 傳送text
    ```bash
    $ adb shell am broadcast -a ADB_INPUT_TEXT --es msg 'test'
    ```
* 全選目前textview的strings
    ```bash
    $ adb shell am broadcast -a ADB_INPUT_TEXT --es mcode '4096,29'
    ```
* Delete Strings
    ```bash
    $ adb shell am broadcast -a ADB_INPUT_CODE --ei code 67
    ```
:::
## 自訂前期的Script
如果想要自行設定前期的登入或是註冊這樣的flow，就可以利用這個模式，只要先設定好XPATH和action，Fastbot就會按照我們給定的config去執行，執行完了之後就會繼續執行我們前面給的command依序crawl
### 設定config
這個部分有點複雜，如果是像spotify這樣因為無法screenshot而無法使用Appium Inspector工具的就會更複雜
1. 在PC上創一個`max.xpath.actions`文件
2. 利用Maxim知道目前的activity name
    ```bash
    $ git clone https://github.com/zhangzhao4444/Maxim.git
    $ cd Maxim
    $ adb push framework.jar /sdcard
    $ adb push monkey.jar /sdcard
    $ adb shell CLASSPATH=/sdcard/Maxim/monkey.jar:/sdcard/Maxim/framework.jar exec app_process /system/bin tv.panda.test.monkey.api.CurrentActivity
    [Maxim] current activity:
    [Maxim] // com.spotify.login.loginflowimpl.LoginActivity
    ```
2. 獲取想要互動的View的XPATH
    如果可以screenshot的話，就可以利用Appium-Inspector，否則可以用我給的script慢慢爬，只要手機USB連線，並且開啟想要爬的activity頁面，執行下方script，就會print出目前和該app有關的clickable/editable view XPATH，以下用spotify為例
    :::spoiler Fetch XPATH Script
    ```python
    import os
    import uiautomator2 as u2
    import xml.etree.ElementTree as ET

    def adb_devices() -> str:  # 取得所有模擬器名稱與狀態
        cmd = 'adb devices'
        process = os.popen(cmd)
        result = process.read().split('\n')
        text = []
        for line in result:
            if 'List of devices' not in line and line != '' and line != ' ':  # 去掉標題跟空白字串
                text.append(line)
        devices = {}
        for i in range(len(text)):
            words = text[i].split('\t')  # 格式: emulator-5554\tdevice
            if 'device' in words[1]:  # 只存有啟動的模擬器
                devices[i] = words[0]  # 用模擬器index當key
        if len(devices) == 0:
            print('[x] None emulator is running')
            raise Exception
        return devices

    def connect_single_device(emulator: str) -> u2.Device:
        try:
            d = u2.connect(emulator)
            return d
        except:
            print('[x] Unable to connect to the emulator')
            raise Exception

    def generate_xpath(view):
        """
        根据视图的属性生成 XPath。
        :param view: 视图的属性字典
        :return: 生成的 XPath 字符串
        """
        xpath = f"//{view['class']}"

        conditions = []
        if view['index']:
            conditions.append(f"@index='{view['index']}'")
        if view['text']:
            conditions.append(f"@text='{view['text']}'")
        if view['resource-id']:
            conditions.append(f"@resource-id='{view['resource-id']}'")
        if view['package']:
            conditions.append(f"@package='{view['package']}'")
        if view['content-desc']:
            conditions.append(f"@content-desc='{view['content-desc']}'")
        if view['clickable']:
            conditions.append(f"@clickable='{view['clickable']}'")

        if conditions:
            xpath += "[" + " and ".join(conditions) + "]"

        return xpath

    def main(emulator: str):
        d = connect_single_device(emulator)

        # get the UI hierarchy dump content
        xml = d.dump_hierarchy(compressed=False, pretty=True, max_depth=50)
        root = ET.fromstring(xml)

        if clickable_views.get(activity_level) is None:
            clickable_views[activity_level] = []
        if editable_views.get(activity_level) is None:
            editable_views[activity_level] = []

        # Find all clickable & editable views
        for view in root.iter():
            resource_id = view.attrib.get('resource-id', '')
            clickable = view.attrib.get('clickable', 'false')
            package_name = view.attrib.get('package', '')
            if any(app_name.lower() in a for a in [resource_id, package_name]) and clickable == 'true':
                print("Clickable View XPATH: ", generate_xpath(view.attrib))
        for view in root.findall(".//*[@class='android.widget.EditText']"):
            resource_id = view.attrib.get('resource-id', '')
            if app_name.lower() in resource_id:
                print("Editable View XPATH: ", generate_xpath(view.attrib))

    if __name__ == '__main__':
        clickable_views = {}
        editable_views = {}
        app_name = 'Spotify'
        activity_level = 0

        try:
            emulators = adb_devices()
        except:
            print('[x] Cannot get the list of emulators, the program will be terminated. Please use adb devices to check if the emulator is running')
            exit()

        main(emulators[0])
    ```
    :::
    ```bash
    $ python fetchXPATH.py
    Clickable View XPATH:  //android.widget.Button[@index='0' and @text='Sign up free' and @package='com.spotify.music' and @clickable='true']
    Clickable View XPATH:  //android.widget.Button[@index='1' and @text='Continue with Google' and @package='com.spotify.music' and @clickable='true']
    Clickable View XPATH:  //android.widget.Button[@index='2' and @text='Continue with Facebook' and @package='com.spotify.music' and @clickable='true']
    Clickable View XPATH:  //android.widget.Button[@index='3' and @text='Log in' and @package='com.spotify.music' and @clickable='true']
    ```
3. 接下來就把XPATH貼到下方格式的地方就可以了
    在同一個activity的步驟不需要拆分，詳細說明可以看[Fastbot handbook](https://github.com/bytedance/Fastbot_Android/blob/main/handbook-cn.md#%E8%87%AA%E5%AE%9A%E4%B9%89%E4%BA%8B%E4%BB%B6%E5%BA%8F%E5%88%97)
    ```json
    [
    {
        "prob": 1,
        "activity": "com.spotify.login.loginflowimpl.LoginActivity",
        "times": 1,
        "actions": [
            {
                "xpath": "//android.widget.Button[@index='3' and @text='Log in' and @package='com.spotify.music' and @clickable='true'",
                "action": "CLICK",
                "throttle" : 2000
            },
            {
                "xpath": "//*[@resource-id='com.spotify.music:id/username_text']",
                "action": "CLICK",
                "text": "username",
                "throttle" : 2000
            },
            {
                "xpath": "//*[@resource-id='com.spotify.music:id/password_text']",
                "action": "CLICK",
                "text": "password",
                "throttle" : 2000
            },
            {
                "xpath": "//*[@resource-id='com.spotify.music:id/login_button' and @text='Log in']",
                "action": "CLICK",
                "throttle" : 2000
            }
        ]
    }
    ]
    ```
    把以上json格式填寫好後，丟到[Json Checker](https://www.json.cn/)檢查有無問題，注意最一開始和最後一定是中括號，格式正確後再填寫到==max.xpath.actions==，並且丟到手機上
    ```bash
    $ adb push max.xpath.actions /sdcard
    ```
### 注意
:::info
1. 如果有想要填寫文字的情況就一定要保證是用ADBKeyboard的狀態下才會如實的填寫我們設定好的text
2. Fastbot預設會到/sdcard抓max.xpath.actions，所以不要放到其他地方
:::