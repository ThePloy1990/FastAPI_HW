from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

# Эндпоинт Корня (GET /):
@app.get('/')
def root():
    return {"message": "Welcome to the Dog API!"}

# Эндпоинт Получения Списка Собак (GET /dog)
@app.get('/dog')
def get_dogs(kind: DogType = None):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())

# Эндпоинт Создания Собаки (POST /dog):
@app.post('/dog')
def create_dog(dog: Dog):
    dog.pk = max(dogs_db.keys()) + 1
    dogs_db[dog.pk] = dog
    return dog

# Эндпоинт Получения Информации о Конкретной Собаке (GET /dog/{pk}):
@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int):
    return dogs_db.get(pk)

# Эндпоинт Обновления Информации о Собаке (PATCH /dog/{pk}):
@app.patch('/dog/{pk}')
def update_dog(pk: int, updated_dog: Dog):
    if pk in dogs_db:
        dog = dogs_db[pk]
        dog.name = updated_dog.name if updated_dog.name else dog.name
        dog.kind = updated_dog.kind if updated_dog.kind else dog.kind
        return dog
    return {"error": "Dog not found"}

@app.post('/post')
def get_post(post: Timestamp):
    post_db.append(post)
    return post
