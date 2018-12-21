import twilio as tw

class Twilio():
    def __init__(self, config):
        _validate_config(config)
        self.account_sid = config['ACCOUNT_SID']
        self.auth_token = config['ACCOUNT_SID']





def _validate_config(config):
    """
    Make sure config object has required values

    """
    required_fields = ["ACCOUNT_SID", "AUTH_TOKEN"]

    for field in required_fields:
        if field not in config:
            raise ValueError("required field {} not found in config file".format(field))


