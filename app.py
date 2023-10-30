from random import randrange
from typing import Optional
from fastapi import  FastAPI , Response , status, HTTPException,Request,Form
from fastapi.params import Body
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pymysql
from algo_part2 import mlalgo

try:
    connection = pymysql.connect(host='localhost',user='root',password='root',db='sra',autocommit=True)
    cursor = connection.cursor()
    print("database connected")
except Exception as e:
    print("database failed to connect")
    print("error : ",e)


app = FastAPI()
templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="templates"), name="static")
@app.get("/")
def home(request:Request):
    try:
        cursor.execute("select email from truss_user_data")
        user=cursor.fetchall()
        user=[i[0] for i in user]
    except:
        return {"user not found"}

    return templates.TemplateResponse("index.html",{"request": request , "users":user})


@app.get("/get_dynamic_data/{selected_option}",response_model=list[dict])
def get_dynamic_data(selected_option: str):
    dynamic_data = f"recommendations for: {selected_option}"
    data=mlalgo(selected_option)
    users=data.to_dict(orient='records')
    return users

@app.get("/{logged_user}/{selected_option}")
def user_interaction(logged_user,selected_option):
    cursor.execute(f"select user_interaction from truss_user_data where email='{logged_user}'")
    ans=cursor.fetchone()[0]
    cursor.execute(f"select skill_1,skill_2,skill_3 from truss_user_data where email='{selected_option}'")
    skills=cursor.fetchone()
    print(skills)
    l=[]
    if ans is not  None:
        l=ans.split(",")
    for i in skills:
        l.insert(0,i)
    l=l[:50]
    l=', '.join(l)
    query=f"update truss_user_data set User_interaction='{l}' where email='{logged_user}'"
    cursor.execute(query)
    return "data inserted"


