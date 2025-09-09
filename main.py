from fastapi import FastAPI
import os

app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello" : "World"}




if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Default to 8080 if PORT not set
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)