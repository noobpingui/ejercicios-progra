from cache import redis_client #To reuse the same client I have
from datetime import datetime, timezone  #To build the timestamp

def send_heartbeat():
    now = datetime.now(timezone.utc).isoformat()  #Current timestamp in text format
    redis_client.set("heartbeat", now, ex=60)     #To perform a set, will expire in 60 seconds and so it does not 'affect' the 'real cache'

    value = redis_client.get("heartbeat")         #To perform another commando to proof activity. In this case get, so it's not only Write but Read activity too
    print(f"Heartbeat OK - Redis response: {value}")  # log available in the workflow logs


if __name__ == "__main__":  #To run only if the script is directly executed and not when getting imported as a package
    send_heartbeat()

    