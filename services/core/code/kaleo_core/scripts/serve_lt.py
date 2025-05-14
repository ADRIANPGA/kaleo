import asyncio
import subprocess
import signal
import sys
import os

from .serve import start_uvicorn, get_server_config

TUNNEL_SUBDOMAIN = "kaleogwdemodemon"
TUNNEL_PORT = get_server_config().port

async def start_localtunnel():
    # Check if lt is installed
    try:
        subprocess.run(["lt", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ localtunnel (lt) is not installed. Please install it with: npm install -g localtunnel")
        sys.exit(1)

    process = await asyncio.create_subprocess_exec(
        "lt", "--port", str(TUNNEL_PORT), "--subdomain", TUNNEL_SUBDOMAIN,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    print("🔌 Starting localtunnel...")
    tunnel_url = None
    
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        decoded = line.decode("utf-8").strip()
        print(f"[lt] {decoded}")
        if "your url is" in decoded:
            tunnel_url = decoded.split('is ')[-1]
            print(f"🌍 Public URL: {tunnel_url}")
            break

    if not tunnel_url:
        print("❌ Failed to get localtunnel URL")
        process.terminate()
        sys.exit(1)

    return process

async def main_async():
    tunnel_process = None
    try:
        # Start localtunnel first
        tunnel_process = await start_localtunnel()
        
        # Then start uvicorn
        await start_uvicorn()

    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        if tunnel_process:
            tunnel_process.terminate()
            try:
                await tunnel_process.wait()
            except:
                pass
        sys.exit(0)

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        sys.exit(0)
