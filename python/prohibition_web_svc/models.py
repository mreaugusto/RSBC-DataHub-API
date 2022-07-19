from datetime import datetime, timedelta
from python.prohibition_web_svc import db, ma
from marshmallow_sqlalchemy.fields import Nested, fields
import logging


class Form(db.Model):
    id = db.Column('id', db.String(20), primary_key=True)
    form_type = db.Column(db.String(20), nullable=False)
    lease_expiry = db.Column(db.Date, nullable=True)
    printed_timestamp = db.Column(db.DateTime, nullable=True)
    user_guid = db.Column(db.String(80), db.ForeignKey('user.user_guid'), nullable=True)
    user = db.relationship("User", backref="form")

    def __init__(self, form_id, form_type, printed=None, lease_expiry=None, user_guid=None):
        self.id = form_id
        self.form_type = form_type
        self.printed_timestamp = printed
        self.lease_expiry = lease_expiry
        self.user_guid = user_guid

    def lease(self, user_guid):
        today = datetime.now()
        lease_expiry = today + timedelta(days=30)
        self.lease_expiry = lease_expiry
        self.user_guid = user_guid
        logging.info("{} leased {} until {}".format(
            self.user_guid, self.id, self.lease_expiry.strftime("%Y-%m-%d")))


class UserRole(db.Model):
    role_name = db.Column(db.String(20), primary_key=True)
    user_guid = db.Column(db.String(80), db.ForeignKey('user.user_guid'), primary_key=True)
    submitted_dt = db.Column(db.DateTime, nullable=True)
    approved_dt = db.Column(db.DateTime, nullable=True)

    def __init__(self, role_name, user_guid, submitted_dt=None, approved_dt=None):
        self.role_name = role_name
        self.user_guid = user_guid
        self.submitted_dt = submitted_dt
        self.approved_dt = approved_dt

    @staticmethod
    def get_roles(user_guid):
        rows = db.session.query(UserRole) \
            .filter(UserRole.user_guid == user_guid) \
            .filter(UserRole.approved_dt != None) \
            .all()
        user_role_schema = UserRoleSchema(many=True)
        return user_role_schema.dump(rows)


class User(db.Model):
    user_guid = db.Column(db.String(120), primary_key=True)
    business_guid = db.Column(db.String(120), nullable=True)
    agency = db.Column(db.String(120), nullable=False)
    badge_number = db.Column(db.String(12), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(40), nullable=True)
    roles = db.relationship(UserRole, backref='roles', lazy='dynamic')

    def __init__(self, user_guid, agency, badge_number, last_name, first_name, business_guid, roles=()):
        self.user_guid = user_guid
        self.agency = agency
        self.badge_number = badge_number
        self.last_name = last_name
        self.first_name = first_name
        self.business_guid = business_guid
        self.roles = roles


class FormSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Form

    id = ma.auto_field()
    form_type = ma.auto_field()
    user = ma.auto_field()
    printed_timestamp = ma.auto_field()
    lease_expiry = ma.auto_field()


class UserRoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserRole

    role_name = ma.auto_field()
    user_guid = ma.auto_field()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    user_guid = ma.auto_field()
    agency = ma.auto_field()
    badge_number = ma.auto_field()
    last_name = ma.auto_field()
    first_name = ma.auto_field()
    business_guid = ma.auto_field()
    roles = fields.Pluck(UserRoleSchema, "role_name", many=True)
