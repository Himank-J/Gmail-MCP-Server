import argparse
import asyncio
import logging, sys
from mcp.types import TextContent
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from gmail_server import GmailService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# instantiate an MCP server client
mcp = FastMCP("Gmail Manager")

# Initialize Gmail service
gmail_service = None

@mcp.tool()
async def send_email(recipient_id: str, subject: str, message: str) -> dict:
    """Send an email to the specified recipient"""
    try:
        result = await gmail_service.send_email(recipient_id, subject, message)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Email sent successfully. Message ID: {result['message_id']}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error sending email: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def get_unread_emails() -> dict:
    """Retrieve all unread emails"""
    try:
        emails = await gmail_service.get_unread_emails()
        return {
            "content": [
                TextContent(
                    type="text",
                    text=str(emails),
                    artifact={"type": "json", "data": emails}
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error retrieving unread emails: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def read_email(email_id: str) -> dict:
    """Read the content of a specific email"""
    try:
        email_content = await gmail_service.read_email(email_id)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=str(email_content),
                    artifact={"type": "dictionary", "data": email_content}
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error reading email: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def trash_email(email_id: str) -> dict:
    """Move an email to trash"""
    try:
        result = await gmail_service.trash_email(email_id)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=result
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error moving email to trash: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def open_email(email_id: str) -> dict:
    """Open an email in the browser"""
    try:
        result = await gmail_service.open_email(email_id)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=result
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening email: {str(e)}"
                )
            ]
        }

@mcp.prompt()
def manage_email() -> list[base.Message]:
    """Prompt for managing emails"""
    return [
        base.UserMessage("You are an email administrator. You can draft, edit, read, trash, open, and send emails."),
        base.UserMessage("You've been given access to a specific gmail account."),
        base.UserMessage("You have the following tools available:"),
        base.UserMessage("- Send an email (send-email)"),
        base.UserMessage("- Retrieve unread emails (get-unread-emails)"),
        base.UserMessage("- Read email content (read-email)"),
        base.UserMessage("- Trash email (trash-email)"),
        base.UserMessage("- Open email in browser (open-email)"),
        base.UserMessage("Never send an email draft or trash an email unless the user confirms first."),
        base.UserMessage("Always ask for approval if not already given."),
        base.AssistantMessage("I understand. I'll help you manage your emails. What would you like me to do?")
    ]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gmail API MCP Server')
    parser.add_argument('--creds-file-path',
                        required=True,
                        help='OAuth 2.0 credentials file path')
    parser.add_argument('--token-path',
                        required=True,
                        help='File location to store and retrieve access and refresh tokens')
    
    args = parser.parse_args()
    
    # Initialize Gmail service
    gmail_service = GmailService(args.creds_file_path, args.token_path)
    
    # Check if running with mcp dev command
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution 