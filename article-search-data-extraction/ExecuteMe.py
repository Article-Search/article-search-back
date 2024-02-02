from DataExtractor import DataExtractor
from ElasticSearchStruct import ElasticSearchStruct
from QA_model import InfosExtractor
import datetime as dt
# extract text from the paper and save it in a file

# track time 
start = dt.datetime.now()
test = DataExtractor('../Research papers/Echantillons Articles-20240101T062528Z-001/Echantillons Articles/Article_09.pdf')
res,PageFirst = test.extractTextFromPdf()
end = dt.datetime.now()
print(f'Extraction took {end-start} seconds')
extractor = InfosExtractor(test)
start = dt.datetime.now()
extractor.firstPass()
extractor.get_authors()
extractor.get_institutions()
extractor.get_references()
extractor.get_summary()
extractor.get_keywords()
extractor.get_title()
# Create an instance of ElasticSearchStruct
end = dt.datetime.now()
print(f'\n\nExtraction infos using AI, Algos and Regex took {end-start} seconds\n\n')
es = ElasticSearchStruct(extractor.answers_map['title'],extractor.answers_map['authors'],extractor.answers_map['institutions'],extractor.answers_map['summary'],extractor.answers_map['keywords'],extractor.answers_map['content'],extractor.answers_map['references'])
es.createAuthors(extractor.answers_map['authors'])
es.createInstitutions(extractor.answers_map['institutions'])
es.createReferences(extractor.answers_map['references'])
es.createKeywords(extractor.answers_map['keywords'])

print(es.createJSON())
 # Extract information from text 
    