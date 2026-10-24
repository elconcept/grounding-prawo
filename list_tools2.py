import sys
sys.path.insert(0, "/app/.venv/lib/python3.13/site-packages")
import os
os.environ["PORTAINER_URL"] = "http://portainer:9000"
os.environ["PORTAINER_PROFILES"] = "BASE,DOCKER,KUBERNETES,GITOPS"
os.environ["PORTAINER_READ_ONLY"] = "0"
os.environ["PORTAINER_NO_PROXY"] = "0"

import portainer_mcp.server as srv_module

# build_server is sync but uses asyncio.run internally
mcp = srv_module.build_server()

# Now we need to get tools - list_tools is async
import asyncio

async def get_tools():
    tools = await mcp.list_tools()
    for t in tools:
        print(t.name)
    print(f"Total: {len(tools)}")

asyncio.run(get_tools())
