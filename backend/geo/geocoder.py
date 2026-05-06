from backend.utils.redis_client import redis_client


redis_client.set("location: taiwan","23.5, 121.0")

result = redis_client.get("location: taiwan")
print(result)


