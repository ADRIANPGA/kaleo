import uvicorn
import os
from ..app import app

def get_server_config():
    port = int(os.getenv("KALEO_CORE_PORT", "13080"))
    return uvicorn.Config(
        "kaleo_core.app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

def main():
    config = get_server_config()
    uvicorn.run(
        app=config.app,
        host=config.host,
        port=config.port,
        reload=config.reload
    )

if __name__ == "__main__":
    main()

async def start_uvicorn():
    config = get_server_config()
    server = uvicorn.Server(config)
    await server.serve() 