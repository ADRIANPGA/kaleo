import sys
import os

# Ensure the project root is in sys.path to find kaleo_core_api_server
# __file__ is .../code/kaleo_core/scripts/serve.py
# project_root becomes .../code/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import uvicorn
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