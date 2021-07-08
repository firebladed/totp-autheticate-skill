from mycroft import MycroftSkill, intent_file_handler
import pyotp
import mycroft.util.parse
import logging



class TotpAutheticate(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('autheticate.totp.intent')
    def handle_autheticate_totp(self, message):
        response_code = self.get_response('Please.read.authentication.code')       
        # ensure number is six digit number as can be read/spoken in multiple ways
        nums = extract_numbers(response_code) 
        numstr = ""
        for number in nums:
            numstr = str(number)
        code = int(numstr)
    
    logging.debug('AuthCode: '.code)
    
    ret = self.totp_validate(code)
    
    if ret == 1:
       self.speak_dialog('authentication.code.accepted')
    elif ret == 0
        self.speak_dialog('authentication.code.invalid')
    elif ret == -1
        self.speak_dialog('authentication.key.not.configured')

        
#    def totp_generate

#    def qrcode_display
        
    def totp_validate(self,code):
        if self.settings.get('totp_key', False):
            return -1
        else
            key = self.settings.get('totp_key')
            totp = pyotp.TOTP(key)
            if totp.verify(code):
                return 1
        return 0
        
        
        
        
def create_skill():
    return TotpAutheticate()

