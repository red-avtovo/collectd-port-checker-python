collectd-port-checker-python
========================

Python-based plugin to get port status and send it to [collectd](http://collectd.org)

Data captured includes:

 * Port status

[deniszh's Python ActiveMQ collectd plugin] (https://github.com/deniszh/collectd-activemq-python) - as inspiration.

Install
-------
 1. Place soap_info.py in /usr/lib/collectd/plugins/python
 2. Configure the plugin (see below).
 3. Restart collectd.

Configuration
-------------
Add the following to your collectd config

    <LoadPlugin python>
      Globals true
    </LoadPlugin>

    <Plugin python>
      ModulePath "/usr/lib/collectd/plugins/python"
      Import "port_checker"

      <Module port_checker>
        Host "localhost"
        Port "8080"
      </Module>
    </Plugin>

_It will try to create a socket connection to `<host>:<port>`_

Dependencies
------------
None

License
-------

[MIT](http://mit-license.org/)