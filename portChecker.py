from threading import Timer
from datetime import datetime
import qbittorrentapi
import os
import sys

portTimer = None

# The qBitorrent WebUI needs to be enabled for this script to work
host = os.getenv('QBITTORRENT_HOST', '')
port = os.getenv('QBITTORRENT_PORT', '')
username = os.getenv('QBITTORRENT_USERNAME', '')
password = os.getenv('QBITTORRENT_PASSWORD', '')

# How often the port is checked in seconds
updateTime = os.getenv('QBITTORRENT_UPDATE_TIME_SECONDS', 60)
portFileName = os.getenv('PIA_PORT_FILE_NAME', '')

def log(message):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + str(message))

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def set_port_in_qbt(pia_port):
    qbt_client = qbittorrentapi.Client(
        host=host, port=port, username=username, password=password)
    
    try:
        qbt_client.auth_log_in()
        log("Logged into qBittorrent!")
    except:
        e = sys.exc_info()[0]
        log("Error: %s" % e)
        log("qBittorrent probably isn't running or the credentials are incorrect.")
        log(host)
        log(port)
        log(username)
        log(password)
        sys.exit()
    
    prefs = qbt_client.application.preferences
    prefs['listen_port'] = pia_port
    qbt_client.app.preferences = prefs


def get_port_from_pia():
    log("Checking port...")
    with open('/pia_port/' + portFileName, 'r') as file:
        file_contents = file.readline().strip()
        log("PIA port: " + file_contents)
        if (file_contents != '' and file_contents.isnumeric()):
            return int(file_contents)
        else:
            log("Error: Port file is empty or not a number.")
            return None
    
    
def run():
    pia_port = get_port_from_pia()
    
    if pia_port is not None:
        set_port_in_qbt(pia_port)
        log("Port set to: " + str(pia_port))
    
def main():
    global portTimer
    
    if not host or not port or not username or not password or not portFileName:
        log("Missing environment variables. Please set the following variables:")
        log("QBITTORRENT_HOST")
        log("QBITTORRENT_PORT")
        log("QBITTORRENT_USERNAME")
        log("QBITTORRENT_PASSWORD")
        log("PIA_PORT_FILE_NAME")
        sys.exit()

    run()
    portTimer = RepeatedTimer(int(updateTime), run)


if __name__ == "__main__":
    main()