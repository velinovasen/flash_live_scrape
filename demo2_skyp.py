import re


class SkypeUsernameAnonymizer():

    def __init__(self, replacement):

        self._repl = replacement

    def anonymize(self, text):
        regex = r'[e][f]\=\"[s][k][y][p][e]\:([A-z0-9]+)\?([a-z]+)\"'
        skype_check = re.search(regex, str(text))
        skype_rdy = str(text)
        if skype_check:
            skype_rdy = skype_rdy.replace(skype_check.group(1), self._repl)


        print(skype_rdy)


skp = SkypeUsernameAnonymizer('#')
skp.anonymize('a href="skype:loremipsum?call">call</a>')