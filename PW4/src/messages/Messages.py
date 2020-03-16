class Messages:
    """Message class.
    This class implements the message object which is exchanged between agent
    during communication.
    attr:
    sender: the sender of the message
    receiver: the receiver of the message
    message_performative: the performative of the message
    content: the content of the message
    """

    def __init__(self, sender, receiver, message_performative, content):
        self.sender = sender
        self.receiver = receiver
        self.performative = message_performative
        self.content = content
        self.info = [self.receiver, self.content]
        self.argu = []

    def get_perf_n_content(self):
        return [self.performative, self.content]

    def get_infos(self):
        return self.info

    def get_perf(self):
        return self.performative

    def get_content(self):
        return self.content
