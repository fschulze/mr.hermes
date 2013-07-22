from email.mime.text import MIMEText
from email.parser import Parser
import os
import pytest


@pytest.fixture
def debugsmtp(request, tmpdir):
    from mr.hermes import DebuggingServer
    os.environ['DEBUG_SMTP_OUTPUT_PATH'] = str(tmpdir)
    debugsmtp = DebuggingServer(('localhost', 0), ('localhost', 0))
    request.addfinalizer(debugsmtp.close)
    return debugsmtp


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
