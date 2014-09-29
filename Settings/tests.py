from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from django.test import TestCase
from django.db import connections
import os
import json

from ScenarioCreator.views import workspace_path
from Settings.utils import close_all_connections


class ScenarioTestCase(TestCase):
    multi_db = True

    def remove_test_file(self, file_path):
        try:
            os.remove(file_path)
        except:
            pass

    def test_post_success(self):
        file_name = 'Test Scenario 123 AZ'
        file_path = workspace_path(file_name) + '.sqlite3'

        self.remove_test_file(file_path)

        r = self.client.post('/app/SaveScenario/', {'filename': file_name})

        try:
            self.assertEqual(r.status_code, 302)
            self.assertTrue(os.path.isfile(file_path))
        finally:
            self.remove_test_file(file_path)

    def test_post_failure(self):
        file_name = 'Test \/ Scenario 123 AZ' # this should break Windows and Linux
        file_path = workspace_path(file_name) + '.sqlite3'

        self.remove_test_file(file_path)

        r = self.client.post('/app/SaveScenario/', {'filename': file_name})

        try:
            self.assertEqual(r.status_code, 302)
            self.assertFalse(os.path.isfile(file_path))
        finally:
            self.remove_test_file(file_path)

    def test_post_failure_ajax(self):
        file_name = 'Test \/ Scenario 123 AZ' # this should break Windows and Linux
        file_path = workspace_path(file_name) + '.sqlite3'

        self.remove_test_file(file_path)

        r = self.client.post('/app/SaveScenario/',
                             {'filename': file_name},
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        try:
            data = json.loads(r.content)
            self.assertIn('status', data)
            self.assertEqual(data['status'], 'failed')
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Failed to save file.')
            self.assertFalse(os.path.isfile(file_path))
        finally:
            self.remove_test_file(file_path)


class UtilsTestCase(TestCase):
    multi_db = True

    def test_close_all_connections(self):
        for conn in connections:
            connections[conn].ensure_connection()

        close_all_connections()

        for conn in connections:
            self.assertEqual(connections[conn].connection, None)
