import json
import logging
from python.common.config import Config

logging.basicConfig(level=Config.LOG_LEVEL)


def load_json_into_dict(file_name) -> dict:
    with open(file_name, 'r') as f:
        data = f.read()
    return json.loads(data)


def validate_form_number(number: str) -> bool:
    """
    Validate check digit used in IRP, VI and UL forms
    :param number:
    :return:
    """
    number_list = list(number)
    check_digit = int(number_list.pop())

    n = list()
    for element in number_list:
        # cast each element to an int
        n.append(int(element))

    # ignore the first two digits, sum the number
    # using a special formula
    number_sum = (
            n[2] +
            _times_2(n[3]) +
            n[4] +
            _times_2(n[5]) +
            n[6] +
            _times_2(n[7]))

    # compare modulus of the sum with check digit
    return number_sum % 10 == check_digit


def _times_2(number: int) -> int:
    """
    If number * 2 is greater than 9, return 1
    otherwise return the number * 2
    :param number:
    :return:
    """
    return int(list(str(number * 2))[0])


def middle_logic(functions: list, **args):
    """
    Recursive function that calls each node in the list.
    Each node has a "try" function that is executed first. If the try
    function returns True, the next node in the list is returned.  If the
    try function returns False, the node's "fail" list is executed in the
    same way.

    example = dict({
            "rules": [
                {
                    "pass": success1,
                    "fail": [
                        {
                            "pass": failure1,
                            "fail": []
                        }
                    ],
                },
            ]
        })

    The middleware is called like this: middle_logic(example['rules'])
    """
    if functions:
        try_fail_node = functions.pop(0)
        logging.debug('calling try function: ' + try_fail_node['try'].__name__)
        flag, args = try_fail_node['try'](**args)
        logging.info("result from {} is {}".format(try_fail_node['try'].__name__, flag))
        if flag:
            logging.debug('calling middleware logic recursively')
            args = middle_logic(functions, **args)
        else:
            logging.debug('calling failure functions recursively')
            args = middle_logic(try_fail_node['fail'], **args)
    return args


def get_listeners(listeners: dict, key: str) -> list:
    """
    Get the list of nested list of functions to invoke
    for a particular form type
    """
    if key in listeners:
        return listeners[key]
    else:
        return listeners['unknown_event']

