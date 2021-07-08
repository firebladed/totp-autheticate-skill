from mycroft import MycroftSkill, intent_file_handler
import pyotp
from mycroft.util.parse import extract_number, extract_numbers
import logging



class TotpAutheticate(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('authenticate.totp.intent')
    def handle_autheticate_totp(self, message):
        response_code = self.get_response('Please.read.authentication.code', validator=code_validate, on_fail=code_fail, num_retries= 3 )       
        # ensure number is six digit number as can be read/spoken in multiple ways      
        code = code_extract(response_code)
          
    
        ret = self.totp_validate(code)

        if ret == 1:
           self.speak_dialog('authentication.code.accepted')
        elif ret == 0:
            self.speak_dialog('authentication.code.invalid')
        elif ret == -1:
            self.speak_dialog('authentication.key.not.configured')

    def code_extract(utterance):       
        nums = extract_numbers(utterance) 
        numstr = ""
        for number in nums:
            numstr += str(number)
        return numstr        
        
    def code_validate(utterance):
        numstr= self.code_extract(utterance) 
        logging.debug('Numstr: '+ numstr)
        return numstr.isnumeric() && (len(numstr) == 6)
 
    def code_fail(utterance):
        return translate('please.repeat.authentication.code')

#    def totp_generate

#    def qrcode_display
        
    def totp_validate(self,code):
        if self.settings.get('totp_key', False):
            return -1
        else:
            key = self.settings.get('totp_key')
            totp = pyotp.TOTP(key)
            if totp.verify(code):
                return 1
        return 0
        
        
        
        
def create_skill():
    return TotpAutheticate()

