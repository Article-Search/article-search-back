import re
import requests
import torch
import numpy as np
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import util
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import json 

hf_token ='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'
qa_model_token = 'FIvTJW2gToHCBMYHrxu9WRDIENrLQC9G'
api_url= "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {hf_token}"}

class Prompter:
    # init
    def __init__(self) -> None:
        pass
    def query(self,texts):
        response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()
    
    def get_vectorstore(self,text_chunks):
        embeddings = OpenAIEmbeddings()
        # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore

    def get_conversation_chain(self,vectorstore):
        llm = ChatOpenAI()
        memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
        )
        return conversation_chain

    def prompt_openai(self,prompt,context):
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len                                     
        )
        text_chunks = text_splitter.split_text(context)
        # embed the text chunks
        vector_store = self.get_vectorstore(text_chunks)
        conversation_chain = self.get_conversation_chain(vector_store)
        response = conversation_chain({'question':prompt})['answer']
        return  response

    def prompt_qaLM(self,question, text):
        qst_embedding = self.query([question])
        query_embeddings = torch.FloatTensor(qst_embedding)
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len                                     
        )

        chunks = text_splitter.split_text(text)
        output = self.query(chunks)
        print(output)
        output=torch.from_numpy(np.array(output)).to(torch.float)
        result=util.semantic_search(query_embeddings, output,top_k=2)
        final=[chunks[result[0][i]['corpus_id']] for i in range(len(result[0]))]
        url = "https://api.ai21.com/studio/v1/answer"
        
        payload = {
                    "context":' '.join(final),
                    "question":question
        }

        headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "Authorization": f"Bearer {qa_model_token}"
        }
        # check size of context must be < 50 000 characters
        response = requests.post(url, json=payload, headers=headers)
        
        if response.json()['answerInContext']:
            return response.json()['answer']
        else:
            return None

class InfosExtractor:
    
    def __init__(self, dataExtracted) -> None:
        self.data = dataExtracted
        self.prompter = Prompter()
        self.answers_map = {}
        self.answers_map['content'] = self.data.extractedText
        pass
    def firstPass(self):
        # Feature Engineering:
        qst_title= None
        qst_authors = None
        qst_abstract = None
        qst_institutions = None 
        qst_references = None
        qst_summary = 'Summarize this paper ?'
        qst_keywords = 'What are the main keywords used in this paper? separe keywords with commas'

        # create dict
        qst_map = { 'title': qst_title, 'authors': qst_authors, 'abstract': qst_abstract, 'summary': qst_summary, 'institutions': qst_institutions, 'references': qst_references, 'keywords': qst_keywords}

        # get answers
        for qst in qst_map.keys():
            if qst_map[qst]!=None:
                self.answers_map[qst] = self.prompter.prompt_qaLM(qst_map[qst], self.data.extractedText)
        

    def get_authors(self):
        # ------------------------------Authors---------------------------------
        # Using a regular expression to extract text before the word "ABSTRACT"
        pattern = r'(.*?)\sABSTRACT'
        match = re.search(pattern, self.data.extractedText, re.DOTALL)

        if match:
            beforeAbstract = match.group(1)
        else:
            beforeAbstract = None

        match = re.search(r':(.*)', self.prompter.prompt_openai('In the answer just give names and write $ after finishing the answer What are valid human names here? start citing the names after this char :', beforeAbstract), re.DOTALL)
        cleaned_text = ''
        self.answers_map['authors'] = self.prompter.prompt_openai('What are the names authors of this paper? the structure of the answer need to be only names separated by one space', beforeAbstract)
        self.beforeAbstract = beforeAbstract

        #---------------------------------------------------
    def get_keywords(self):
        #---------------------Keywords----------------------
        match = re.search(r':\s*([^:]+)', self.answers_map['keywords'])
        if match:
            keywords = match.group(1)
            # Cleaning the text and keeping only alphabetical characters
            cleaned_text = re.sub(r'[^a-zA-Z,\s]', '', keywords)
            self.answers_map['keywords'] =  cleaned_text.strip()
        #---------------------------------------------------
        
    def get_institutions(self):
        #---------------------Institutions------------------
        # Ask the qst from the parsed using regex of before abstarct using in autohrs 
        inst = self.prompter.prompt_qaLM('What are the institutions or universities and labs where the authors of the paper are affiliated separe them with commas ?', self.beforeAbstract)
        # take what is after :
        match = re.search(r':(.*)', inst, re.DOTALL)
        if match:
            extracted_text = match.group(1).strip()
            # Clean the extracted text from numbers and specific special characters
            cleaned_text = re.sub(r'[^a-zA-Z\s]', '', extracted_text)
            self.answers_map['institutions'] = cleaned_text
        # ---------------------------------------------------

    def get_references(self):
        #---------------------References--------------------
        # Extract the text after abstract and stop at the next line with one word after a jumpline
        references = re.search(r'REFERENCES(.+)', self.data.extractedText , re.DOTALL)
        references = references.group(1) if references else None
        cleaned_text = re.sub(r'[^a-zA-Z\s]+', '', references)
        clean_LM = self.prompter.prompt_openai('What are the references of this paper? separate by this string /SEPARATOR/', references)
        cleaned_text = re.sub(r'[\n]+', ' ', clean_LM)
        self.answers_map['references'] = cleaned_text if cleaned_text else None

        #----------------------------------------------------
    def get_title(self):
        #--------------------Title---------------------------
        title = self.prompter.prompt_qaLM('What is the title of this paper? the answer should be sent as the name of the paper only', self.beforeAbstract)    
        pattern = re.compile(r'\\\"(.*?)\\\"')
        match = pattern.search(title)
        # Extract the desired text
        if match:
            self.answers_map['title'] = match.group(1)
        else:
            self.answers_map['title'] = self.prompter.prompt_openai('What is the title of this paper ?', self.beforeAbstract)

        #----------------------------------------------------
            
    def get_abstract(self):
        #---------------------Abstract------------------------
            
        #extract the text after abstract and stop at the next line with one word after a jumpline
        abstract = re.search(r'ABSTRACT(.+?)\n\n\w', self.data.pageFirstText, re.DOTALL)
        abstract = abstract.group(1) if abstract else None
        abstract = re.sub(r'[\n]+', ' ', abstract)
        self.answers_map['abstract'] = abstract

        #----------------------------------------------------

    def get_summary(self):
        self.answers_map['summary'] = self.prompter.prompt_openai('What is the summary of this paper?', self.data.extractedText)

    def get_answerMap(self):
        return json.dumps(self.answers_map)
            



'''
Un article scientifique est caractérisé par :
Le titre de l’article
Le résumé de l’article
Un ou plusieurs auteurs de l’article
Une ou plusieurs institutions auxquelles appartient les auteurs de l’article
Un ou plusieurs mots clés de l’article
Le texte intégral en format textuel
L’URL du fichier PDF associé
Une ou plusieurs références bibliographiques de l’article
'''
