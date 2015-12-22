from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import ntpath, re, smtplib, os

gmail_user = "rtester@digitalvirgoamericas.com"
gmail_pwd  = "remote123"

def mail(to, subject, text, attaches):
   sImg           = ''
   msg            = MIMEMultipart()

   msg['From']    = gmail_user
   msg['To']      = to
   msg['Subject'] = subject

   if( len(attaches) > 0 ):
       for i in attaches:
           # This example assumes the image is in the current directory
           fp       = open(i, 'rb')
           msgImage = MIMEImage(fp.read())
           fp.close()
   
           # Define the image's ID as referenced above
           i = ntpath.basename(i).split('.')[0]
        
           # We reference the image in the IMG SRC attribute by the ID we give it below
           msgImage.add_header('Content-ID', '<' + i + '>')
           msg.attach(msgImage)
           sImg += '<img src="cid:' + i + '"> '

       text += '<br><br>{img}'
       msg.attach(MIMEText(text.replace('{img}', sImg), 'html'))

   for attach in attaches:
       part = MIMEBase('application', 'octet-stream')
       part.set_payload(open(attach, 'rb').read())
       encoders.encode_base64(part)
       part.add_header('Content-Disposition',
               'attachment; filename="%s"' % os.path.basename(attach))
       msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

def clean(img):
    for i in img:
        os.remove(i)
