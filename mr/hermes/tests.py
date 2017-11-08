# coding: utf-8
from email.mime.text import MIMEText
from email.parser import Parser
import os
import pytest


@pytest.fixture
def debugsmtp(request, tmpdir):
    from mr.hermes import DebuggingServer
    debugsmtp = DebuggingServer(('localhost', 0), ('localhost', 0))
    debugsmtp.path = str(tmpdir)
    yield debugsmtp
    debugsmtp.close()


@pytest.fixture
def debugsmtp_thread(debugsmtp):
    import asyncore
    import threading
    thread = threading.Thread(
        target=asyncore.loop,
        kwargs=dict(
            timeout=1))
    thread.start()
    yield thread
    debugsmtp.close()
    thread.join()


@pytest.fixture
def sendmail(debugsmtp, debugsmtp_thread):
    def sendmail(msg):
        import smtplib
        (host, port) = debugsmtp.socket.getsockname()[:2]
        s = smtplib.SMTP(host, port)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
    return sendmail


@pytest.fixture
def email_msg():
    msg = MIMEText(u'Söme text', 'plain', 'utf-8')
    msg['Subject'] = 'Testmail'
    msg['From'] = 'sender@example.com'
    msg['To'] = 'receiver@example.com'
    return msg


def test_mails_filename_order(debugsmtp):
    me = 'bar@example.com'
    you = 'foo@example.com'
    for i in range(10):
        msg = MIMEText('Mail%02i.' % i)
        msg['Subject'] = 'Test'
        msg['From'] = me
        msg['To'] = you
        debugsmtp.process_message(('localhost', 0), me, [you], msg.as_string())
    mail_content = []
    path = os.path.join(debugsmtp.path, 'foo@example.com')
    for filename in os.listdir(path):
        with open(os.path.join(path, filename)) as f:
            msg = Parser().parsestr(f.read())
            mail_content.append(msg.get_payload())
    assert mail_content == [
        'Mail00.', 'Mail01.', 'Mail02.', 'Mail03.', 'Mail04.',
        'Mail05.', 'Mail06.', 'Mail07.', 'Mail08.', 'Mail09.']


def test_functional(sendmail, email_msg, tmpdir):
    sendmail(email_msg)
    (receiver,) = tmpdir.listdir()
    assert receiver.basename == 'receiver@example.com'
    (email_path,) = receiver.listdir()
    assert email_path.basename.endswith('.eml')
    with email_path.open() as f:
        email = Parser().parsestr(f.read())
    body = email.get_payload(decode=True)
    body = body.decode(email.get_content_charset())
    assert email['Subject'] == 'Testmail'
    assert email['From'] == 'sender@example.com'
    assert email['To'] == 'receiver@example.com'
    assert u'Söme text' in body
