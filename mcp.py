from fastmcp import FastMCP
import random
import requests

mcp = FastMCP("simple calculator server")

BACKEND_URL = "http://localhost:8000"  # change to your deployed backend URL

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers
    Args:
        a: First number
        b: Second number
    Returns:
        The sum of a and b
    """
    return a + b

@mcp.tool()
def get_random_number(min: int, max: int) -> int:
    """Get a random number between min and max
    Args:
        min: Minimum value
        max: Maximum value
    Returns:
        A random number between min and max
    """
    return random.randint(min, max)

@mcp.tool()
def create_campaign(campaign_name: str, target_audience: str, tone: str) -> dict:
    """Create a new outbound campaign
    Args:
        campaign_name: Name of the campaign
        target_audience: Description of the target audience
        tone: Tone of the campaign (e.g. professional, casual, friendly)
    Returns:
        Campaign details including the new campaign_id
    """
    import uuid
    campaign_id = str(uuid.uuid4())[:8]
    return {
        "campaign_id": campaign_id,
        "campaign_name": campaign_name,
        "target_audience": target_audience,
        "tone": tone,
        "status": "created",
        "message": f"Campaign '{campaign_name}' created successfully."
    }

@mcp.tool()
def get_campaign_stats(campaign_id: str) -> dict:
    """Get statistics for a campaign
    Args:
        campaign_id: The ID of the campaign
    Returns:
        Campaign statistics including opens, replies, and meetings booked
    """
    return {
        "campaign_id": campaign_id,
        "opens": random.randint(10, 500),
        "replies": random.randint(1, 50),
        "meetings_booked": random.randint(0, 10),
        "status": "active"
    }

@mcp.tool()
def get_recent_replies() -> list:
    """Get the latest email replies from leads
    Returns:
        A list of recent replies with lead_id, sender, and message preview
    """
    return [
        {"lead_id": "lead_001", "sender": "alice@example.com", "preview": "Thanks for reaching out, I'm interested!", "received_at": "2026-04-01T09:00:00Z"},
        {"lead_id": "lead_002", "sender": "bob@example.com", "preview": "Can we schedule a call this week?", "received_at": "2026-04-01T10:30:00Z"},
        {"lead_id": "lead_003", "sender": "carol@example.com", "preview": "Please remove me from this list.", "received_at": "2026-04-01T11:00:00Z"},
    ]

@mcp.tool()
def send_reply(lead_id: str, message: str) -> dict:
    """Send a reply to a lead
    Args:
        lead_id: The ID of the lead to reply to
        message: The message to send
    Returns:
        Confirmation of the sent reply
    """
    return {
        "lead_id": lead_id,
        "status": "sent",
        "message_preview": message[:100],
        "message": f"Reply sent to lead {lead_id} successfully."
    }

@mcp.tool()
def book_meeting(lead_id: str, time_slot: str) -> dict:
    """Book a meeting with a lead
    Args:
        lead_id: The ID of the lead
        time_slot: Desired time slot (e.g. '2026-04-05 14:00 UTC')
    Returns:
        Meeting confirmation details
    """
    return {
        "lead_id": lead_id,
        "time_slot": time_slot,
        "status": "booked",
        "meeting_id": f"mtg_{lead_id}_{random.randint(1000,9999)}",
        "message": f"Meeting booked with lead {lead_id} at {time_slot}."
    }

@mcp.tool()
def get_greeting() -> dict:
    """Get a welcome greeting from the backend server
    Returns:
        A greeting message from the backend
    """
    response = requests.get(f"https://test-mcp-r3tk.onrender.com/greeting")
    return response.json()

@mcp.tool()
def generate_poem(topic: str) -> dict:
    """Generate a poem about a given topic using AI
    Args:
        topic: The topic or theme for the poem
    Returns:
        A generated poem about the topic
    """
    response = requests.post(
        f"https://test-mcp-r3tk.onrender.com/generate-poem",
        params={"topic": topic}
    )
    return response.json()

@mcp.resource("resource://info")
def server_info() -> dict:
    """Get server information"""
    return {
        "name": "simple calculator server",
        "version": "1.0.0",
        "description": "A simple calculator server",
        "tools": ["add", "get_random_number", "create_campaign", "get_campaign_stats",
                  "get_recent_replies", "send_reply", "book_meeting", "get_greeting", "generate_poem"]
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="http", host="0.0.0.0", port=8081)
