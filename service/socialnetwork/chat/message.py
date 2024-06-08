from gameblog.redis_connection import r

class Message:
    def __init__(self, sender, receiver, message, created_at):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.created_at = created_at

  