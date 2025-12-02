import uvicorn
from backend.config import config
from backend import app

def main():
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT,
        log_level="debug" if config.DEBUG else "info",
        ssl_keyfile=config.SSL_KEYFILE,
        ssl_certfile=config.SSL_CERTFILE,
    )
    


if __name__ == "__main__":
    main()
