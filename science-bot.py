from nostr_sdk import Keys, Client, Event, EventBuilder, Filter, HandleNotification, Timestamp, nip04_decrypt, SecretKey, init_logger, LogLevel
import time
import requests
from settings import *


init_logger(LogLevel.DEBUG)

sk = SecretKey.from_hex(NOSTR_KEY)
keys = Keys(sk)
sk = keys.secret_key()
pk = keys.public_key()
print(f"Bot public key: {pk.to_bech32()}")

client = Client(keys)

client.add_relay("wss://relay.damus.io")
client.add_relay("wss://nostr.mom")
client.add_relay("wss://nostr.oxtr.dev")
client.connect()

filter = Filter().pubkey(pk).kind(4).since(Timestamp.now())
client.subscribe([filter])

# function to format results into title and url

def format_answer(response):
    # Extract the answer
    formatted_response = "Short answer:\n" + response["short_answer"] + "\n\nExcerpts from articles:\n" + response["chunks"]
    return formatted_response

class NotificationHandler(HandleNotification):
    def handle(self, relay_url, event):
        print(f"Received new event from {relay_url}: {event.as_json()}")
        if event.kind() == 4:
            print("Decrypting event")
            try:
                msg = nip04_decrypt(sk, event.pubkey(), event.content())
                print(f"Received new msg: {msg}")
                params = {'query': str(msg)}
                try:
                    resp = requests.get('http://127.0.0.1:6000/ask', params=params)
                except Exception as e:
                    print(f"Error during request: {e}")
                if resp.status_code == 200:
                    print("Sending answer")
                    event = EventBuilder.new_encrypted_direct_msg(keys, event.pubkey(), f"{resp.text}", event.id()).to_event(keys)
                    client.send_event(event)
                else:
                    print(f"Error during content decryption: {resp.text}")
            except Exception as e:
                print(f"Error during content decryption: {e}")

    def handle_msg(self, relay_url, msg):
        None
        
client.handle_notifications(NotificationHandler())

while True:
    time.sleep(5.0)