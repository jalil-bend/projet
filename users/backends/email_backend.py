from django.core.mail.backends.smtp import EmailBackend as BaseEmailBackend
import smtplib
from socket import gethostname
import ssl
from django.core.mail.utils import DNS_NAME

class EmailBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def open(self):
        if self.connection:
            return False

        connection_class = smtplib.SMTP
        if self.use_ssl:
            connection_class = smtplib.SMTP_SSL

        connection_params = {'local_hostname': DNS_NAME.get_fqdn()}
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout

        try:
            self.connection = connection_class(
                self.host,
                self.port,
                context=self.ssl_context,
                **connection_params
            )

            if not self.use_ssl and self.use_tls:
                self.connection.starttls(context=self.ssl_context)

            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except:
            if not self.fail_silently:
                raise
