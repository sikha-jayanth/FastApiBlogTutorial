from fastapi import FastAPI
app = FastAPI()


@app.get("/blog/{blog_id}")
def get_blog(blog_id: int):
    return {"blog": blog_id}