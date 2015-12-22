from flask import Flask, render_template, request
from subprocess import  check_output, call
from uiautomator import  Device
from shutil import copyfile
import xml.etree.ElementTree as ET
import time, random, os, re, sqlite3, json

app = Flask(__name__)

def dbQuery(query):
    conn = sqlite3.connect('data/uioctopus.db')
    c = conn.cursor()
    result = c.execute(query)
    conn.commit()
    return result

def findTree(tree,info):
    items = []
    for item in tree:
        bounds = item.get('bounds').replace('][',',').replace('[','').replace(']','').split(',')
        if item.get('clickable') == "true":
            if (0 <= int(bounds[0]) <= int(info['displayWidth'])) and (0 <= int(bounds[1]) <= int(info['displayHeight'])):
                items.append(item)
        if len(list(item)) > 0:
            items += findTree(item, info)
    return items

def getProp(serial):
    props = {} 
    rawProp = os.popen("adb -s " + serial + " shell getprop | grep -E 'model|manufacturer|serialno|product.name|brand|gsm.sim.operator.alpha' | awk -F \": \" '{ gsub(/(ro\.)|([\[\]])/, \"\", $0); print $1, $2 }'").read().strip().split('\n')
    for p in rawProp:
        row = p.split(' ')
        if len(row) >= 3:
            props[row[0]] = row[1] + " " + row[2]
        else:
            props[row[0]] = row[1]
    return props

def device():
    seriales = check_output(['adb', 'devices'])
    seriales = str(seriales).strip().split('\\n')
    seriales.pop(0)
    new_serial = {} 
    for serial in seriales:
        data = serial.split('\\t')
        if (len(data) >  1):
            new_serial[data[0]] = {'properties': getProp(data[0])}
    return new_serial

@app.route('/')
def index():
    seriales = device()
    return render_template('load.html', seriales=seriales)

@app.route('/page/<serial>')
def  page(serial):
    d = Device(serial)
    f = 'screenshots/work.png'
    d.screenshot('static/' + f)
    info = d.dump()
    tree = ET.fromstring(info.encode('utf-8'))
    data = d.info
    items = findTree(tree, data)
    return render_template('index.html', xml=items, serial=serial, device_info=data, file=f, rd=random.randint(0,9999))

@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        sName = request.form.get('subject').lower().replace(' ','-').replace('ñ','n') + '.py'
        sPath = './scripts/' + time.strftime("%Y-%m-%d") + '/' + sName
        iPath = './static/screenshots/' + time.strftime("%Y-%m-%d") + '/'

        if not os.path.exists(os.path.dirname(sPath)):
            os.makedirs(os.path.dirname(sPath))

        if not os.path.exists(os.path.dirname(iPath)):
            os.makedirs(os.path.dirname(iPath))

        dbQuery("INSERT INTO scripts(name, date, path) VALUES ('" + sName + "', datetime('now', 'localtime'), '" + sPath + "')");
        script  = request.form.get('myconsole')
        archivo = open(sPath, 'w')
        archivo.write(script)
        archivo.close()

    lscripts = dbQuery("SELECT * FROM scripts ORDER BY id DESC")
    return render_template('list.html', scripts=lscripts)

@app.route('/ejecutar', methods=['GET', 'POST'])
def ejecutar():
    script = request.args.get('script')
    exe    = os.popen('python3.4 ' + script + ' &').read()
    print(exe)
    return "ok"

#AJAX PAGES
@app.route('/load/<serial>')
def load(serial):
    if serial == 'null': 
        return 'nok'

    #Chrome
    os.popen("adb -s " + serial + " shell pm clear com.android.chrome").read()
    browserOn = os.popen("adb -s " + serial + " shell am start -a android.intent.action.VIEW -n com.android.chrome/com.google.android.apps.chrome.Main -d http://www.google.com/").read().strip().split('\n')

    #Default browser
    if len(browserOn) > 1 and re.match('Error', browserOn[1], re.I) is not None:
        os.popen("adb -s " + serial + " shell pm clear com.android.browser").read()
        browserOn = os.popen("adb -s " + serial + " shell am start -a android.intent.action.VIEW -n com.android.browser/.BrowserActivity").read().strip().split('\n')
    
    #Firefox
    if len(browserOn) > 1 and re.match('Error', browserOn[1], re.I) is not None:
        os.popen("adb -s " + serial + " shell pm clear org.mozilla.firefox").read()
        browserOn = os.popen("adb -s " + serial + " shell am start -a android.intent.action.VIEW -n org.mozilla.firefox/.App").read().strip().split('\n')
    
    if len(browserOn) > 1 and re.match('Error', browserOn[1], re.I) is not None:
        return 'nok'

    time.sleep(5)
    return 'ok'

@app.route('/add_text', methods=['GET'])
def add_text():
    serial = request.args.get('serial')
    d      = Device(serial)
    op     = int(request.args.get('op'))
    if op == 0:
        d(resourceId=request.args.get('text')).clear_text()
        d(resourceId=request.args.get('text')).set_text(request.args.get('value'))
    if op == 1:
        d(textContains=request.args.get('text'), className=request.args.get('class')).clear_text()
        d(textContains=request.args.get('text'), className=request.args.get('class')).set_text(request.args.get('value'))
    if op == 2:
        d(description=request.args.get('text'), className=request.args.get('class')).clear_text()
        d(description=request.args.get('text'), className=request.args.get('class')).set_text(request.args.get('value'))
    d.press.enter()
    time.sleep(5)
    return 'ok'

@app.route('/click', methods=['GET'])
def click():
    serial = request.args.get('serial')
    d = Device(serial)
    op = int(request.args.get('op'))
    if op == 1:
        d(text=request.args.get('text'), index=request.args.get('index')).click()
    if op == 2:
        d(description=request.args.get('text'), index=request.args.get('index')).click()
    if op == 3:
        d.click(int(request.args.get('text')), int(request.args.get('index')))
    time.sleep(5)
    return 'ok'

@app.route('/swipe', methods=['GET'])
def swipe():
    serial = request.args.get('serial')
    d = Device(serial)
    d.swipe(int(request.args.get('x0')),
            int(request.args.get('y0')),
            int(request.args.get('x1')),
            int(request.args.get('y1')))
    return 'ok'

@app.route('/geturl', methods=['GET'])
def geturl():
    serial = request.args.get('serial')
    rId    = 'com.android.chrome:id/url_bar'
    if( serial is not '' and serial is not None ):
        d = Device(serial)
        if d.exists(resourceId=rId):
            return d(resourceId=rId).info['text']
        
    return '#nok'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
