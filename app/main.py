from fastapi import FastAPI

app = FastAPI(
    docs_url="/api/docs"
)

@app.get("/")
def root():
    return {
        "message": "Social Hub API",
        "docs": "/api/docs"
    }