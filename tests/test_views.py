# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Module tests."""

from __future__ import absolute_import, print_function

from flask import Flask

from invenio_record_editor import InvenioRecordEditor


def test_save_view(app):
    """Test view."""

    json_data = {
        "pid_type": "literature",
        "recid": 1407739,
        "json_data": {}
        # "json_data": {
        #     "$schema": "http://localhost:5000/schemas/records/hep.json",
        #     "authors": [
        #         {
        #             "affiliations": [
        #                 {
        #                     "value": "NTUA"
        #                 },
        #                 {
        #                     "value": "Dubna Intl. Univ."
        #                 }
        #             ],
        #             "full_name": "Zahos",
        #             "ids": [
        #                 {
        #                     "type": "INSPIRE BAI",
        #                     "value": "E.V.Arbuzova.1"
        #                 }
        #             ],
        #             "uuid": "8c271f7b-3798-4dcf-94ce-b0d85c443a5f"
        #         }
        #     ]
        # }
    }

    InvenioRecordEditor(app)
    with app.test_client() as client:
        res = client.get("/editor/save")
        assert res.status_code == 405
        res = client.post(
            "/editor/save", content_type='application/json', data=json_data)
        assert res.status_code == 200
        assert res.data.status == "200"
