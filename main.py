import uvicorn
from backend.config import config
from backend import app

def main():
    uvicorn.run(
        app="backend.app:app",
        host=config.HOST,
        port=config.PORT,
        ssl_keyfile=config.SSL_KEYFILE,
        ssl_certfile=config.SSL_CERTFILE,
        reload=True if config.DEBUG else False,
    )
    


if __name__ == "__main__":
    main()
