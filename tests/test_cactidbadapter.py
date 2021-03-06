# -*- coding: utf-8 -*-

"""UnitTests for cactidbadapter."""

import unittest
from cactidbadapter import CactiDBAdapter


class UnitTests(unittest.TestCase):

    """Class UnitTests.

    Unit test for cactidbadapter.

    """

    def setUp(self):
        """Setup."""
        self.obj = CactiDBAdapter(user='root',
                                  password='',
                                  host='localhost',
                                  port=3306)

    def test_attrs(self):
        """test cactidbadapter."""
        # check default values
        obj = CactiDBAdapter()

        self.assertEqual(obj.database, 'cacti')
        self.assertEqual(obj.user, 'root')
        self.assertEqual(obj.password, '')
        self.assertEqual(obj.host, 'localhost')
        self.assertEqual(obj.port, 3306)
        self.assertEqual(obj.charset, 'utf8mb4')

        # check specified values
        obj = CactiDBAdapter(user='admin',
                             password='password',
                             host='localhost',
                             database='aaaaa',
                             port=12345)

        self.assertEqual(obj.database, 'aaaaa')
        self.assertEqual(obj.user, 'admin')
        self.assertEqual(obj.password, 'password')
        self.assertEqual(obj.host, 'localhost')
        self.assertEqual(obj.port, 12345)
        self.assertEqual(obj.charset, 'utf8mb4')

    def test_get_host(self):
        """Get host from cacti db."""
        hostname = '127.0.0.1'

        hosts = self.obj.get_host()
        self.assertEqual(len(hosts), 3)
        self.assertEqual(hosts[0]['hostname'], hostname)

        hosts = self.obj.get_host(condition='hostname = "%s"' % hostname)
        self.assertEqual(hosts[0]['hostname'], hostname)

    def test_host_columns(self):
        """Check column values."""
        vals = self.obj.host_columns()
        self.assertEqual(type(vals), list)

    def test_host_snmp_cache_columns(self):
        """Check column values."""
        vals = self.obj.host_snmp_cache_columns()
        self.assertEqual(type(vals), list)

    def test_host_snmp_cache_field_names(self):
        """Check field_name values."""
        vals = self.obj.host_snmp_cache_field_names()
        self.assertEqual(type(vals), list)

    def test_get_snmp_cache(self):
        """Get fetched snmp values from cacti db."""
        condition = 'field_name = "ifindex"'
        vals = self.obj.get_snmp_cache(condition=condition)
        for val in vals:
            if val['field_value'] == '1':
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['field_name'], 'ifIndex')
                self.assertEqual(val['field_value'], '1')

        condition = 'field_name = "ifIP"'
        vals = self.obj.get_snmp_cache(condition=condition)
        for val in vals:
            if val['field_value'] == '10.0.2.15':
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['field_name'], 'ifIP')
                self.assertEqual(val['field_value'], '10.0.2.15')

        condition = 'field_name = "ifIP" or field_name = "ifName"'
        vals = self.obj.get_snmp_cache(condition=condition)
        for val in vals:
            if val['field_value'] == '10.0.2.15':
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['field_name'], 'ifIP')
                self.assertEqual(val['field_value'], '10.0.2.15')

            elif val['field_value'] == 'lo':
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['field_name'], 'ifName')
                self.assertEqual(val['field_value'], 'lo')

        # condition
        hostname = '127.0.0.1'
        condition = ('field_name = "ifIP"'
                     ' or field_name = "ifName"'
                     ' and hostname = "%s"' % hostname)
        vals = self.obj.get_snmp_cache(condition=condition)
        for val in vals:
            self.assertEqual(val['hostname'], hostname)

        # limit check
        condition = 'field_name = "ifIP"'
        vals = self.obj.get_snmp_cache(condition=condition, limit=1)
        self.assertEqual(len(vals), 1)

        vals = self.obj.get_snmp_cache(condition=condition, limit=2)
        self.assertEqual(len(vals), 2)

    def test_get_ifip(self):
        """Get fetched snmp ifIP values from cacti db."""
        vals = self.obj.get_ifip()
        for val in vals:
            if val['field_value'] == '127.0.0.1':
                self.assertEqual(val['id'], 1)
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['field_name'], 'ifIP')
                self.assertEqual(val['oid'],
                                 '.1.3.6.1.2.1.4.20.1.2.127.0.0.1')

            if val['field_value'] == '10.0.2.15':
                self.assertEqual(val['id'], 1)
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['field_name'], 'ifIP')
                self.assertEqual(val['oid'],
                                 '.1.3.6.1.2.1.4.20.1.2.10.0.2.15')

            if val['field_value'] == '192.168.56.2':
                self.assertEqual(val['id'], 1)
                self.assertEqual(val['hostname'], '127.0.0.1')
                self.assertEqual(val['description'], 'Localhost')
                self.assertEqual(val['field_name'], 'ifIP')
                self.assertEqual(val['oid'],
                                 '.1.3.6.1.2.1.4.20.1.2.192.168.56.2')

    def test_get_sysdescr(self):
        """Get fetched snmp sysDescr values from cacti db."""
        vals = self.obj.get_sysdescr()
        for val in vals:
            self.assertEqual(val['oid'], '.1.3.6.1.2.1.1.1.0')

    def test_get_sysobjectid(self):
        """Get fetched snmp sysObjectID values from cacti db."""
        vals = self.obj.get_sysobjectid()
        for val in vals:
            self.assertEqual(val['oid'], '.1.3.6.1.2.1.1.2.0')

    def test_get_sysuptime(self):
        """Get fetched snmp sysUpTime values from cacti db."""
        vals = self.obj.get_sysuptime()
        for val in vals:
            self.assertEqual(val['oid'], '.1.3.6.1.2.1.1.3.0')

    def test_get_syscontact(self):
        """Get fetched snmp sysContact values from cacti db."""
        vals = self.obj.get_syscontact()
        for val in vals:
            self.assertEqual(val['oid'], '.1.3.6.1.2.1.1.4.0')

    def test_get_sysname(self):
        """Get fetched snmp sysName values from cacti db."""
        vals = self.obj.get_sysname()
        for val in vals:
            self.assertEqual(val['oid'], '.1.3.6.1.2.1.1.5.0')

    def test_get_syslocation(self):
        """Get fetched snmp sysLocation values from cacti db."""
        vals = self.obj.get_syslocation()
        for val in vals:
            self.assertEqual(val['oid'], '.1.3.6.1.2.1.1.6.0')

    def test_get_sysservices(self):
        """Get fetched snmp sysServices values from cacti db."""
        vals = self.obj.get_sysservices()
        for val in vals:
            self.assertEqual(val['oid'], '.1.3.6.1.2.1.1.7.0')
