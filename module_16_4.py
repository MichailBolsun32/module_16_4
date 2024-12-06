from fastapi import FastAPI, Path, HTTPException, Body
from pydantic import BaseModel
from typing import Annotated, List

app = FastAPI()

# Используйте CRUD запросы из предыдущей задачи.

# Создайте пустой список users = []
users = []

# Создайте класс(модель) User, наследованный от BaseModel, который будет содержать следующие поля:
#     id - номер пользователя (int)
#     username - имя пользователя (str)
#     age - возраст пользователя (int)

class User(BaseModel):
    id: int
    username: str
    age: int

#get запрос по маршруту '/users' теперь возвращает список users.

@app.get('/users')
async def get_all_massages() -> List[User]:
    return users

# post запрос по маршруту '/user/{username}/{age}', теперь:
#     Добавляет в список users объект User.
#     id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
#     Все остальные параметры объекта User - переданные в функцию username и age соответственно.
#     В конце возвращает созданного пользователя.

# @app.post('/user/{username}/{age}')
# async def create_message(user_: User) -> User:
#     user_.id = len(users) + 1
#     users.append(user_)
#     return user_

@app.post('/user/{username}/{age}')
async def create_message(username: Annotated[str, Path(min_length=5,
                                             max_length=20,
                                             description='Enter username',
                                             example='UrbanUser')] ,
                        age: Annotated[int, Path(ge=18,
                                      le=120,
                                      description='Enter age',
                                      example='24'
                                      )]) -> User:

    if users:
        new_user = User(id=users[-1].id + 1, username=username, age=age)
    else:
        new_user = User(id=1, username=username, age=age)

    users.append(new_user)
    return new_user


# put запрос по маршруту '/user/{user_id}/{username}/{age}' теперь:
#     Обновляет username и age пользователя, если пользователь с таким user_id
#     есть в списке users и возвращает его.
#     В случае отсутствия пользователя выбрасывается исключение HTTPException с
#     описанием "User was not found" и кодом 404.

@app.put('/user/{user_id}/{username}/{age}')
async def update_message(user_id: Annotated[int, Path(ge=1,
                                                      le=150,
                                                      description='Enter user_id',
                                                      example=1)],
                         age: Annotated[int, Path(ge=18,
                                                  le=120,
                                                  description='Enter age',
                                                  example='24'
                                                  )],
                         username_: Annotated[str, Body(min_length=5,
                                                        max_length=20,
                                                        description='Enter username',
                                                        example='UrbanUser')
                         ]) -> User:
    try:
        edit_user = users[user_id - 1]
        edit_user.age = age
        edit_user.username = username_
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

# delete запрос по маршруту '/user/{user_id}', теперь:
#     Удаляет пользователя, если пользователь с таким user_id
#     есть в списке users и возвращает его.
#     В случае отсутствия пользователя выбрасывается исключение
#     HTTPException с описанием "User was not found" и кодом 404.

@app.delete('/user/{user_id}')
async def delete_message(user_id: Annotated[int, Path(ge=1,
                                                      le=150,
                                                      description='Enter user_id',
                                                      example=1)]) -> User:
    try:
        edit_user = users[user_id - 1]
        users.pop(user_id - 1)
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')
