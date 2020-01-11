import requests
class User:
    def __init__(self, pathToToken):
        self.__PATH = pathToToken
        self.__URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    
    def __IsEnglish(self, sentense):
        if sentense[0] in "qwertyuiopasdfghjklzxcvbnm":
            return True
        return False
     
    def __DoRequest(self, url, options):
        try:
            webRequest = requests.get(url, params = options)
            resp = ''
            for i in webRequest.json()["text"]:
                resp+=i
            return resp
        except requests.exceptions.ConnectionError:
            return "ConnectionError"
        except:
            return "TokenError"
    
    def __GetToken(self):
        try:
            reader = open(self.__PATH, 'r')
            token = reader.read()
            reader.close()
            return token
        except:
            return None
        
        
    def DoTranslate(self, sentense):
        if sentense is None or len(sentense) < 1:
            return None
            
        language = 'ru-en'
        if self.__IsEnglish(sentense):
            language = 'en-ru'
            
        token = self.__GetToken()
        if token is None:
            return None
        options = {
                    'key'  : token, 
                    'text' : sentense, 
                    'lang' : language
                }
        
        return self.__DoRequest(self.__URL, options)
                  

    
    
    