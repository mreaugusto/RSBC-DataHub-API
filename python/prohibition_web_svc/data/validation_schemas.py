
def admin_user_schema() -> dict:
    return {
        "user_guid": {
            'type': 'string',
            'empty': False,
            'required': True
        },
        "business_guid": {
            "type": "string",
            'minlength': 4,
            'maxlength': 40,
            "required": True
        },
        "badge_number": {
            "type": "string",
            'minlength': 2,
            'maxlength': 8,
            "required": True
        },
        "agency": {
            "type": "string",
            'minlength': 4,
            'maxlength': 40,
            "required": True
        },
        "first_name": {
            "type": "string",
            'minlength': 2,
            'maxlength': 30,
            "required": True
        },
        "last_name": {
            "type": "string",
            'minlength': 2,
            'maxlength': 30,
            "required": True,
        },
        "roles": {
            "type": "list",
            "required": True,
            "schema": {
                "type": "string",
                'allowed': ['administrator', 'agency_admin', 'officer']
            }
        }
    }


def agency_user_schema() -> dict:
    """
    Agency admins cannot create users with administrator permissions
    """
    schema = admin_user_schema()
    schema['roles']['schema']['allowed'] = ['agency_admin', 'officer']
    return schema
