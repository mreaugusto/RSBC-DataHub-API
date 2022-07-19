from flask import Blueprint
from flask.cli import with_appcontext
import pytz
from datetime import datetime
import click
import logging
from python.prohibition_web_svc.models import db as database, Form, User, UserRole

bp = Blueprint('rsbc', __name__)


@bp.cli.command('create_db')
@with_appcontext
def create_db():
    database.create_all()


@bp.cli.command('seed_form_ids')
@with_appcontext
def seed_form_ids():
    seed_records = []
    prefix = ["JZ", "VZ", "40", "22"]
    for idx, form_type in enumerate(["12Hour", "24Hour", "IRP", "VI"]):
        for x in range(100000, 100100):
            unique_id = '{}{}'.format(prefix[idx], str(x))
            seed_records.append(Form(
                form_id=unique_id,
                form_type=form_type))
    database.session.bulk_save_objects(seed_records)
    database.session.commit()
    print("SUCCESS: seed temporary unique form_ids")


@bp.cli.command('seed_administrator')
@click.argument('admin_username')
@with_appcontext
def seed_initial_administrator(admin_username):
    vancouver_tz = pytz.timezone("America/Vancouver")
    current_dt = datetime.now(vancouver_tz)
    user = User(user_guid=admin_username,
                badge_number='0000',
                agency="RoadSafety",
                first_name="Initial",
                last_name="Administrator",
                business_guid="IDIR")
    database.session.add(user)
    roles = [
        UserRole(user_guid=admin_username, role_name='officer', submitted_dt=current_dt, approved_dt=current_dt),
        UserRole(user_guid=admin_username, role_name='administrator', submitted_dt=current_dt, approved_dt=current_dt)
    ]
    database.session.bulk_save_objects(roles)
    database.session.commit()
    logging.warning("seed initial administrator: " + admin_username)
    return

