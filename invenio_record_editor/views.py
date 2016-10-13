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
import json
from jsonschema import ValidationError,Draft4Validator
from flask import Blueprint, render_template,request,jsonify
from invenio_db import db
from invenio_indexer.api import RecordIndexer
from inspirehep.utils.record_getter import get_db_record,RecordGetterError

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

@blueprint.route("/editor/save" , methods = ['POST'])
def save():
	"""Save endpoint"""
	data = request.json
	pid_type = data['category']
	recid = data['recid']
	json_data = data['json_data']
	try:
		record = get_db_record(pid_type,recid)
		if record:
			record.update(json_data)
			#record.validate(validator=Draft4Validator)
			record.commit()
			ri = RecordIndexer()
			ri.index(record)
	except (RecordGetterError,ValidationError) as e:
		return jsonify({"message":e.message,
						"relative_path" : list(e.relative_path)})

	db.session.commit()
	return jsonify({"message":"success"})
