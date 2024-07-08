from fastapi import FastAPI

# Create FastAPI app instance
app = FastAPI()

# Define a root endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

# Define another endpoint
@app.get("/info")
async def read_info():
    return {"message": "This is a FastAPI app with two endpoints."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)