from mycroft import MycroftSkill, intent_file_handler


class TotpAutheticate(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('autheticate.totp.intent')
    def handle_autheticate_totp(self, message):
        self.speak_dialog('autheticate.totp')


def create_skill():
    return TotpAutheticate()

