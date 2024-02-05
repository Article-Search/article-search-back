# Create the json for Elastic Search 
'''
{
    "publish_date": "date",
    "title": {
        "raw": "text",
        "suggest": "text"
    },
    "authors": [
        {
            "first_name": {
                "raw": "text",
                "suggest": "text"
            },
            "last_name": {
                "raw": "text",
                "suggest": "text"
            }
        }
    ],
    "institutions": [
        {
            "name": {
                "raw": "text",
                "suggest": "text"
            }
        }
    ],
    "summary": {
        "raw": "text",
        "suggest": "text"
    },
    "keywords": ["keyword1", "keyword2"],
    "content": {
        "raw": "text",
        "suggest": "text"
    },
    "pdf_url": "text",
    "references": [
        {
            "title": {
                "raw": "text",
                "suggest": "text"
            }
        }
    ]
}

'''

import re

def clean_text(text):
    # Keep only alphabets, numbers, and certain special characters
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s\.,;!?]', '', text)
    
    # Remove extra whitespaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

class ElasticSearchStruct:
    def __init__(self, title, authors, institutions, summary, keywords, content, references) -> None:
        self.publish_date = None
        self.title = title
        
        self.summary = summary
        
        self.content = clean_text(content)
        
        self.pdf_url = None

    # create Authors
    def createAuthors(self, authors):
        # authors is a string of authors first and last name separated by spaces
        authors = authors.split(' ')
        authorList = []
        for i in range(0, len(authors), 2):
            authorList.append({
                "first_name":  authors[i],
                "last_name":  authors[i+1],  
            })
        self.authors = authorList
    # create Institutions
        
    def createInstitutions(self, institutions):
        self.institutions = institutions.split(',')
        institutionList = []
        for i in range(0, len(institutions), 1):
            institutionList.append({
                "name": self.institutions[i]
            })
        self.institutions = institutionList
    # create Keywords
    def createKeywords(self, keywords):
        self.keywords = keywords.split(',')
    # create References
    def createReferences(self, references):
        references = references.split('/SEPARATOR/')
        referencesList = []
        for reference in references:
            referencesList.append({
                "title": reference
            })
        self.references = referencesList
    def createJSON(self):
        return (
            {
    "publish_date": self.publish_date,
    "title": self.title,
    "authors": self.authors,
    "institutions": self.institutions,
    "summary": self.summary,
    "keywords": self.keywords,
    "content": self.content,
    "pdf_url": self.pdf_url,
    "references": self.references
        }

    )
    
    
    def __str__(self) -> str:
        return f"publish_date: {self.publish_date}, title: {self.title}, authors: {self.authors}, institutions: {self.institutions}, summary: {self.summary}, keywords: {self.keywords}, content: {self.content}, pdf_url: {self.pdf_url}, references: {self.references}"



