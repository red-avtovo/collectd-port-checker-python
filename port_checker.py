# collectd-port-checker-python
# ========================
#
# Python-based plugin to check ports status and send it to collectd
#
# https://github.com/deniszh/collectd-activemq-python - was used as inspiration
# http://stackoverflow.com/questions/27834815/how-to-run-multiple-instances-of-python-plugin-in-collectd - was used
# as the template
import socket

CONFIGS = []
plugin_name = "port_checker"


def configure_standalone(host='localhost', port=0, verbose_logging=False):
    host = host
    port = port
    verbose_logging = verbose_logging
    CONFIGS.append({
        'host': host,
        'port': port,
        'verbose_logging': verbose_logging
    })


def log_verbose(verbose_logging, msg):
    if not verbose_logging:
        return
    elif __name__ == '__main__':
        print msg
    else:
        collectd.info('%s plugin [verbose]: %s' % (plugin_name, msg))


def configure_callback(conf):
    """Receive configuration block"""
    host = ""
    port = "80"
    verbose_logging = False
    for node in conf.children:
        if node.key == 'Host':
            host = node.values[0]
        elif node.key == 'Port':
            port = int(node.values[0])
        elif node.key == 'Verbose_logging':
            verbose_logging = node.values[0]
        else:
            collectd.warning('%s plugin: Unknown config key: %s.' % (plugin_name, node.key))
    log_verbose(verbose_logging, 'Configured with host=%s, port=%s' % (
        host, port))
    CONFIGS.append({
        'host': host,
        'port': port,
        'verbose_logging': verbose_logging
    })
    log_verbose(verbose_logging, 'configs: %s' % CONFIGS)


def dispatch_value(verbose_logging, plugin_instance, value_type, instance, value):
    """Dispatch a value to collectd"""
    log_verbose(verbose_logging, 'Sending value: %s.%s.%s=%s' % (plugin_name, plugin_instance, instance, value))
    if __name__ == "__main__":
        return
    val = collectd.Values()
    val.plugin = plugin_name
    val.plugin_instance = plugin_instance
    val.type = value_type
    val.type_instance = instance
    val.values = [value, ]

    val.dispatch()


def fetch_metrics(conf):

    gauges = []
    counters = []
    coded_name = conf['host'].replace(".", "_") + "__" + str(conf['port'])
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((conf['host'], conf['port']))
            s.shutdown(2)
            s.close()
            log_verbose(conf['verbose_logging'], "Success in connecting to listener at")
            log_verbose(conf['verbose_logging'], '%s on port: %s' % (conf['host'], str(conf['port'])))
            gauges.append((coded_name, 'status', 1))
            counters.append((coded_name, 'status', 1))
        except:
            log_verbose(conf['verbose_logging'], "Error can't connect to listener ")
            log_verbose(conf['verbose_logging'], '%s on port: %s' % (conf['host'], str(conf['port'])))
            gauges.append((coded_name, 'status', 0))
            counters.append((coded_name, 'status', 0))

    except Exception:
        log_verbose(conf['verbose_logging'], '%s plugin: No info received, offline node' % plugin_name)
        return

    metrics = {
        'gauges': gauges,
        'counters': counters,
    }
    return metrics


def read_callback():
    for config in CONFIGS:
        """Collectd read callback"""
        log_verbose(config['verbose_logging'], 'Read callback called')
        metrics = fetch_metrics(config)
        if metrics is None:
            log_verbose(config['verbose_logging'], 'No metrics returned.')
            return

        for gauge in metrics['gauges']:
            dispatch_value(config['verbose_logging'], gauge[0], 'gauge', gauge[1], gauge[2])

        for counter in metrics['counters']:
            dispatch_value(config['verbose_logging'], counter[0], 'counter', counter[1], counter[2])


if __name__ == "__main__":
    import argparse

    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('host')
        parser.add_argument('port')
        parser.add_argument('-v', '--verbose-logging', default=False)

        return parser.parse_args()


    args = parse_args()
    configure_standalone(args.host, args.port, args.verbose_logging)
    read_callback()

else:
    import collectd

    collectd.register_config(configure_callback)
    collectd.register_read(read_callback)
