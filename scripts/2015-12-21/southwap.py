from uiautomator import Device
import time, os, sys
from subprocess import call, check_output
sys.path.append(os.path.join(os.path.abspath("./scripts")))
import myemail

os.popen("adb -s LGD7229d0db227 shell pm clear com.android.chrome").read()
os.popen("adb -s LGD7229d0db227 shell am start -a android.intent.action.VIEW -n com.android.chrome/com.google.android.apps.chrome.Main -d http://www.google.com/").read()
d = Device("LGD7229d0db227")
img = []
d(resourceId="com.android.chrome:id/url_bar").clear_text()
d(resourceId="com.android.chrome:id/url_bar").set_text("http://southwap.com/")
d.press.enter()
time.sleep(20)
d.click(386, 661)
time.sleep(20)
d.screenshot("static/screenshots/2015-12-21/southwap2.png")
img.append("static/screenshots/2015-12-21/southwap2.png")
d.click(341, 600)
time.sleep(20)
d.screenshot("static/screenshots/2015-12-21/southwap3.png")
img.append("static/screenshots/2015-12-21/southwap3.png")
d.click(317, 597)
time.sleep(20)
d.screenshot("static/screenshots/2015-12-21/southwap4.png")
img.append("static/screenshots/2015-12-21/southwap4.png")
myemail.mail("lagudelo@digitalvirgoamericas.com", "Southwap", "Southwap", img)
myemail.clean(img)
