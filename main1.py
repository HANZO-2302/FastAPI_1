# Необходимо создать API для управления списком пользователей.
# Создайте класс User с полями id, name, email и password.

# API должен содержать следующие конечные точки:
# — GET /users — возвращает список пользователей.
# — GET /users/{id} — возвращает пользователя с указанным идентификатором.
# — POST /users — добавляет нового пользователя.
# — PUT /users/{id} — обновляет пользователя с указанным идентификатором.
# — DELETE /users/{id} — удаляет пользователя с указанным идентификатором.

# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.

from fastapi import FastAPI,HTTPException,Request
import uvicorn
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app=FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str
    email: Optional[str]   #может быть пустой строка =None можно не писать
    password: str

class UserInput(BaseModel): # — POST /users — добавляет нового пользователя.
    name: str
    email: Optional[str]
    password: str

users=[
    User(id=0, name='Vasileva',email='122@mail.ru', password='111111'),
    User(id=1, name='Ivanov',email='123@mail.ru', password='222222'),
    User(id=2, name='Petrov',email='124@mail.ru', password='333333'),
    User(id=3, name='Sidorov',email='125@mail.ru', password='444444'),
    User(id=4, name='Kalunin',email='126@mail.ru', password='555555')
]

@app.get("/users")  # — GET /users — возвращает список пользователей.
async def get_users():
    return users

@app.post("/users",response_model=list[User]) # — POST /users — добавляет нового пользователя.
async def new_user(user: UserInput):
    user=User(
        id=len(users),
        name=user.name,
        email =user.email,
        password=user.password
    )
    users.append(user)
    return users

@app.get('/users{user_id}',response_model=User)  # — GET /users/{id} — возвращает пользователя с указанным идентификатором.
async def one_user(user_id : int):
    if len(users)<user_id:
        raise HTTPException(status_code=404, detail='User not found')
    return users[user_id]

@app.put('/users{user_id}',response_model=User)  # — PUT /users/{id} — обновляет пользователя с указанным идентификатором.
async def edit_user(user_id : int,new_user:UserInput):
    for user in users:
        if user.id==user_id:
            user.name=new_user.name
            user.email=new_user.email
            user.password=new_user.password
            return user
    raise HTTPException(status_code=404, detail='User not found')

@app.delete('/users{user_id}',response_model=str)  #put response_model=str - возвращает строку
async def delete_user(user_id : int,new_user:UserInput):
    for user in users:
        if user.id==user_id:
            users.remove(user)
            return 'Задача удалена'
    raise HTTPException(status_code=404, detail='Task not found')

@app.get("/users{user_id}", response_class=HTMLResponse)
async def read_HTML_user(request: Request,user_id:int):
    return templates.TemplateResponse(name="user.html", context={"request": request,'user_id':user_id})


if __name__=='__main__':
    uvicorn.run('task_3-5:app', host ='127.0.0.1', port=8000, reload=True)