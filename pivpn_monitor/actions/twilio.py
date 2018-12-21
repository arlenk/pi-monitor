import twilio as tw


class Twilio():
    def __init__(self, config):
        config = _process_config(config)
        self.account_sid = config['account_sid']
        self.auth_token = config['auth_token']
        self.from_phone = config['from_phone']
        self.to_phone = config['to_phone']


    def act(self, event):
        pass





def _process_config(config):
    """
    Make sure config object has required values

    """
    required_fields = [
        "account_sid",
        "auth_token",
        "from_phone",
        "to_phone",
        ]

    for field in required_fields:
        if field not in config:
            raise ValueError("required field {} not found in config file".format(field))

    return config


