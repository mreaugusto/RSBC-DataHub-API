

def log_static_get(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "get static resource",
        "resource": kwargs.get('resource'),
        "user_guid": kwargs.get('user_guid', ''),
        "username": kwargs.get('username', '')
    }
    return True, kwargs


def log_form_index(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "get form index",
        "user_guid": kwargs.get('user_guid', ''),
        "username": kwargs.get('username')
    }
    return True, kwargs


def log_form_create(**kwargs) -> tuple:
    forms_response = kwargs.get('response_dict')
    kwargs['splunk_data'] = {
        "event": "create form",
        "user_guid": kwargs.get('user_guid', ''),
        "username": kwargs.get('username'),
        'form_type': kwargs.get('form_type'),
        'lease_expiry': forms_response.get('lease_expiry'),
        'id': forms_response.get('id')
    }
    return True, kwargs


def insufficient_form_ids(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "insufficient form ids",
        "user_guid": kwargs.get('user_guid', ''),
        "username": kwargs.get('username'),
        'form_type': kwargs.get('form_type'),
    }
    return True, kwargs


def unable_to_renew_lease(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "unable to renew form lease",
        "user_guid": kwargs.get('user_guid', ''),
        "username": kwargs.get('username'),
        'form_type': kwargs.get('form_type'),
        'id': kwargs.get('form_id')
    }
    return True, kwargs


def form_submitted(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "form submitted",
        "user_guid": kwargs.get('user_guid', ''),
        "username": kwargs.get('username'),
        'form_type': kwargs.get('form_type'),
        'id': kwargs.get('form_id')
    }
    return True, kwargs


def form_lease_renewed(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "form lease renewed",
        "user_guid": kwargs.get('user_guid', ''),
        "username": kwargs.get('username'),
        'form_type': kwargs.get('form_type'),
        'id': kwargs.get('form_id')
    }
    return True, kwargs


def get_user(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "get user",
        "user_guid": kwargs.get('user_guid', ''),
        "username": kwargs.get('username')
    }
    return True, kwargs


def get_users(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "get users",
        "business_guid": kwargs.get('business_guid', ''),
        "requesting_user_guid": kwargs.get('user_guid', ''),
        "requesting_username": kwargs.get('username')
    }
    return True, kwargs


def create_user(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        'event': 'create user',
        'requesting_user_guid': kwargs.get('user_guid', ''),
        'requesting_username': kwargs.get('username'),
        'business_guid': kwargs.get('business_guid'),
        'payload': kwargs.get('payload')
    }
    return True, kwargs


def update_user(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        'event': 'update user',
        'requesting_user_guid': kwargs.get('user_guid', ''),
        'requesting_username': kwargs.get('username'),
        'business_guid': kwargs.get('business_guid'),
        'payload': kwargs.get('payload')
    }
    return True, kwargs


def delete_user(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        'event': 'delete user',
        'requesting_user_guid': kwargs.get('user_guid', ''),
        'requesting_username': kwargs.get('username'),
        'deleted_user_guid': kwargs.get('delete_user_guid'),
    }
    return True, kwargs


def admin_get_forms(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "admin get forms",
        "form_type": kwargs.get('form_type')
    }
    return True, kwargs


def admin_create_form(**kwargs) -> tuple:
    payload = kwargs.get('payload')
    kwargs['splunk_data'] = {
        "event": "admin create form",
        "form_type": payload.get('form_type'),
        "form_id": payload.get('form_id')
    }
    return True, kwargs


def permission_denied(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "permission denied",
        "user_guid": kwargs.get('user_guid', ''),
        "username": kwargs.get('username')
    }
    return True, kwargs


def unauthenticated(**kwargs) -> tuple:
    kwargs['splunk_data'] = {
        "event": "unauthenticated",
    }
    return True, kwargs


def basic_authentication_failed(**kwargs) -> tuple:
    request = kwargs.get('request')
    # not sure the remote address will help much the remote
    # address is almost certainly the address of the proxy
    kwargs['splunk_data'] = {
        "event": "basic authentication failed",
        "requesting_ip": request.remote_addr
    }
    return True, kwargs

