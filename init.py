import deepl
import config
from db import database
from Parser import Parser
import threading

auth_key = config.DEEPL_KEY
translator = deepl.Translator(auth_key)

db = database()
sources = db.get_sources_articles()

for source in sources:
    if source[1]:# == "DW":
        parser = Parser(source[4])
        threading.Thread(target=parser.get_all_articles, args=(source[2],)).start()
        #parser.get_all_articles(source[2])

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