# -*- coding: utf-8 -*-
import googletrans
import sys
import config
import json

class Google_Translator:
    def __init__(self):
        self.translator = googletrans.Translator()

    def getAllLanguages(self, withReductions=False):
        langDict = []
        for k,v in googletrans.LANGUAGES.items():
            if withReductions:
                langDict.append(v + '({})'.format(k))
            else:
                langDict.append(v)
        langDict.sort()
        return langDict

    def getTranslationInfo(self, text,  srcLang='en', destLang='ru'):
        result = self.translator.translate(text, src=srcLang, dest=destLang)
        return {
            'src' : result.src,
            'dest' : result.dest,
            'text' : result.text,
            'pronunciation' : result.pronunciation,
            'extra_data' : result.extra_data
            }

    def translate(self, text, srcLang='en', destLang='ru'):
        return self.getTranslationInfo(text, srcLang, destLang)['text']

    def detect(self, text):
        return self.getDetectInfo(text)['lang']

    def getDetectInfo(self, text):
        result = self.translator.detect(text)
        return {
            'lang' : result.lang,
            'confidence' : result.confidence
        }
     

def main():
    translator = Google_Translator()
    if len(sys.argv) < 2:
        print('AVAILABLE LANGUAGES')
        print(translator.getAllLanguages(True))
    elif len(sys.argv) == 2:
        print(translator.translate(sys.argv[1]))
    elif len(sys.argv) == 3: 
        text = sys.argv[1]
        destLang = sys.argv[2]
        srcLang = translator.detect(text)
        try:
            print(translator.translate(text, srcLang, destLang))
        except:
            print('SomeErrorOcuured')
            print('AVAILABLE LANGUAGES')
            print(translator.getAllLanguages(True))    

if __name__ == '__main__':
    main()
    
