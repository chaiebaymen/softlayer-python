"""
    SoftLayer.tests.managers.ssl_tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT, see LICENSE for more details.
"""
from SoftLayer import SSLManager
from SoftLayer.tests import TestCase, FixtureClient

from mock import ANY


class SSLTests(TestCase):

    def set_up(self):
        self.client = FixtureClient()
        self.ssl = SSLManager(self.client)
        self.test_id = 10

    def test_list_certs(self):
        self.ssl.list_certs('valid')
        f = self.client['Account'].getValidSecurityCertificates
        f.assert_called_once_with(mask=ANY)

        self.ssl.list_certs('expired')
        f = self.client['Account'].getExpiredSecurityCertificates
        f.assert_called_once_with(mask=ANY)

        self.ssl.list_certs('all')
        f = self.client['Account'].getSecurityCertificates
        f.assert_called_once_with(mask=ANY)

    def test_add_certificate(self):
        test_cert = {
            'certificate': 'cert',
            'privateKey': 'key',
        }

        self.ssl.add_certificate(test_cert)

        f = self.client['Security_Certificate'].createObject
        f.assert_called_once_with(test_cert)

    def test_remove_certificate(self):
        self.ssl.remove_certificate(self.test_id)
        f = self.client['Security_Certificate'].deleteObject
        f.assert_called_once_with(id=self.test_id)

    def test_edit_certificate(self):
        test_cert = {
            'id': self.test_id,
            'certificate': 'cert',
            'privateKey': 'key'
        }

        self.ssl.edit_certificate(test_cert)
        f = self.client['Security_Certificate'].editObject
        f.assert_called_once_with(
            {
                'id': self.test_id,
                'certificate': 'cert',
                'privateKey': 'key'
            },
            id=self.test_id)

    def test_get_certificate(self):
        self.ssl.get_certificate(self.test_id)
        f = self.client['Security_Certificate'].getObject
        f.assert_called_once_with(id=self.test_id)
