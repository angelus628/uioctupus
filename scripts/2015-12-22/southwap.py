from uiautomator import Device
import time, os, sys
from subprocess import call, check_output
sys.path.append(os.path.join(os.path.abspath("./scripts")))
import myemail

os.popen("adb -s LGD7229d0db227 shell pm clear com.android.chrome").read()
os.popen("adb -s LGD7229d0db227 shell am start -a android.intent.action.VIEW -n com.android.chrome/com.google.android.apps.chrome.Main -d http://www.google.com/").read()
d = Device("LGD7229d0db227")
img = []
iText = ""
iText = d(resourceId="com.android.chrome:id/url_bar").info['text']
d(resourceId="com.android.chrome:id/url_bar").clear_text()
d(resourceId="com.android.chrome:id/url_bar").set_text("http://southwap.com/")
d.press.enter()
time.sleep(20)
iText += "southwap.com"
d.screenshot("static/screenshots/2015-12-22/southwap1.png")
img.append("static/screenshots/2015-12-22/southwap1.png")
d.click(327, 538)
time.sleep(20)
iText += "www.celmovil.co/?landed=True&v=SGMv2_sexy_2&c=CE-SMT"
d.screenshot("static/screenshots/2015-12-22/southwap2.png")
img.append("static/screenshots/2015-12-22/southwap2.png")
d.click(358, 593)
time.sleep(20)
iText += "smt.claro.com.co/portalone/subscribe.action?&pid=MDSP2000011095&sid=0016242000010163&access=wap&adprovider=iTelcel&pic=http%3A%2F%2Fwww.celmovil.co%2FHome%2FImage%3Fv%3DSGMv2_sexy_2%26x%3Da%26n%3Dsmt.gif&language=es&url=http%3A%2F%2Fmiclub.co%2FMemberZone%2F%3Ft%3D3219365804&css=http%3A%2F%2Fwww.celmovil.co%2FSites%2FLandings%2FClaroColombia%2FSGMv2_sexy_2%2Fclub.css"
d.screenshot("static/screenshots/2015-12-22/southwap3.png")
img.append("static/screenshots/2015-12-22/southwap3.png")
myemail.mail("lagudelo@digitalvirgoamericas.com", "Southwap", "Southwap", img)
myemail.clean(img)
