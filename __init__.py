from mycroft import MycroftSkill, intent_file_handler
import pyotp
from mycroft.util.parse import extract_number, extract_numbers
import logging
import base64



class TotpAutheticate(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('authenticate.totp.intent')
    def handle_autheticate_totp(self, message):
        response_code = self.get_response('Please.read.authentication.code', validator=self.code_validate, on_fail=self.code_fail, num_retries= 3 )       
        # ensure number is six digit number as can be read/spoken in multiple ways      

        if response_code == None:
            self.speak_dialog('authentication.code.invalid')
        else:
            code = self.code_extract(response_code)

            ret = self.totp_validate(code)

            if ret == 1:
                self.speak_dialog('authentication.code.accepted')
            elif ret == 0:
                self.speak_dialog('authentication.code.invalid')
            elif ret == -1:
                self.speak_dialog('authentication.key.not.configured')

    def code_validate(self, utterance):
        numstr= self.code_extract(utterance)
        self.log.debug('Validate Code')
        self.log.debug('Numstr: '+ numstr)
        return numstr.isnumeric() and (len(numstr) == 6)

    def code_fail(self, utterance):
        return self.translate('please.repeat.authentication.code')

    def code_extract(self, utterance):
        self.log.debug("Extract code from utterance: "+utterance)
        nums = extract_numbers(utterance)
        numstr = ""
        for number in nums:
            self.log.debug("Extracted number: "+ str(int(number)))
            numstr += str(int(number))
        self.log.debug("Extracted code: "+numstr)
        return numstr

    def checkkey(self,key):
        keyl = len(key)
        self.log.debug("Key Length:" + str(keyl))
        if keyl != 32:
           self.log.info("Key Wrong Length")
           return False
        try:
            base64.b32decode(key)
        except:
            self.log.info("Invalid Key Encoding")
            return False
        return True

#    def totp_generate
#
#    def qrcode_display

    def totp_validate(self, code):
        if self.settings.get('totp_key', False) == False:
            self.log.debug('TOTP Key Not Set')
            return -1
        else:
            key = self.settings.get('totp_key')
            self.log.debug('TOTP Key: '+ key)
            if not self.checkkey(key):
                return -1

            totp = pyotp.TOTP(key)
            self.log.debug('TOTP Code: Currently: '+str(totp.now()))
            if totp.verify(code):
                self.log.info("Valid Code")
                return 1
        self.log.info("Invalid Code")
        return 0




def create_skill():
    return TotpAutheticate()

