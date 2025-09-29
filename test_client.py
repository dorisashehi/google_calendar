"""
Interactive CLI client for Google Calendar MCP Server

This lets you schedule and manage meetings through simple text commands.
"""

import asyncio
import re
from datetime import datetime, timedelta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def interactive_client():
    """Interactive client for Google Calendar MCP server."""

    server_params = StdioServerParameters(
        command="python3",
        args=["calendar_server.py"]
    )

    print("🔗 Connecting to Google Calendar MCP Server...")

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize session
                await session.initialize()
                print("✅ Connected to MCP server!")

                # List available tools
                print("\n📋 Available tools:")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                print("\n🤖 Interactive Mode Started")
                print("Type commands like:")
                print("  - list")
                print("  - schedule team sync tomorrow at 2pm with bob@example.com")
                print("  - auto project review for 45")
                print("  - quit\n")

                while True:
                    user_input = input("You: ").strip()

                    if user_input.lower() in ("quit", "exit"):
                        print("👋 Goodbye!")
                        break

                    elif user_input.lower() == "list":
                        print("📅 Fetching your upcoming meetings...")
                        result = await session.call_tool(
                            name="list_meetings",
                            arguments={"max_results": 10}
                        )
                        print("Result:", result.content[0].text)

                    elif user_input.lower().startswith("schedule "):
                        # Basic parsing: extract emails + time
                        text = user_input[9:]
                        attendees = []
                        emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
                        if emails:
                            attendees = emails

                        # crude date/time parsing
                        if "tomorrow" in text.lower():
                            start_time = datetime.utcnow() + timedelta(days=1)
                            start_time = start_time.replace(hour=14, minute=0, second=0, microsecond=0)
                        else:
                            start_time = datetime.utcnow() + timedelta(hours=1)

                        end_time = start_time + timedelta(hours=1)

                        start_iso = start_time.isoformat() + 'Z'
                        end_iso = end_time.isoformat() + 'Z'

                        result = await session.call_tool(
                            name="create_meeting",
                            arguments={
                                "summary": "Scheduled Meeting",
                                "start_time": start_iso,
                                "end_time": end_iso,
                                "description": f"Meeting requested: {text}",
                                "attendees": ",".join(attendees)
                            }
                        )
                        print("Result:", result.content[0].text)

                    elif user_input.lower().startswith("auto "):
                        text = user_input[5:]
                        # detect duration like "for 45"
                        duration = 60
                        match = re.search(r'for (\d+)', text)
                        if match:
                            duration = int(match.group(1))

                        result = await session.call_tool(
                            name="auto_schedule_meeting",
                            arguments={
                                "summary": text,
                                "duration_minutes": duration,
                                "description": f"Auto-scheduled meeting: {text}",
                                "attendees": ""
                            }
                        )
                        print("Result:", result.content[0].text)

                    else:
                        print("❓ Unknown command. Try:")
                        print("  - list")
                        print("  - schedule team sync tomorrow at 2pm with alice@example.com")
                        print("  - auto project review for 30")
                        print("  - quit")

    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        print("\n💡 Make sure you have:")
        print("  1. Installed dependencies: pip install -r requirements.txt")
        print("  2. Set up Google Calendar credentials (credentials.json + token.json)")
        print("  3. The calendar_server.py file in the same directory")


if __name__ == "__main__":
    print("🚀 Starting Google Calendar MCP Interactive Client")
    print("=" * 50)
    asyncio.run(interactive_client())
