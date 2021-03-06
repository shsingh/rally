# Copyright (C) 2014 Yahoo! Inc. All Rights Reserved.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from rally import exceptions
from rally.plugins.common import types
from tests.unit import test


class PathOrUrlTestCase(test.TestCase):

    @mock.patch("os.path.isfile")
    @mock.patch("requests.head")
    def test_preprocess_file(self, mock_requests_head, mock_isfile):
        mock_isfile.return_value = True
        path = types.PathOrUrl({}, {}).pre_process("fake_path", {})
        self.assertEqual("fake_path", path)

    @mock.patch("os.path.isfile")
    @mock.patch("requests.head")
    def test_preprocess_bogus(self, mock_requests_head, mock_isfile):
        mock_isfile.return_value = False
        mock_requests_head.return_value = mock.Mock(status_code=500)
        self.assertRaises(exceptions.InvalidScenarioArgument,
                          types.PathOrUrl({}, {}).pre_process,
                          "fake_path", {})
        mock_requests_head.assert_called_once_with("fake_path", verify=False)

    @mock.patch("os.path.isfile")
    @mock.patch("requests.head")
    def test_preprocess_url(self, mock_requests_head, mock_isfile):
        mock_isfile.return_value = False
        mock_requests_head.return_value = mock.Mock(status_code=200)
        path = types.PathOrUrl({}, {}).pre_process("fake_url", {})
        self.assertEqual("fake_url", path)


class FileTypeTestCase(test.TestCase):

    @mock.patch("six.moves.builtins.open",
                side_effect=mock.mock_open(read_data="file_context"),
                create=True)
    def test_preprocess_by_path(self, mock_open):
        resource_spec = "file.yaml"
        file_context = types.FileType({}, {}).pre_process(resource_spec, {})
        self.assertEqual("file_context", file_context)

    @mock.patch("six.moves.builtins.open", side_effect=IOError, create=True)
    def test_preprocess_by_path_no_match(self, mock_open):
        resource_spec = "nonexistant.yaml"
        self.assertRaises(IOError,
                          types.FileType({}, {}).pre_process,
                          resource_spec=resource_spec,
                          config={})


class FileTypeDictTestCase(test.TestCase):

    @mock.patch("six.moves.builtins.open",
                side_effect=mock.mock_open(read_data="file_context"),
                create=True)
    def test_preprocess_by_path(self, mock_open):
        resource_spec = ["file.yaml"]
        file_context = types.FileTypeDict({}, {}).pre_process(resource_spec,
                                                              {})
        self.assertEqual({"file.yaml": "file_context"}, file_context)

    @mock.patch("six.moves.builtins.open", side_effect=IOError, create=True)
    def test_preprocess_by_path_no_match(self, mock_open):
        resource_spec = ["nonexistant.yaml"]
        self.assertRaises(IOError,
                          types.FileTypeDict({}, {}).pre_process,
                          resource_spec=resource_spec, config={})
