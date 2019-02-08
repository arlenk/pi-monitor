from pi_monitor.core import Event
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail
from python_http_client import exceptions


class Sendgrid:
    def __init__(self, config):
        config = _process_config(config)
        self.api_key = config['api_ky']
        self.from_email = config['from_email']
        self.to_email = config['to_email']


    def act(self, event: Event):
        print("{} acting on {}".format(__name__, event))

        sg = sendgrid.SendGridAPIClient(
            apikey=self.api_key,
        )
        from_email = Email(self.from_email)
        to_email = Email(self.to_email)
        subject = "pivpn update"
        content = Content(
            "text/plain", event.message,
        )
        mail = Mail(from_email, subject, to_email, content)

        try:
            response = sg.client.mail.send.post(request_body=mail.get())
        except exceptions.BadRequestsError as e:
            print(e.body)
            raise

        return response


def _process_config(config):
    """
    Make sure config object has required values

    """
    required_fields = [
        "api_key",
        "from_email",
        "to_email",
        ]

    for field in required_fields:
        if field not in config:
            raise ValueError("required field {} not found in config file".format(field))

    return config


