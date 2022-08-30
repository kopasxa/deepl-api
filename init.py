from email.parser import Parser
import deepl
import config
from db import database
from parser import Parser

auth_key = config.DEEPL_KEY
translator = deepl.Translator(auth_key)

db = database()
sources = db.get_sources_articles()

for source in sources:
    Parser(source[3])

#try:
#    with open("from_text.txt", "r") as f:
#        file_text = f.read()
#
#        result = translator.translate_text(file_text, target_lang="RU")
#
#        with open("to_text.txt", "w") as f:
#            f.write(result.text)
#
#    print("ok")
#except:
#    print("error")