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

"""Invenio module for editing JSON records."""

from __future__ import absolute_import, print_function
from jsonschema import ValidationError
from flask import Blueprint, render_template, request, jsonify
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from inspirehep.utils.record_getter import get_db_record, RecordGetterError

blueprint = Blueprint(
    'invenio_record_editor',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.route("/")
def index():
    """Basic view."""
    return render_template(
        "invenio_record_editor/index.html",
        module_name='Invenio-RecordEditor')


@blueprint.route("/editor/save", methods=['POST'])
def save():
    """Save endpoint."""
    data = request.json
    # Maybe raise an error if json hasn't the required fields
    pid_type = data.get('pid_type', "")
    recid = data.get('recid', 0)
    json_data = data.get('json_data', {})
    try:
        record = get_db_record(pid_type, recid)
        if record:
            record.update(json_data)
            record.commit()
            ri = RecordIndexer()
            ri.index(record)
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "Record saved successfully"
            })

    except ValidationError as e:
        rel_path = list(e.relative_path)
        msg = '.'.join(str(item) for item in rel_path)
        return jsonify({
            "status": 500,
            "errorMap": {
                msg: [{
                    "message": e.message.replace('u\'', '').replace('\'', '')
                }]
            }
        })
    except RecordGetterError:
        return jsonify({
            "status": 404,
            "message": "Record doesn't exist",

        })
