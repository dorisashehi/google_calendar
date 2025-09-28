# Google Calendar MCP Agent

A simple Model Context Protocol (MCP) server that provides Google Calendar integration for auto-scheduling meetings. Perfect for beginners to understand MCP concepts!

## What is MCP?

MCP (Model Context Protocol) is a way for AI agents to use tools and access external services. Think of it as a bridge between AI and real-world applications like Google Calendar.

## What This Agent Can Do

🤖 **Auto-schedule meetings** - The AI can understand natural language and create calendar events
📅 **List meetings** - See your upcoming meetings
✏️ **Manage meetings** - Create, update, and delete calendar events
🔗 **Google Calendar integration** - Direct connection to your Google Calendar

## Quick Start (For Beginners)

### 1. Install Dependencies

```bash
cd goole_meetings
pip install -r requirements.txt
```

### 2. Set Up Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create OAuth2 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
   - Choose "Desktop application"
   - Download the JSON file
5. Rename the downloaded file to `credentials.json` and place it in this directory

### 3. Test the Server

```bash
# Test the MCP server directly
python test_client.py
```

### 4. Try the AI Agent

```bash
# Run the interactive AI agent
python simple_agent.py
```

## How to Use

### Basic Commands

```bash
# List your meetings
You: list

# Schedule a meeting
You: schedule team meeting tomorrow at 2pm

# Auto-schedule a meeting
You: auto project review meeting
```

### Direct MCP Tools

The server provides these tools:

- `create_meeting` - Create a new meeting
- `list_meetings` - List upcoming meetings
- `delete_meeting` - Delete a meeting
- `auto_schedule_meeting` - Auto-schedule for next available slot

## File Structure

```
goole_meetings/
├── calendar_server.py    # Main MCP server
├── test_client.py        # Simple test client
├── simple_agent.py       # AI agent demo
├── requirements.txt      # Dependencies
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

## Understanding the Code

### MCP Server (`calendar_server.py`)

```python
# This creates an MCP server
mcp = FastMCP("google-calendar")

# This creates a tool that AI can use
@mcp.tool()
async def create_meeting(summary: str, start_time: str, end_time: str):
    # Tool implementation here
    pass
```

### AI Agent (`simple_agent.py`)

```python
# The agent connects to the MCP server
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Use the tools
        result = await session.call_tool("create_meeting", arguments={...})
```

## Troubleshooting

### Common Issues

1. **"Credentials not found"**

   - Make sure `credentials.json` is in the directory
   - Check that you downloaded OAuth2 credentials (not API key)

2. **"Permission denied"**

   - Make sure you granted calendar permissions during OAuth
   - Check that Google Calendar API is enabled

3. **"Connection failed"**
   - Make sure all dependencies are installed
   - Check that the server starts without errors

### Getting Help

- Check the console output for error messages
- Make sure your Google account has calendar access
- Verify that the OAuth flow completed successfully

## Next Steps

Once you understand this basic example, you can:

1. **Add more features** - Meeting reminders, recurring events, etc.
2. **Improve the AI** - Better natural language understanding
3. **Add integrations** - Connect to other services
4. **Create your own MCP server** - For other APIs and services

## Learning Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Google Calendar API](https://developers.google.com/calendar)
- [FastMCP](https://fastmcp.cloud/) - Easy MCP server creation

Happy coding! 🚀
