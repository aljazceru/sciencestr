from nostr_sdk import Keys, Client, Event, EventBuilder, Filter, HandleNotification, Timestamp, nip04_decrypt, SecretKey, init_logger, LogLevel
import time
import requests
from settings import *
import sqlite3

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
client.add_relay("wss://a.nos.lol")
client.add_relay("wss://nostr-01.bolt.observer")
client.add_relay("wss://e.nos.lol")
client.connect()

filter = Filter().pubkey(pk).kind(4).since(Timestamp.now())
client.subscribe([filter])

# function to format results into title and url

def format_answer(response):
    # Extract the answer
    formatted_response = "Short answer:\n" + response["short_answer"] + "\n\nExcerpts from articles:\n" + response["chunks"]
    return formatted_response

# function to interact with local database
def interact_with_db(event_id, action):
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    if action == "check":
        c.execute("SELECT * FROM events WHERE id=?", (str(event_id),))
        return c.fetchone() is not None
    elif action == "insert":
        c.execute("INSERT INTO events VALUES (?)", (str(event_id),))
        conn.commit()
    conn.close()

class NotificationHandler(HandleNotification):
    def handle(self, relay_url, event):
        print(f"Received new event from {relay_url}: {event.as_json()}")
        if event.kind() == 4:
            try:
                msg = nip04_decrypt(sk, event.pubkey(), event.content())
                print(f"Received new question: {msg}")
                params = {'query': str(msg)}
                try:
                    resp = requests.get('http://127.0.0.1:6000/ask', params=params)
                    if resp.status_code == 200:
                        print("Sending answer")
                        event = EventBuilder.new_encrypted_direct_msg(keys, event.pubkey(), f"{resp.text}", event.id()).to_event(keys)
                        client.send_event(event)
                    else:
                        print(f"Error querying API: status code: {resp.status_code}, response: {resp.t}")
                except Exception as e:
                    print(f"Error during request: {e}")
                
            except Exception as e:
                print(f"Error during content decryption: {e}")

    def handle_msg(self, relay_url, msg):
        None
        
client.handle_notifications(NotificationHandler())

while True:
    time.sleep(5.0)