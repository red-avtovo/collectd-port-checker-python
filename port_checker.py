# collectd-port-checker-python
# ========================
#
# Python-based plugin to check ports status and send it to collectd
#
# https://github.com/deniszh/collectd-activemq-python - was used as inspiration

import socket


class PortMonitor(object):
    def __init__(self, plugin_name='port_checker', host='localhost', port=0,
                 verbose_logging=False):
        self.plugin_name = plugin_name
        self.host = host
        self.port = port
        self.verbose_logging = verbose_logging

    def log_verbose(self, msg):
        if not self.verbose_logging:
            return
        elif __name__ == '__main__':
            print msg
        else:
            collectd.info('%s plugin [verbose]: %s' % (self.plugin_name, msg))

    def configure_callback(self, conf):
        """Receive configuration block"""
        for node in conf.children:
            if node.key == 'Host':
                self.host = node.values[0]
            elif node.key == 'Port':
                self.port = int(node.values[0])
            else:
                collectd.warning('%s plugin: Unknown config key: %s.' % (self.plugin_name, node.key))
        self.log_verbose('Configured with host=%s, port=%s' % (
            self.host, self.port))

    def dispatch_value(self, plugin_instance, value_type, instance, value):
        """Dispatch a value to collectd"""
        self.log_verbose('Sending value: %s.%s.%s=%s' % (self.plugin_name, plugin_instance, instance, value))
        if __name__ == "__main__":
            return
        val = collectd.Values()
        val.plugin = self.plugin_name
        val.plugin_instance = plugin_instance
        val.type = value_type
        val.type_instance = instance
        val.values = [value, ]

        val.dispatch()

    def fetch_metrics(self):
        """Connect to SOAP-service and return DOM object"""

        gauges = []
        counters = []
        coded_name = self.host.replace(".", "_") + "__" + str(self.port)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((self.host, self.port))
                s.shutdown(2)
                self.log_verbose("Success in connecting to listener at")
                self.log_verbose('%s on port: %s' % (self.host, str(self.port)))
                gauges.append((coded_name, 'status', 1))
                counters.append((coded_name, 'status', 1))
            except:
                self.log_verbose("Error can't connect to listener ")
                self.log_verbose('%s on port: %s' % (self.host, str(self.port)))
                gauges.append((coded_name, 'status', 0))
                counters.append((coded_name, 'status', 0))

        except Exception:
            self.log_verbose('%s plugin: No info received, offline node' % self.plugin_name)
            return

        metrics = {
            'gauges': gauges,
            'counters': counters,
        }
        return metrics

    def read_callback(self):
        """Collectd read callback"""
        self.log_verbose('Read callback called')
        metrics = self.fetch_metrics()
        if metrics is None:
            self.log_verbose('No metrics returned.')
            return

        for gauge in metrics['gauges']:
            self.dispatch_value(gauge[0], 'gauge', gauge[1], gauge[2])

        for counter in metrics['counters']:
            self.dispatch_value(counter[0], 'counter', counter[1], counter[2])


if __name__ == "__main__":
    import argparse

    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('host')
        parser.add_argument('port')

        return parser.parse_args()


    args = parse_args()
    amq = PortMonitor(host=args.host, port=int(args.port),
                      verbose_logging=True)
    amq.read_callback()

else:
    import collectd

    amq = PortMonitor()
    # register callbacks
    collectd.register_config(amq.configure_callback)
    collectd.register_read(amq.read_callback)
