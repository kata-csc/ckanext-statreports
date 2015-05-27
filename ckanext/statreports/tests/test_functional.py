import unittest
import commands

from pylons import config

from ckanext.statreports import email_template

class TestReport(unittest.TestCase):
    '''Test full report'''

    def test_report(self):
        cmd = 'paster --plugin=ckanext-statreports %s --config=%s' % \
              ('reporter report', config['__file__'])

        (status, output) = commands.getstatusoutput(cmd)

        assert not status
        assert output
        assert email_template.footer in output, output
