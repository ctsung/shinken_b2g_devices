from b2g_util.check_versions import *
from os import listdir
from os.path import isfile, join
import pycurl
import time


SUCCESS_LOG_PATH = ''
SERVER_URL = ''
USERNAME = ''
PASSWORD = ''


class DeviceMonitor:
    def __init__(self):
        self.devices = None
        self.success_logs = None

    def get_device_list(self):
        return AdbWrapper.adb_devices()

    def get_success_log_list(self):
        return [file[6:14] for file in listdir(SUCCESS_LOG_PATH)
                if '.success' in file and isfile(join(SUCCESS_LOG_PATH, file))]

    def diff_device_success_log(self):
        unsuccess_device_list = []

        self.devices = self.get_device_list()
        self.success_logs = self.get_success_log_list()

        for device in self.devices:
            if device not in self.success_logs:
                unsuccess_device_list.append(device)

        return unsuccess_device_list

    def post_device_info(self, device_list, status):
        curl = pycurl.Curl()
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.URL, str(SERVER_URL))
        curl.setopt(pycurl.USERPWD, "%s:%s" % (str(USERNAME), str(PASSWORD)))

        if status == 0:
            output = 'Looks good!'
        elif status == 2:
            output = 'Seems like there are some problems.'

        for device in device_list:
            curl.setopt(pycurl.POSTFIELDS, "time_stamp=" + str(time.time())
                        + "&host_name=" + device
                        + "&service_description=Flame"
                        + "&return_code=" + str(status)
                        + "&output=" + output)
            curl.setopt(pycurl.USERPWD, "%s:%s" % (str(USERNAME), str(PASSWORD)))
            curl.perform()


if __name__ == '__main__':
    monitor = DeviceMonitor()
    success_device_list = monitor.get_success_log_list()
    unsuccess_device_list = monitor.diff_device_success_log()

    monitor.post_device_info(success_device_list, 0)
    monitor.post_device_info(unsuccess_device_list, 2)
