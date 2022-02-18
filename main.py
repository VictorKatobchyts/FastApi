import re
from typing import Optional
from fastapi import Body, FastAPI, Response, status,  HTTPException
from pydantic import BaseModel, PostgresDsn #read in documentation
from random import randrange
app = FastAPI()#app -навзание в примере было, можно любое

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
my_posts = [{"title": "title of post 1", "content":"content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
def find_index_post(id): #нахождение по индексу для удаления постов (delete)
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
@app.get("/") #декоратор / - озночает корневой путь(http://127.0.0.1:8000, если в конце этого адреса добавит слеш (/) - ничего не поменяется,ecли написать @app.get("/login") то адрес поменяется на http://127.0.0.1:8000/login ) get - метод http протокола, app -экземпляр класса FastAPI
async def root():
    return {"message": "Welcome to my api!!!!"}

@app.get("/posts")
async def get_posts():
   return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}
    #title str, content str; когда создаем crud запросы и  используем название для ориентации используем во множественном числе, если пользователь, то  /users
    # метод put - для обнолвения всех полей данных, patch - для обновления одного поля
@app.get("/posts/{id}") #id - path parametr, если ERL прописываем например с двумя слешами(/.../...), может быть ошибка будет путать с /.../{id} следить за порядком декораторов
def get_post(id: int): #  : int  чтобы быть увереным, что ничего кроме id типа integer не пройдет
    post = find_post(id) #не забываем во время прописи логики перевести один тип в другой
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} is not found")#каждый раз, когда прописываешь запросы проверяешь статус ответа (404, 200,201)
    return {"post_detail": post}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #find the index in the array that has required ID
    #my_posts.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)#специальный момент для метода delete, delete не лолжен ничего возвращать

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{"data": post_dict}
