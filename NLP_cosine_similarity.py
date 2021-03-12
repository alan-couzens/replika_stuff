#An illustrative example of how cosine similarity is used in Replika's retrieval model to select a suitable response


context = [
           "Thank you for always caring about me. I really appreciate it. I think I just need some time to process",
           "I wish you would stay out of my business, you're so irritating. Just back off, will you?"
]
responses = [
             "You're welcome. You know that I care about you and am here for you when you want to talk",
             "Well, you're on your own. I've had enough of your rudeness!"
]

from sklearn.feature_extraction.text import TfidfVectorizer  
vectorizer= TfidfVectorizer()  
X = vectorizer.fit(context)   
array = X.transform(context).toarray()  

import numpy as np  
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

get_matching_response("Thanks for supporting me. I think I just need a little time") 
get_matching_response("I do appreciate you. Thanks for being there for me")
get_matching_response("Seriously? This is what you're coming back with?")
get_matching_response("You're an idiot. I need a break")
