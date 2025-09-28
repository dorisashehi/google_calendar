"""
Simple test client for Google Calendar MCP Server

This client demonstrates how to use the Google Calendar MCP server.
It connects to the server and tests the available tools.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_calendar_server():
    """Test the Google Calendar MCP server tools."""

    # Server parameters - adjust path if needed
    server_params = StdioServerParameters(
        command="python3",
        args=["calendar_server.py"]
    )

    print("🔗 Connecting to Google Calendar MCP Server...")

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                print("✅ Connected to MCP server!")

                # List available tools
                print("\n📋 Available tools:")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")

                # Test 1: List current meetings
                print("\n📅 Testing: List current meetings")
                try:
                    result = await session.call_tool(
                        name="list_meetings",
                        arguments={"max_results": 5}
                    )
                    print("Result:", result.content[0].text)
                except Exception as e:
                    print(f"Error listing meetings: {e}")

                # Test 2: Create a test meeting
                print("\n➕ Testing: Create a test meeting")
                try:
                    from datetime import datetime, timedelta
                    now = datetime.utcnow()
                    start_time = (now + timedelta(hours=1)).isoformat() + 'Z'
                    end_time = (now + timedelta(hours=2)).isoformat() + 'Z'

                    result = await session.call_tool(
                        name="create_meeting",
                        arguments={
                            "summary": "Test Meeting from MCP",
                            "start_time": start_time,
                            "end_time": end_time,
                            "description": "This is a test meeting created by the MCP client",
                            "attendees": ""
                        }
                    )
                    print("Result:", result.content[0].text)
                except Exception as e:
                    print(f"Error creating meeting: {e}")

                # Test 3: Auto-schedule a meeting
                print("\n🤖 Testing: Auto-schedule a meeting")
                try:
                    result = await session.call_tool(
                        name="auto_schedule_meeting",
                        arguments={
                            "summary": "Auto-scheduled Meeting",
                            "duration_minutes": 30,
                            "description": "This meeting was auto-scheduled by the MCP agent",
                            "attendees": ""
                        }
                    )
                    print("Result:", result.content[0].text)
                except Exception as e:
                    print(f"Error auto-scheduling meeting: {e}")

                print("\n✅ Test completed!")

    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        print("\n💡 Make sure you have:")
        print("  1. Installed dependencies: pip install -r requirements.txt")
        print("  2. Set up Google Calendar credentials (credentials.json)")
        print("  3. The calendar_server.py file is in the same directory")

if __name__ == "__main__":
    print("🚀 Starting Google Calendar MCP Test Client")
    print("=" * 50)
    asyncio.run(test_calendar_server())
