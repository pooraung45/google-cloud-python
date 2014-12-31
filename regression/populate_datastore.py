# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script to populate datastore with regression test data."""

from six.moves import zip

from gcloud import datastore
# This assumes the command is being run via tox hence the
# repository root is the current directory.
from regression import regression_utils


ANCESTOR = ('Book', 'GoT')
RICKARD = ANCESTOR + ('Character', 'Rickard')
EDDARD = RICKARD + ('Character', 'Eddard')
KEY_PATHS = [
    RICKARD,
    EDDARD,
    ANCESTOR + ('Character', 'Catelyn'),
    EDDARD + ('Character', 'Arya'),
    EDDARD + ('Character', 'Sansa'),
    EDDARD + ('Character', 'Robb'),
    EDDARD + ('Character', 'Bran'),
    EDDARD + ('Character', 'Jon Snow'),
]
CHARACTERS = [
    {
        'name': u'Rickard',
        'family': u'Stark',
        'appearances': 0,
        'alive': False,
    }, {
        'name': u'Eddard',
        'family': u'Stark',
        'appearances': 9,
        'alive': False,
    }, {
        'name': u'Catelyn',
        'family': [u'Stark', u'Tully'],
        'appearances': 26,
        'alive': False,
    }, {
        'name': u'Arya',
        'family': u'Stark',
        'appearances': 33,
        'alive': True,
    }, {
        'name': u'Sansa',
        'family': u'Stark',
        'appearances': 31,
        'alive': True,
    }, {
        'name': u'Robb',
        'family': u'Stark',
        'appearances': 22,
        'alive': False,
    }, {
        'name': u'Bran',
        'family': u'Stark',
        'appearances': 25,
        'alive': True,
    }, {
        'name': u'Jon Snow',
        'family': u'Stark',
        'appearances': 32,
        'alive': True,
    },
]


def add_characters():
    dataset = regression_utils.get_dataset()
    with dataset.transaction():
        for key_path, character in zip(KEY_PATHS, CHARACTERS):
            if key_path[-1] != character['name']:
                raise ValueError(('Character and key don\'t agree',
                                  key_path, character))
            key = datastore.key.Key(*key_path, dataset_id=dataset.id())
            entity = datastore.entity.Entity(dataset=dataset).key(key)
            entity.update(character)
            entity.save()
            print('Adding Character %s %s' % (character['name'],
                                              character['family']))


if __name__ == '__main__':
    add_characters()
