import getpass
import requests
import re
import os

from dotenv import load_dotenv

from .exceptions import (
    LoginFailedException,
    RequireTwoFactorException
)

load_dotenv()

csrf_regexp = re.compile(r"globals.csrf='([a-f0-9-]+)'")

class AuthLevelEnum(object):
    USER_REMEMBERED = "USER_REMEMBERED"
    NONE = "NONE"

class TwoFactorVerificationModeEnum(object):
    SMS = 0
    EMAIL = 1

class PersonalCapital(object):

    SP_HEADER_KEY = "spHeader"
    SUCCESS_KEY = "success"
    CSRF_KEY = "csrf"
    AUTH_LEVEL_KEY = "authLevel"
    ERRORS_KEY = "errors"
    BASE_URL= "https://home.personalcapital.com"
    API_ENDPOINT = '/api'

    def __init__(self):
        self.__session = requests.Session()
        self.__csrf = ""

    def login(self):
        try:
            self.__enter_login_credentials()
        except RequireTwoFactorException:
            self.authenticate_login()
        except LoginFailedException:
            raise LoginFailedException('Login attempt failed')

    def authenticate_login(self):
        self.two_factor_challenge(TwoFactorVerificationModeEnum.SMS)
        self.two_factor_authenticate(TwoFactorVerificationModeEnum.SMS, input('code: '))
        password = self.__get_password()
        self.__authenticate_password(password)

    def two_factor_challenge(self, mode):
        if mode == TwoFactorVerificationModeEnum.SMS:
            return self.__challenge_sms()
        elif mode == TwoFactorVerificationModeEnum.EMAIL:
            return self.__challenge_email()

    def two_factor_authenticate(self, mode, code):
        if mode == TwoFactorVerificationModeEnum.SMS:
            return self.__authenticate_sms(code)
        elif mode == TwoFactorVerificationModeEnum.EMAIL:
            return self.__authenticate_email(code)

    def fetch(self, endpoint, data = None):
        """
        for getting data after logged in
        """
        payload = {
            "lastServerChangeId": "-1",
            "csrf": self.__csrf,
            "apiClient": "WEB"
        }
        if data is not None:
            payload.update(data)

        return self.post(endpoint, payload)

    def post(self, endpoint, data):
        response = self.__session.post(PersonalCapital.BASE_URL + PersonalCapital.API_ENDPOINT + endpoint, data)
        return response

    def get_session(self) -> dict:
        return requests.utils.dict_from_cookiejar(self.__session.cookies)

    def set_session(self, cookies):
        self.__session.cookies = requests.utils.cookiejar_from_dict(cookies)
        
    def set_csrf(self, csrf):
        self.__csrf = csrf
            
    # private methods

    def __enter_login_credentials(self):
        try:
            self.__enter_user_email()
            self.__enter_user_password()
        except LoginFailedException:
            raise LoginFailedException('User credentials are not valid')

    def __enter_user_email(self):
        email = self.__get_email()
        initial_csrf = self.__get_csrf_from_home_page(PersonalCapital.BASE_URL)
        final_csrf, auth_level = self.__identify_user(email, initial_csrf)
        self.set_csrf(final_csrf)

        if (auth_level == AuthLevelEnum.NONE):
            raise LoginFailedException('User email is not valid')
        elif (auth_level != AuthLevelEnum.USER_REMEMBERED):
            raise RequireTwoFactorException

    def __get_email(self):
        email = os.getenv('EMAIL')
        if not email:
            print('You can set the environment variables for PEW_EMAIL and PEW_PASSWORD so the prompts don\'t come up every time')
            return input('Enter email:')
        return email

    def __get_csrf_from_home_page(self, url):
        r = self.__session.get(url)
        found_csrf = csrf_regexp.search(r.text)

        if found_csrf:
            return found_csrf.group(1)
        return None

    def __identify_user(self, username, csrf):
        """
        Returns reusable CSRF code and the auth level as a 2-tuple
        """
        data = {
            "username": username,
            "csrf": csrf,
            "apiClient": "WEB",
            "bindDevice": "false",
            "skipLinkAccount": "false",
            "redirectTo": "",
            "skipFirstUse": "",
            "referrerId": "",
        }

        r = self.post("/login/identifyUser", data)

        if r.status_code == requests.codes.ok:
            result = r.json()
            new_csrf = self.__get_sp_header_value(result, PersonalCapital.CSRF_KEY)
            auth_level = self.__get_sp_header_value(result, PersonalCapital.AUTH_LEVEL_KEY)
            return (new_csrf, auth_level)

        return (None, None)
        
    def __enter_user_password(self):
        password = self.__get_password()
        result = self.__authenticate_password(password).json()
        if self.__get_sp_header_value(result, PersonalCapital.SUCCESS_KEY) == False:
            raise LoginFailedException(getErrorValue(result))

    def __get_password(self):
        password = os.getenv('PASSWORD')
        if not password:
            return getpass.getpass('Enter password:')
        return password

    def __authenticate_password(self, passwd):
        data = {
            "bindDevice": "true",
            "deviceName": "",
            "redirectTo": "",
            "skipFirstUse": "",
            "skipLinkAccount": "false",
            "referrerId": "",
            "passwd": passwd,
            "apiClient": "WEB",
            "csrf": self.__csrf
        }
        return self.post("/credential/authenticatePassword", data)

    @classmethod
    def __get_sp_header_value(cls, result, valueKey):
        if (PersonalCapital.SP_HEADER_KEY in result) and (valueKey in result[PersonalCapital.SP_HEADER_KEY]):
            return result[PersonalCapital.SP_HEADER_KEY][valueKey]
        return None

    @classmethod
    def __get_error_value(cls, result):
        try:
            return cls.__get_sp_header_value(result, PersonalCapital.ERRORS_KEY)[0]['message']
        except (ValueError, IndexError):
            return None

    def __generate_challenge_payload(self, challenge_type):
        return {
            "challengeReason": "DEVICE_AUTH",
            "challengeMethod": "OP",
            "challengeType": challenge_type,
            "apiClient": "WEB",
            "bindDevice": "false",
            "csrf": self.__csrf
        }

    def __generate_authentication_payload(self, code):
        return {
            "challengeReason": "DEVICE_AUTH",
            "challengeMethod": "OP",
            "apiClient": "WEB",
            "bindDevice": "false",
            "code": code,
            "csrf": self.__csrf
        }

    def __challenge_email(self):
        data = self.__generate_challenge_payload("challengeEmail")
        return self.post("/credential/challengeEmail", data)

    def __authenticate_email(self, code):
        data = self.__generate_authentication_payload(code)
        return self.post("/credential/authenticateEmailByCode", data)

    def __challenge_sms(self):
        data = self.__generate_challenge_payload("challengeSMS")
        return self.post("/credential/challengeSms", data)

    def __authenticate_sms(self, code):
        data = self.__generate_authentication_payload(code)
        return self.post("/credential/authenticateSms", data)
