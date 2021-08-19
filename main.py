import configparser
import argparse
import requests
import time
from smtplib import SMTP_SSL
from email.message import EmailMessage

def parse_args(config_file):
  config = configparser.ConfigParser(
    defaults = { 'helper':  'https://api.ipify.org',
                 'server':  'smtp.yandex.ru',
                 'port':    '0',
                 'user':    'user',
                 'pass':    '',
                 'sender':  'user@yandex.ru',
                 'sendto':  'user@yandex.ru',
                 'subject': 'IP monitor',
                 'delay':   '30',
                 'notify':  '6000' })

  config.read(config_file)
  
  cfg = config['DEFAULT']

  parser = argparse.ArgumentParser(
    prog = 'ip-monitor',
    description = 'Public IP address monitoring'
  )

  parser.add_argument(
    '--ip-helper',
    type = str,
    metavar = 'URL',
    default = cfg.get('helper'),
    help = 'public IP service provider',
    dest = 'ip_helper'
  )

  parser.add_argument(
    '--server',
    type = str,
    metavar = 'URL',
    default = cfg.get('server'),
    help = 'SMTP server address',
    dest = 'smtp_server'
  )

  parser.add_argument(
    '--port',
    type = int,
    metavar = 'PORT',
    default = cfg.get('port'),
    help = 'SMTP server port',
    dest = 'smtp_port'
  )

  parser.add_argument(
    '--user',
    type = str,
    metavar = 'NAME',
    default = cfg.get('user'),
    help = 'SMTP username',
    dest = 'smtp_user'
  )

  parser.add_argument(
    '--pass',
    type = str,
    metavar = '****',
    default = cfg.get('pass'),
    help = 'SMTP password',
    dest = 'smtp_pass'
  )

  parser.add_argument(
    '--sender',
    type = str,
    metavar = 'EMAIL',
    default = cfg.get('sender'),
    help = 'sender email address',
    dest = 'sender'
  )

  parser.add_argument(
    '--sendto',
    type = str,
    metavar = 'EMAIL',
    default = cfg.get('sendto'),
    help = 'where to send notifications',
    dest = 'sendto'
  )

  parser.add_argument(
    '--subject',
    type = str,
    metavar = 'TITLE',
    default = cfg.get('subject'),
    help = 'notification email subject',
    dest = 'subject'
  )

  parser.add_argument(
    '--delay',
    type = int,
    metavar = 'TIME',
    default = cfg.get('delay'),
    help = 'IP check delay in seconds',
    dest = 'delay'
  )

  parser.add_argument(
    '--notify',
    type = int,
    metavar = 'TIME',
    default = cfg.get('notify'),
    help = 'email notification timeout in seconds',
    dest = 'notify'
  )

  return parser.parse_args()

def send_notification(
  smtp_url: str,
  smtp_port: int,
  user: str,
  password: str,
  sender: str,
  sendto: str,
  subject: str,
  ip: str
):
  msg = EmailMessage()
  msg.set_content(ip)
  msg['Subject'] = subject
  msg['From'] = sender
  msg['To'] = sendto

  with SMTP_SSL(smtp_url, smtp_port) as smtp:
    smtp.login(user, password)
    smtp.send_message(msg, sender, sendto)

args = parse_args('ip-monitor.ini')

a_helper  = args.ip_helper
a_smtp    = args.smtp_server
a_port    = args.smtp_port;
a_user    = args.smtp_user
a_pass    = args.smtp_pass
a_sender  = args.sender;
a_sendto  = args.sendto;
a_subject = args.subject;
a_delay   = args.delay
a_notify  = args.notify

address     = ''
addr_new    = ''
time_check  = 0
time_notify = 0

while True:
  if time_check <= 0:
    try:
      addr_new   = requests.get(a_helper).text
      time_check = a_delay

      if addr_new != address or time_notify <= 0:
        send_notification(
          a_smtp, a_port, a_user, a_pass,
          a_sender, a_sendto, a_subject,
          addr_new
        )

        address     = addr_new
        time_notify = a_notify

    except Exception:
      ...

  time_check -= 1
  time_notify -= 1
  time.sleep(1)
