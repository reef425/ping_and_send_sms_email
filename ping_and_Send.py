import datetime
import socket
import sys
import time

#импортируем библиотеку для работы с почтой
import smtplib
from email.MIMEText import MIMEText

# Получаем IP и порт для пинга
host = raw_input('Хост:')
port = raw_input('Порт:')

#состояние хоста
HOST_UP=1
HOST_DOWN=2


def send_mail(status_msg):


# с какого ящика отправлять сообщение
      me = 'your_mail@gmail.com'
# на какой ящик получать.
      you = 'your_mail_for_messages@gmail.com'

# формат текста письма
      text =  timestamp+'  '+ host + ':'  + status_msg
# формат заголовка письма
      subj = status_msg + host
# параметры SMTP-сервера
      server = "smtp.gmail.com"
      port = 587
      user_name = "your_mail"
      user_passwd = "your_password"
# формирование сообщения
      msg = MIMEText(text, "", "utf-8")
      msg['Subject'] = subj
      msg['From'] = me
      msg['To'] = you
# отправка e-mail
      s = smtplib.SMTP(server, port)
#debuglevel(1) покажет отладку отправки сообщения.
      s.set_debuglevel(0)
      s.ehlo()
      s.starttls()
      s.login(user_name, user_passwd)
      s.sendmail(me, you, msg.as_string())
      print "Отчёт отправлен!"
      s.quit()


# Проверяем правильно ли написан порт
if not port.isalnum():
    print 'Введите правильно порт'
    sys.exit(1)

status=None
status_changed=False

while 1:
# Получаем дату и время
    d = datetime.datetime.now()
    timestamp = d.strftime("%Y-%m-%d %H:%M:%S")
# Создаем сокет
    s = socket.socket()
    s.settimeout(1)
# Если пропало или появилось соединение, то будет отправлено сообщение.
    try:
        s.connect((host, int(port)))
    except socket.error:
        if status != HOST_DOWN:
            status_changed = True
        status = HOST_DOWN
        status_msg=' Offline'
    else:
        s.close
        if status != HOST_UP:
            status_changed = True
        status = HOST_UP
        status_msg=' Online'
        print timestamp+'  '+ host + ':' + port + ' - Активен'

    if status_changed:
        send_mail(status_msg)
        status_changed = False

#задержка перед пингом 60 секунд
    time.sleep(60)
