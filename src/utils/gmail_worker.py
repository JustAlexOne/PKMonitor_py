#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE

import itertools
import requests
import smtplib

import time

import sys

url_search_tickets = 'http://booking.uz.gov.ua/purchase/search/'
url_station_id = 'http://booking.uz.gov.ua/purchase/station/?term='

form_data = {
    'station_id_from': '2210690',
    'station_id_till': '2204001',
    'station_from': 'Бердянськ',
    'station_till': 'Харків',
    'date_dep': '13.08.2017',
    'time_dep': '00:00',
    'time_dep_till': '',
    'another_ec': 0,
    'search': '',
}

global temp_text1
global temp_text2
global recipients
global creds
global gmail_server
gmail_server = None

mins_wait = 10
trains = 1
old_places = {}


def send_email(to_addrs, subject, body):
    print('sending email')
    global gmail_server
    gmail_server = gmail_server

    if not gmail_server:
        login_to_gmail('ukrnat19@gmail.com', 'ukrnat1991')

    # Send the mail
    msg = create_msg('ukrnat19@gmail.com', to_addrs, subject, body)
    gmail_server.sendmail('ukrnat19@gmail.com', to_addrs, msg.as_string())
    print('email sent!')


def create_msg(from_addr, to_addrs, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = str(to_addrs)
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
    return msg


def login_to_gmail(login, password):
    global gmail_server
    gmail_server = smtplib.SMTP('smtp.gmail.com', 587)
    # Next, log in to the server
    gmail_server.starttls()
    gmail_server.login(login, password)

def create_msg_text(new, body):
    res = ''
    if body:
        res = body
    else:
        res = f'New:\n{new}\nOld:\n{old_places}\n'
    res = res + '\nCheck it out: http://booking.uz.gov.ua/'
    return res




if __name__ == '__main__':
    creds = ('ukrnat19@gmail.com', 'ukrnat1991')
    recipients = [
        creds[0],
        'alex.cherevatiy@gmail.com',
    ]