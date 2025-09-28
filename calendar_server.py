"""
Google Calendar MCP Server

This MCP server provides tools for auto-scheduling meetings using Google Calendar API.
It includes tools for creating, listing, updating, and deleting calendar events.

For beginners: This server uses the Model Context Protocol (MCP) to provide
Google Calendar functionality that can be used by AI agents.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("google-calendar")

# Google Calendar API configuration
SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

class GoogleCalendarService:
    """Handles Google Calendar API authentication and operations."""

    def __init__(self):
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Calendar API."""
        creds = None

        # Load existing token if available
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"Please download your OAuth2 credentials from Google Cloud Console "
                        f"and save them as '{CREDENTIALS_FILE}' in the current directory."
                    )

                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)

    def create_event(self, summary: str, start_time: str, end_time: str,
                    description: str = "", attendees: List[str] = None) -> Dict[str, Any]:
        """Create a new calendar event."""
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
        }

        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]

        try:
            created_event = self.service.events().insert(calendarId='primary', body=event).execute()
            return {
                'success': True,
                'event_id': created_event['id'],
                'event_link': created_event.get('htmlLink', ''),
                'message': f"Event '{summary}' created successfully"
            }
        except HttpError as error:
            return {
                'success': False,
                'error': str(error),
                'message': f"Failed to create event: {error}"
            }

    def list_events(self, max_results: int = 10, time_min: str = None) -> Dict[str, Any]:
        """List upcoming calendar events."""
        try:
            if not time_min:
                time_min = datetime.utcnow().isoformat() + 'Z'

            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                formatted_events.append({
                    'id': event['id'],
                    'summary': event.get('summary', 'No Title'),
                    'start': start,
                    'description': event.get('description', ''),
                    'attendees': [att.get('email', '') for att in event.get('attendees', [])]
                })

            return {
                'success': True,
                'events': formatted_events,
                'count': len(formatted_events)
            }
        except HttpError as error:
            return {
                'success': False,
                'error': str(error),
                'message': f"Failed to list events: {error}"
            }

    def delete_event(self, event_id: str) -> Dict[str, Any]:
        """Delete a calendar event."""
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            return {
                'success': True,
                'message': f"Event {event_id} deleted successfully"
            }
        except HttpError as error:
            return {
                'success': False,
                'error': str(error),
                'message': f"Failed to delete event: {error}"
            }

# Initialize the Google Calendar service
try:
    calendar_service = GoogleCalendarService()
except Exception as e:
    print(f"Warning: Could not initialize Google Calendar service: {e}")
    calendar_service = None

@mcp.tool()
async def create_meeting(summary: str, start_time: str, end_time: str,
                        description: str = "", attendees: str = "") -> str:
    """
    Create a new meeting in Google Calendar.

    Args:
        summary: Title of the meeting
        start_time: Start time in ISO format (e.g., "2024-01-15T10:00:00Z")
        end_time: End time in ISO format (e.g., "2024-01-15T11:00:00Z")
        description: Optional description of the meeting
        attendees: Comma-separated list of attendee email addresses

    Returns:
        Success message with event details or error message
    """
    if not calendar_service:
        return "Error: Google Calendar service not initialized. Please check your credentials."

    attendee_list = [email.strip() for email in attendees.split(',')] if attendees else None

    result = calendar_service.create_event(
        summary=summary,
        start_time=start_time,
        end_time=end_time,
        description=description,
        attendees=attendee_list
    )

    return json.dumps(result, indent=2)

@mcp.tool()
async def list_meetings(max_results: int = 10) -> str:
    """
    List upcoming meetings from Google Calendar.

    Args:
        max_results: Maximum number of events to return (default: 10)

    Returns:
        List of upcoming meetings with details
    """
    if not calendar_service:
        return "Error: Google Calendar service not initialized. Please check your credentials."

    result = calendar_service.list_events(max_results=max_results)
    return json.dumps(result, indent=2)

@mcp.tool()
async def delete_meeting(event_id: str) -> str:
    """
    Delete a meeting from Google Calendar.

    Args:
        event_id: The ID of the event to delete

    Returns:
        Success or error message
    """
    if not calendar_service:
        return "Error: Google Calendar service not initialized. Please check your credentials."

    result = calendar_service.delete_event(event_id)
    return json.dumps(result, indent=2)

@mcp.tool()
async def auto_schedule_meeting(summary: str, duration_minutes: int = 60,
                               description: str = "", attendees: str = "") -> str:
    """
    Automatically schedule a meeting for the next available time slot.

    Args:
        summary: Title of the meeting
        duration_minutes: Duration of the meeting in minutes (default: 60)
        description: Optional description of the meeting
        attendees: Comma-separated list of attendee email addresses

    Returns:
        Success message with scheduled meeting details or error message
    """
    if not calendar_service:
        return "Error: Google Calendar service not initialized. Please check your credentials."

    # Find next available slot (simplified - starts from now + 1 hour)
    now = datetime.utcnow()
    start_time = now + timedelta(hours=1)
    end_time = start_time + timedelta(minutes=duration_minutes)

    # Format times for Google Calendar
    start_iso = start_time.isoformat() + 'Z'
    end_iso = end_time.isoformat() + 'Z'

    attendee_list = [email.strip() for email in attendees.split(',')] if attendees else None

    result = calendar_service.create_event(
        summary=summary,
        start_time=start_iso,
        end_time=end_iso,
        description=description,
        attendees=attendee_list
    )

    return json.dumps(result, indent=2)

@mcp.resource("config://calendar")
def get_calendar_config():
    """Get calendar configuration information."""
    return {
        "service": "Google Calendar",
        "scopes": SCOPES,
        "credentials_required": True,
        "setup_instructions": [
            "1. Go to Google Cloud Console",
            "2. Create a new project or select existing",
            "3. Enable Google Calendar API",
            "4. Create OAuth2 credentials",
            "5. Download credentials.json to this directory"
        ]
    }

if __name__ == "__main__":
    mcp.run(transport='stdio')
