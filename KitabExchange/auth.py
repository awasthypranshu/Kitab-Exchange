from fastapi import Header,HTTPException

API_KEY ="1234"

async def check_auth(x_api_key: str = Header()):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key
    