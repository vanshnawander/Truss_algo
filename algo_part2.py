import pandas as pd
import pymysql
import spacy
from scipy import spatial
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
try:
     connection=pymysql.connect(host="truss.clwk1t6znrss.ap-south-1.rds.amazonaws.com",user='admin',password='axtrixninjastar321',db='truss', autocommit=True)
except Exception as e:
    print("database failed to connect")
    print("error : ",e)
def convert(text):
  try:
    return text.replace(" ","")
  except:
    return ""
  
def func(text):
  try:
    l=text.split(",")
    for i in range(len(l)):
      l[i]=l[i].replace(" ","")
    return " ".join(l)
  except:
    return ""
nlp = spacy.load('en_core_web_sm')
def spacy_tokenizer(doc):
  return [t.text for t in nlp(doc) if not t.is_punct]

def mlalgo(email):
    df = pd.read_sql(sql="SELECT * FROM truss_data", con=connection)  
    df=df.dropna(subset=["email"])
    print(df.index)
    ans=pd.DataFrame()
    ans["email"] = df["email"]
    ans["tags"]=df["gender"]+" "+ df["residence"] +" "+ df["focused industry"]+" "+ df["skill_1"].apply(convert)+ " "+df["skill_2"].apply(convert)+" "+df["skill_3"].apply(convert)
    ans["skills_required"]=df["skills_required"].apply(func) +" "+ df["residence"]+" "+df["gender"]+" " + df["user_interaction"].apply(func)
    ans.fillna("",inplace=True)
    corpus=list(ans['tags'])
    vectorizer = CountVectorizer(tokenizer=spacy_tokenizer, lowercase=False, binary=True)
    bow = vectorizer.fit_transform(corpus)
    new_sentences = list(ans["skills_required"][ans["email"]==email])
    new_bow = vectorizer.transform(new_sentences)
    similarities = cosine_similarity(new_bow, bow)
    for i, new_sentence in enumerate(new_sentences):
        most_similar_indices = similarities[i].argsort()[::-1][:5]  
    return (df.loc[list(most_similar_indices)]).to_dict(orient='records')






