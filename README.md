# Shinken deployment for b2g devices
This is a simple Shinken deployment for b2g devices (Currently in mtbf-4).

# Setting
To add a new host for monitoring, you should add two configuration files under /etc/shinken/hosts and /etc/shinken/services respectively.
For example,

    # /etc/shinken/hosts/YOUR_DEVICE_SERIAL.cfg
    define host {
        use             generic-service
        host_name       YOUR_DEVICE_SERIAL
        address         YOUR_IP_ADDRESS_OF_YOUR_DEVICE
    }

     # /etc/shinken/services/YOUR_DEVICE_SERIAL.cfg
    define service {
        service_description           Flame
        check_command                 passive_check_lab_device!2!"Warning: No checks received from the remote currently."
        host_name                     YOUR_DEVICE_SERIAL
        flap_detection_enabled        0
        event_handler_enabled         0
        use                           check_passive_26h_24x7, notify_24x7
    }

After adding new configuration files, you should reload/restart Shinken service.

# Running the monitoring service
Let the monitor.py run periodically on your client machine (Currently in moztwlab-01). The following variables should be set correctly,

    SUCCESS_LOG_PATH = ''
    SERVER_URL = ''
    USERNAME = ''
    PASSWORD = ''

# Reference
* http://www.unixmen.com/how-to-monitor-linux-clients-using-shinken/
* http://www.admin-magazine.com/Archive/2014/22/Nagios-Passive-Checks
