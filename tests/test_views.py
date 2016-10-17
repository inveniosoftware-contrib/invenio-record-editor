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
import pytest
import json
from invenio_pidstore.models import PersistentIdentifier as PI
from invenio_records.models import RecordMetadata as RM
from invenio_pidstore.errors import PIDAlreadyExists
from invenio_records.api import Record
from invenio_db import db as db_
from sqlalchemy_utils.functions import create_database, database_exists
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError


@pytest.yield_fixture()
def db(app):
    """Database fixture."""
    #import pdb
    #pdb.set_trace()
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    db_.create_all()
    yield db_
    db_.session.remove()
    db_.drop_all()


@pytest.fixture(scope='function')
def generate_data(app):
    schema = {
        "titles": {
            "items": {
                "type": "object",
                "properties": {
                    "value": "string"
                }
            },
            "type": "array",
        }
    }
    record_data = {
        "$schema": schema,
        "titles": [
            {
                "title": "Cosmic Antigravity ---------"
            }
        ]
    }
    json_data = {
        "pid_type": "testSaveView",
        "recid": 1,
        "json_data": record_data
    }

    # Create record in DB Record.create()
    # Create entry in PersistentIdentifier
    with app.app_context():

        record = Record.create(json_data)
        record_uuid = record
        db.session.commit()
        try:
            pid = PI.create(json_data["pid_type"], json_data[
                "recid"], object_uuid=record_uuid)
        except (PIDAlreadyExists, NoResultFound, SQLAlchemyError):
            pid = PI.get(json_data["pid_type"], json_data["recid"])
        db.session.commit()
    yield json_data

    # Delete record from DB
    # Delete entry in PersistentIdentifier
    record.delete(force=True)
    pid.delete()


def test_get_db_record(generate_data):
    pid = PI.get(generate_data["pid_type"], generate_data["recid"])
    rec = Record.get_record(pid.object_uuid)


# def test_save_view_does_not_accept_get_request(app, app_client):
#     res = app_client.get("/editor/save")
#     assert res.status_code == 405


# def test_save_view_valid_schema_data(app, app_client, generate_data):
#     res = app_client.post("/editor/save", data=json.dumps(generate_data))
#     res_data = json.loads(res.data)
#     assert res.status_code == 200
#     assert res_data["status"] == 200
#     assert res_data["message"] == "Record saved successfully"


# def test_save_view_invalid_schema_data(app, app_client, generate_data):
#     generate_data["json_data"]["authors"][
#         0]["affiliations"][0]["value"] = 0
#     res = app_client.post("/editor/save", data=json.dumps(generate_data))
#     res_data = json.loads(res.data)
#     assert res.status_code == 200
#     assert res_data["status"] == 500
#     assert res_data["errorMap"] == {
#         "authors.0.affiliations.0.value": [
#             {
#                 "message": "0 is not of type string"
#             }
#         ]
#     }


# def test_save_view_not_existing_data(app, app_client, generate_data):
#     generate_data["pid_type"] = "error"
#     res = app_client.post("/editor/save", data=json.dumps(generate_data))
#     res_data = json.loads(res.data)
#     assert res.status_code == 200
#     assert res_data["status"] == 404
#     assert res_data["message"] == "Record doesn't exist"
