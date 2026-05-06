import redis

# Logic: Establish a connection to the OrbStack Redis container
redis_client = redis.Redis(
    host='localhost', 
    port=6379, 
    db=0, 
    decode_responses=True
)

def get_redis_connection():
    """
    Logic: Test if the container is reachable before the pipeline starts.
    """
    try:
        redis_client.ping()
        print("✅ Redis connection successful!")
        return redis_client
    except redis.ConnectionError:
        print("❌ Redis connection failed. Is the OrbStack container running?")
        return None