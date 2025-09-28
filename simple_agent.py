"""
Simple AI Agent using Google Calendar MCP Server

This demonstrates how to use the Google Calendar MCP server with a simple AI agent
that can understand natural language and schedule meetings automatically.
"""

import asyncio
import json
from datetime import datetime, timedelta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class CalendarAgent:
    """Simple AI agent that can schedule meetings using natural language."""

    def __init__(self):
        self.session = None

    async def connect(self):
        """Connect to the Google Calendar MCP server."""
        server_params = StdioServerParameters(
            command="python3",
            args=["calendar_server.py"]
        )

        self.stdio_client = stdio_client(server_params)
        self.read, self.write = await self.stdio_client.__aenter__()
        self.session = ClientSession(self.read, self.write)
        await self.session.initialize()
        print("✅ Connected to Google Calendar MCP Server")

    async def disconnect(self):
        """Disconnect from the server."""
        if self.session:
            await self.session.close()
        if hasattr(self, 'stdio_client'):
            await self.stdio_client.__aexit__(None, None, None)

    async def schedule_meeting(self, request: str) -> str:
        """
        Schedule a meeting based on natural language request.

        Args:
            request: Natural language request like "Schedule a meeting tomorrow at 2pm for 1 hour"

        Returns:
            Response about the scheduled meeting
        """
        try:
            # Simple parsing - in a real agent, you'd use NLP
            if "tomorrow" in request.lower():
                start_time = datetime.utcnow() + timedelta(days=1)
                start_time = start_time.replace(hour=14, minute=0, second=0, microsecond=0)
            else:
                start_time = datetime.utcnow() + timedelta(hours=1)

            end_time = start_time + timedelta(hours=1)

            # Format for Google Calendar
            start_iso = start_time.isoformat() + 'Z'
            end_iso = end_time.isoformat() + 'Z'

            # Extract meeting title
            title = "Meeting"
            if "meeting" in request.lower():
                # Simple extraction - in real agent, use proper NLP
                words = request.split()
                if len(words) > 1:
                    title = " ".join(words[:3])  # Take first few words as title

            result = await self.session.call_tool(
                name="create_meeting",
                arguments={
                    "summary": title,
                    "start_time": start_iso,
                    "end_time": end_iso,
                    "description": f"Meeting scheduled via AI agent: {request}",
                    "attendees": ""
                }
            )

            return result.content[0].text

        except Exception as e:
            return f"Error scheduling meeting: {e}"

    async def list_my_meetings(self) -> str:
        """List upcoming meetings."""
        try:
            result = await self.session.call_tool(
                name="list_meetings",
                arguments={"max_results": 10}
            )
            return result.content[0].text
        except Exception as e:
            return f"Error listing meetings: {e}"

    async def auto_schedule(self, title: str, duration: int = 60) -> str:
        """Auto-schedule a meeting for the next available slot."""
        try:
            result = await self.session.call_tool(
                name="auto_schedule_meeting",
                arguments={
                    "summary": title,
                    "duration_minutes": duration,
                    "description": f"Auto-scheduled meeting: {title}",
                    "attendees": ""
                }
            )
            return result.content[0].text
        except Exception as e:
            return f"Error auto-scheduling: {e}"

async def interactive_demo():
    print("hello")
    """Interactive demo of the Calendar Agent."""
    agent = CalendarAgent()

    try:
        await agent.connect()

        print("🤖 Google Calendar AI Agent Demo")
        print("=" * 40)
        print("Available commands:")
        print("  - 'schedule [description]' - Schedule a meeting")
        print("  - 'list' - List upcoming meetings")
        print("  - 'auto [title]' - Auto-schedule a meeting")
        print("  - 'quit' - Exit")
        print()

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'list':
                print("Agent: Let me check your upcoming meetings...")
                response = await agent.list_my_meetings()
                print(f"Agent: {response}")
            elif user_input.lower().startswith('auto '):
                title = user_input[5:]  # Remove 'auto ' prefix
                print(f"Agent: Auto-scheduling '{title}'...")
                response = await agent.auto_schedule(title)
                print(f"Agent: {response}")
            elif user_input.lower().startswith('schedule '):
                request = user_input[9:]  # Remove 'schedule ' prefix
                print(f"Agent: Scheduling meeting: {request}")
                response = await agent.schedule_meeting(request)
                print(f"Agent: {response}")
            else:
                print("Agent: I can help you schedule meetings! Try:")
                print("  - 'schedule team meeting tomorrow'")
                print("  - 'list' to see your meetings")
                print("  - 'auto project review' to auto-schedule")

            print()

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have:")
        print("  1. Set up Google Calendar credentials")
        print("  2. The calendar_server.py is running")

    finally:
        await agent.disconnect()

if __name__ == "__main__":
    print("🚀 Starting Google Calendar AI Agent")
    asyncio.run(interactive_demo())
