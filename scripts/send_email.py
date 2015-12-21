# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import ntpath, re, smtplib

# Define these once; use them twice!
msgText = '<strong>Some <i>HTML</i> text</strong> and an image.\
           <br><br>\
           {img}'

strFrom = 'rtester@digitalvirgoamericas.com'
strTo   = 'lagudelo@digitalvirgoamericas.com'
img     = []
ids     = []
sImg    = ''
img.append("./static/screenshots/2015-12-21/southwap2.png")
img.append("./static/screenshots/2015-12-21/southwap3.png")
img.append("./static/screenshots/2015-12-21/southwap4.png")



# Create the root message and fill in the from, to, and subject headers
msgRoot            = MIMEMultipart('related')
msgRoot['Subject'] = 'test message'
msgRoot['From']    = strFrom
msgRoot['To']      = strTo
msgRoot.preamble   = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

for i in img:
    # This example assumes the image is in the current directory
    fp       = open(i, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    i = ntpath.basename(i).split('.')[0]

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgImage.add_header('Content-ID', '<' + i + '>')
    msgRoot.attach(msgImage)
    sImg += '<img src="cid:' + i + '"><br><br>'

msgText = MIMEText(msgText.replace('{img}', sImg), 'html')
msgAlternative.attach(msgText)

# Send the email (this example assumes SMTP authentication is required)
smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login(strFrom, 'remote123')

smtp.sendmail(strFrom, strTo, msgRoot.as_string())
smtp.quit()
