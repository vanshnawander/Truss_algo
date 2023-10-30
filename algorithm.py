import pandas as pd
import pymysql
try:
    connection = pymysql.connect(host='database-1.cpgnivwu2wnj.us-east-1.rds.amazonaws.com',user='root',password='vanshr123@&',db='sra',autocommit=True)
    print("database connected")
except Exception as e:
    print("database failed to connect")
    print("error : ",e)

def mlalgo(email):
    df = pd.read_sql(sql="SELECT * FROM truss_user_data", con=connection)  
    df=df.dropna(subset=["email"])
    df=df.iloc[:,:18]
    a=email
    x=df[df["email"]==a]
    l=list(x["skills_required"])
    l=l[0].split(", ")
    k=[]
    c=0
    ans=pd.DataFrame(columns=list(df.columns))
    for i in l:
        k.append((df["skill_1"]==i) | (df["skill_2"]==i) | (df["skill_3"]==i))
        l=list(df[k[c]]["name"])
        ans=pd.concat([df[k[c]],ans])
        c+=1
    final_ans=ans.groupby(['email'])['name'].count().reset_index(name='Count').sort_values(['Count'], ascending=False)
    desired_order=final_ans['email']
    return df[df['email'].isin(desired_order)]
