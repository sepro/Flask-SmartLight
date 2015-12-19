import json
from functools import wraps


def error_to_json(f):
    """
    Decorator to catch errors from a function and return the error as a json string.

    usage (will return status error and Division By Zero):

    @main.route('/example')
    @error_to_json
    def example():
        12/0
        return True
    """
    @wraps(f)
    def applicator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})

    return applicator
