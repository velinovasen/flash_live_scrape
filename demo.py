import re

# regex = r"^[a-zA-Z0-9][a-zA-Z0-9_.+-]+[a-zA-Z0-9]@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
# email = 'asdhsdh@jhsdks.com'
# matched_email = re.search(regex, str(email))
# email_rdy = ''
# if matched_email:
#     email_rdy = matched_email.group(0)
#
# email_hidden = email_rdy.split('@')[1]
# email_hidden = '...@' + email_hidden
# print(email_hidden)

class PhoneNumberAnonymizer():

    def __init__(self, replacement, last_digits=3):

        if not isinstance(replacement, str) or not isinstance(last_digits, int):
            raise ValueError
        self._repl = replacement
        self._digits = last_digits

    def anonymize(self, text):

        regex = r'[ ]\+[0-9]+[ ](\d{9})'
        phone_check = re.findall(regex, str(text))
        phones_input = str(text)

        for x in phone_check:
            to_replace = list(x)[::-1]
            for y in range(self._digits):
                to_replace[y] = self._repl
            to_replace_rdy = "".join(to_replace[::-1])
            phones_input = phones_input.replace(x, to_replace_rdy)
        print(phones_input)
        return phones_input


phn = PhoneNumberAnonymizer('x', 7)
phn.anonymize('*-3-Lorem +48 666666123, +48 777777777 sit 888888888 amet')