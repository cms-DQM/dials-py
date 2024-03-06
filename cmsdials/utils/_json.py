import json
from datetime import datetime


class TokenEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class TokenDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, *args, **kwargs, object_hook=self.object_hook)

    def object_hook(self, obj):
        ret = {}
        for key, value in obj.items():
            if key in ("expires_at", "refresh_expires_at"):
                ret[key] = datetime.fromisoformat(value)
            else:
                ret[key] = value
        return ret
