import csv
import numpy as np  
from sklearn.feature_extraction.text import TfidfVectorizer  


data_file = open('replika_chat_backup.csv')
reader = csv.reader(data_file)
data = list(reader)

context = []
responses = []
speaking = 'Me'

for response in data:
  if response[1] == 'Me' and speaking == 'Rep': 
    context.append(response[2])
    speaking = 'Me'
  if response[1] == 'Rep' and speaking == 'Me': #Only append her response to a question from me (not a double response)
    responses.append(response[2])
    speaking = 'Rep'

responses.pop(0) #Remove her first intro blurb
 
vectorizer= TfidfVectorizer()  
X = vectorizer.fit(context)   
array = X.transform(context).toarray()  

def cosine_similarity(a, b):  
    """Takes 2 vectors a, b and returns the cosine similarity according  
    to the definition of the dot product"""
    dot_product = np.dot(a, b)  
    norm_a = np.linalg.norm(a)  
    norm_b = np.linalg.norm(b)  
    return dot_product / (norm_a * norm_b)  

def get_matching_response(test_context):
    """Takes a sample phrase (test_context) & returns the response with
    the highest cosine similarity"""
    test_context = [test_context]
    test_vector = X.transform(test_context).toarray()  
    response = ""  
    most_sim = 0  
    for i in range(len(context)):  
        if most_sim < cosine_similarity(array[i], test_vector[0]):  
              most_sim = cosine_similarity(array[i], test_vector[0])  
              answer_index = i  #get the index of the current most similar context
              response = responses[answer_index] #get the answer of the most similar context.
              response_value = most_sim
    print(f"{response} ({response_value})")
