"""
Interactive CLI client for Google Calendar MCP Server

Supports: list_meetings, create_meeting, auto_schedule_meeting, delete_meeting
"""

import asyncio
import re
import dateparser  # NEW: for natural language date/time parsing
from datetime import datetime, timedelta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


OPTIONS_MENU = """
Choose one of these options:
  1. list → Show upcoming meetings
  2. schedule <title> on <date/time> with <email> → Create a meeting
     e.g., "schedule project kickoff on 2025-10-05 at 15:30 with alice@example.com"
     e.g., "schedule sync tomorrow at 3pm with bob@example.com"
  3. auto <title> for <minutes> → Auto-schedule a meeting
  4. delete <event_id> → Delete a meeting by ID
  5. quit → Exit
"""


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

                print("\n🤖 Google Calendar MCP Client")
                print("=" * 40)
                print(OPTIONS_MENU)

                while True:
                    user_input = input("You: ").strip()

                    # Exit
                    if user_input.lower() in ("quit", "exit", "5"):
                        print("👋 Goodbye!")
                        break

                    # List meetings
                    elif user_input.lower() in ("list", "1"):
                        result = await session.call_tool(
                            name="list_meetings",
                            arguments={"max_results": 10}
                        )
                        print("Result:", result.content[0].text)
                        print(OPTIONS_MENU)

                    # Create meeting
                    elif user_input.lower().startswith("schedule ") or user_input.startswith("2 "):
                        text = user_input[9:] if user_input.lower().startswith("schedule ") else user_input[2:]
                        attendees = []
                        emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
                        if emails:
                            attendees = emails

                        # Try parsing any natural date/time expression
                        parsed_time = dateparser.parse(text)

                        if parsed_time:
                            start_time = parsed_time
                        else:
                            print("⚠️ Could not parse date/time, defaulting to 1 hour from now.")
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
                        print(OPTIONS_MENU)

                    # Auto-schedule meeting
                    elif user_input.lower().startswith("auto ") or user_input.startswith("3 "):
                        text = user_input[5:] if user_input.lower().startswith("auto ") else user_input[2:]
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
                        print(OPTIONS_MENU)

                    # Delete meeting
                    elif user_input.lower().startswith("delete ") or user_input.startswith("4 "):
                        event_id = user_input[7:] if user_input.lower().startswith("delete ") else user_input[2:]
                        event_id = event_id.strip()

                        if not event_id:
                            print("⚠️ You must provide an event_id (get it from the 'list' command).")
                        else:
                            result = await session.call_tool(
                                name="delete_meeting",
                                arguments={"event_id": event_id}
                            )
                            print("Result:", result.content[0].text)
                        print(OPTIONS_MENU)

                    # Invalid option
                    else:
                        print("\n❌ Doesn’t match.")
                        print(OPTIONS_MENU)

    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        print("\n💡 Make sure you have:")
        print("  1. Installed dependencies: pip install -r requirements.txt")
        print("  2. Installed dateparser: pip install dateparser")
        print("  3. Set up Google Calendar credentials (credentials.json + token.json)")
        print("  4. The calendar_server.py file is in the same directory")


if __name__ == "__main__":
    print("🚀 Starting Google Calendar MCP Interactive Client")
    print("=" * 50)
    asyncio.run(interactive_client())
