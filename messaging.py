"""
Messaging integration module for WhatsApp and Google Chat.
Requires environment variables to be set for API credentials.
"""

import os
import requests
# from twilio.rest import Client


class MessagingService:
    """Handle message delivery via WhatsApp and Google Chat."""

    def __init__(self):
        """Initialize messaging service with credentials from environment."""
        # Twilio credentials for WhatsApp
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

        # Google Chat webhook URL
        self.google_chat_webhook = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")

        # Personal contact info
        self.recipient_phone = os.getenv("RECIPIENT_WHATSAPP_NUMBER", "+27795510741")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL", "tebza27@gmail.com")

    def send_whatsapp(self, sender_name, sender_email, message_text):
        """Send message via WhatsApp using Twilio."""
        if not self.twilio_account_sid or not self.twilio_auth_token:
            return {
                "success": False,
                "error": "WhatsApp API not configured. Set Twilio credentials.",
            }

        try:
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            message = client.messages.create(
                from_=f"whatsapp:{self.twilio_from_number}",
                body=f"New message from portfolio:\n\nFrom: {sender_name}\nEmail: {sender_email}\n\nMessage:\n{message_text}",
                to=f"whatsapp:{self.recipient_phone}",
            )
            return {"success": True, "sid": message.sid}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_google_chat(self, sender_name, sender_email, message_text):
        """Send message via Google Chat using webhook."""
        if not self.google_chat_webhook:
            return {
                "success": False,
                "error": "Google Chat webhook not configured.",
            }

        try:
            payload = {
                "text": (
                    f"📧 New Contact Form Submission\n\n"
                    f"From: {sender_name}\n"
                    f"Email: {sender_email}\n\n"
                    f"Message:\n{message_text}"
                )
            }
            response = requests.post(self.google_chat_webhook, json=payload, timeout=10)
            response.raise_for_status()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_email(self, sender_name, sender_email, message_text):
        """Placeholder for email integration (can use SendGrid, etc.)."""
        # TODO: Implement email via SendGrid, AWS SES, or similar
        return {
            "success": False,
            "error": "Email integration not yet configured.",
        }


def get_messaging_service():
    """Factory function to get messaging service instance."""
    print("Messaging disabled")
