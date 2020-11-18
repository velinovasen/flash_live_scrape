"""Email anonymizer module."""
import re


class EmailAnonymizer():


    def __init__(self, replacement):

        if not isinstance(replacement, str):
            raise ValueError
        self._replacement = replacement

    def anonymize(self, text):

        #
        # @TODO: Implement it
        #
        regex = r"([A-z0-9]|[A-z0-9]{1}[A-z0-9._+-]+)@[A-z0-9][A-z0-9._+-]+"

        matched_email = re.search(regex, str(text))
        email_done = str(text)
        print(matched_email.groups())
        if matched_email:
            #token = email_done.split(matched_email)
            email_done = email_done.replace(matched_email.group(1), self._replacement)


        print(email_done)
        return email_done
#Lorem ...@bb12.com ipsum
eml = EmailAnonymizer('***')
eml.anonymize('Lorem some@data ipsum')