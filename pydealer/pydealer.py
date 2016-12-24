"""
pydealer

Starts a Steam client that checks if there are any steam cards to idle
and if so loops all games that has steam cards
"""
# pylint: disable=no-member
import logging
from steam import SteamClient
from steam.enums import EResult

# setup logging
logging.basicConfig(format="%(asctime)s | %(message)s", level=logging.INFO)
LOG = logging.getLogger()

CLIENT = SteamClient()
CLIENT.set_credential_location(".")  # where to store sentry files and other stuff

@CLIENT.on("error")
def handle_error(result):
    """Reports if login got a error"""
    LOG.info("Logon result: %s", repr(result))

@CLIENT.on("channel_secured")
def send_login():
    """Checks if it is possible to login again"""
    if CLIENT.relogin_available:
        CLIENT.relogin()

@CLIENT.on("connected")
def handle_connected():
    """Successfully connected"""
    LOG.info("Connected to %s", CLIENT.current_server_addr)

@CLIENT.on("reconnect")
def handle_reconnect(delay):
    """How long until reconnecting"""
    LOG.info("Reconnect in %ds...", delay)

@CLIENT.on("disconnected")
def handle_disconnect():
    """Disconnected from Steamclient"""
    LOG.info("Disconnected.")

    if CLIENT.relogin_available:
        LOG.info("Reconnecting...")
        CLIENT.reconnect(maxdelay=30)

@CLIENT.on("logged_on")
def handle_after_logon():
    """What to do when successfully logged in"""
    LOG.info("-"*30)
    LOG.info("Logged on as: %s", CLIENT.user.name)
    LOG.info("Community profile: %s", CLIENT.steam_id.community_url)
    LOG.info("Last logon: %s", CLIENT.user.last_logon)
    LOG.info("Last logoff: %s", CLIENT.user.last_logoff)
    LOG.info("Last logoff: %s", CLIENT.games_played([40420]))
    LOG.info("-"*30)
    LOG.info("Press ^C to exit")


# main bit
LOG.info("Persistent logon recipe")
LOG.info("-"*30)

try:
    RESULT = CLIENT.cli_login()

    if RESULT != EResult.OK:
        LOG.info("Failed to login: %s", repr(RESULT))
        raise SystemExit

    CLIENT.run_forever()
except KeyboardInterrupt:
    if CLIENT.connected:
        LOG.info("Logout")
        CLIENT.logout()
