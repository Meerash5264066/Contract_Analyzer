import nlp_engine
import database

text = "Late payment will result in penalty. Service may be terminated due to delay."

keywords = database.get_keywords()

result = nlp_engine.analyze_contract(text, keywords)

print(result)