from __future__ import annotations

import argparse
import os
from typing import Optional

import google.generativeai as genai
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Gemini client setup
# ---------------------------------------------------------------------------
API_KEY: Optional[str] = "" # ADD API KEY HERE......
if not API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY environment variable not set.")

# Configure the global Gemini client once at import‑time.
genai.configure(api_key=API_KEY)
MODEL = genai.GenerativeModel("gemini-1.5-flash")  # light, fast, cheap

# ---------------------------------------------------------------------------
# MCP server definition
# ---------------------------------------------------------------------------

mcp = FastMCP("Gemini MCP Server") 


@mcp.tool()
def chat(prompt: str, temperature: float = 0.3) -> str:
    """Return Gemini’s answer to *prompt*.

    Args:
        prompt:  The natural‑language question or instruction.
        temperature: Sampling temperature (0–1). Lower = more deterministic.
    """

    # Simple, blocking call – OK for demo purposes.
    response = MODEL.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=temperature),
    )

    return response.text.strip()


# ---------------------------------------------------------------------------
# Entry‑point helpers (stdio vs SSE transport)
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Gemini MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Communication transport. stdio is recommended for local use.",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host for SSE mode")
    parser.add_argument("--port", type=int, default=8080, help="Port for SSE mode")
    args = parser.parse_args()

    if args.transport == "stdio":
        # One‑line helper provided by FastMCP.
        mcp.run(transport="stdio")
        return

    # --- SSE transport (useful when you need HTTP access) ---
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.routing import Mount, Route
    import uvicorn

    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request):
        async with sse.connect_sse(request.scope, request.receive, request._send) as (
            read_stream,
            write_stream,
        ):
            await mcp._mcp_server.run(
                read_stream,
                write_stream,
                mcp._mcp_server.create_initialization_options(),
            )

    app = Starlette(
        debug=False,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()