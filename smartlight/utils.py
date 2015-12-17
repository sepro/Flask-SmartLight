import json
from functools import wraps

def error_to_json(f):
    @wraps(f)
    def applicator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})

    return applicator