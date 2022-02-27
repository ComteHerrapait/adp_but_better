# Enable debug logging
import logging
import sys

from slack_sdk.errors import SlackApiError

logging.basicConfig(level=logging.WARNING)
# Verify it works
from slack_sdk import WebClient

client = WebClient()
client.oauth_v2_access(
    client_id="2541715624.3127813182465",
    client_secret="59c661a26f77bb3313bcdde0bfb1f03b",
)
print(client.api_test())
status = client.users_profile_get()
print(status)
