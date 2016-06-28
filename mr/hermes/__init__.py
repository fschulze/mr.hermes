import os
import smtpd
import sys
import time


class DebuggingServer(smtpd.DebuggingServer):
    def __init__(self, localaddr, remoteaddr, *args, **kwargs):
        self.path = os.environ.get('DEBUG_SMTP_OUTPUT_PATH')
        if self.path is None:
            print >>sys.stderr, "DEBUG_SMTP_OUTPUT_PATH not set, dumping mails to stdout only."
        smtpd.DebuggingServer.__init__(
            self, localaddr, remoteaddr, *args, **kwargs)

    def process_message(self, peer, mailfrom, rcpttos, data):
        smtpd.DebuggingServer.process_message(self, peer, mailfrom, rcpttos, data)
        sys.stdout.flush()
        if self.path is None:
            return
        filename = time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time()))
        for addr in rcpttos:
            path = os.path.join(self.path, addr)
            if not os.path.exists(path):
                os.makedirs(path)
            dest = os.path.join(path, "%s.eml" % filename)
            index = 1
            while os.path.exists(dest):
                if index > 1000:
                    raise IOError("Tried too many filenames like: %s" % dest)
                dest = os.path.join(path, "%s_%s.eml" % (filename, index))
                index = index + 1
            with open(dest, "w") as f:
                f.write(data)
