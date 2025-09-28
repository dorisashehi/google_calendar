# Google Calendar MCP Setup Guide

This guide will help you set up the Google Calendar MCP agent step by step.

## Prerequisites

- Python 3.10 or higher
- A Google account
- Basic understanding of command line

## Step 1: Google Cloud Console Setup

### 1.1 Create a Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: "MCP Calendar Agent"
4. Click "Create"

### 1.2 Enable Google Calendar API

1. In the left sidebar, go to "APIs & Services" → "Library"
2. Search for "Google Calendar API"
3. Click on it and press "Enable"

### 1.3 Create OAuth2 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in app name: "MCP Calendar Agent"
   - Add your email as developer contact
   - Save and continue through the steps
4. For Application type, choose "Desktop application"
5. Name it "MCP Calendar Client"
6. Click "Create"
7. **Important**: Download the JSON file and rename it to `credentials.json`
8. Place `credentials.json` in your `goole_meetings` directory

## Step 2: Install Dependencies

```bash
# Navigate to the project directory
cd /home/dorisa/Public/AI/MCP/goole_meetings

# Install Python dependencies
pip install -r requirements.txt
```

## Step 3: Test the Setup

### 3.1 Test the MCP Server

```bash
python test_client.py
```

**Expected output:**

- Connection successful message
- List of available tools
- Test results for each tool

### 3.2 Test the AI Agent

```bash
python simple_agent.py
```

**Try these commands:**

- `list` - See your meetings
- `schedule team meeting tomorrow` - Schedule a meeting
- `auto project review` - Auto-schedule a meeting
- `quit` - Exit

## Step 4: Understanding the Code

### MCP Server Structure

```python
# 1. Import MCP framework
from mcp.server.fastmcp import FastMCP

# 2. Create server instance
mcp = FastMCP("google-calendar")

# 3. Define tools (functions AI can use)
@mcp.tool()
async def create_meeting(summary: str, start_time: str, end_time: str):
    # Tool implementation
    pass

# 4. Run the server
if __name__ == "__main__":
    mcp.run(transport='stdio')
```

### AI Agent Structure

```python
# 1. Connect to MCP server
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # 2. Use tools
        result = await session.call_tool("create_meeting", arguments={...})
```

## Common Issues and Solutions

### Issue: "Credentials not found"

**Solution:**

- Make sure `credentials.json` is in the correct directory
- Check the file name is exactly `credentials.json` (not `credentials.json.json`)

### Issue: "Permission denied"

**Solution:**

- During first run, a browser window will open for OAuth
- Grant calendar permissions to the application
- The `token.json` file will be created automatically

### Issue: "Module not found"

**Solution:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "Connection failed"

**Solution:**

- Check that `calendar_server.py` runs without errors
- Make sure all dependencies are installed
- Verify Python version is 3.10+

## Next Steps

Once everything works:

1. **Customize the agent** - Modify `simple_agent.py` to add new features
2. **Add more tools** - Create additional MCP tools in `calendar_server.py`
3. **Integrate with other services** - Add email, Slack, etc.
4. **Deploy** - Run on a server for 24/7 availability

## Understanding MCP Concepts

### What is MCP?

- **Model Context Protocol** - Standard for AI agents to use tools
- **Bridges AI and real applications** - Like Google Calendar, databases, APIs
- **Tool-based** - AI can call functions to perform actions

### Key Components:

1. **MCP Server** - Provides tools (like our calendar functions)
2. **MCP Client** - Uses the tools (like our AI agent)
3. **Tools** - Functions that AI can call
4. **Resources** - Data that AI can access

### Why Use MCP?

- **Standardized** - Works with any AI model
- **Secure** - Controlled access to tools
- **Extensible** - Easy to add new capabilities
- **Beginner-friendly** - Simple to understand and use

## Success Indicators

✅ **Setup Complete When:**

- `python test_client.py` runs without errors
- `python simple_agent.py` starts and responds to commands
- You can see your Google Calendar events
- You can create new meetings through the agent

🎉 **Congratulations!** You now have a working MCP agent that can manage your Google Calendar!
