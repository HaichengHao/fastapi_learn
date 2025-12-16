from fastapi import FastAPI

app = FastAPI()

@app.post('/items') #tips:如果不用BaseModel的花我们可以尝试使用字典进行post
async def create_item(user:dict) -> dict:
    return user
