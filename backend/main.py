from fastapi import FastAPI
import httpx
app = FastAPI(title="GeoAir API", description="API for GeoAir application", version="1.0.0")
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



@app.get("/news")
async def get_news():
    api_key = "7572e05d9c1440a9887c595d6019bf7b"  # Replace with your actual API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}