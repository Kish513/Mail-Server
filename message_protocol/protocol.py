import json
import socket

class message_protocol:
    def __init__(self, data_dict):
        self.data_dict = data_dict
    
    def to_json(self):
        #add the protocol and then for every key and value in the dict add a json quarry with the key and value
        return json.dumps({**self.data_dict})
    
    def encode_message(self):
        return self.to_json().encode()
    
    def get_message(self):
        return self.to_json().encode()
    
    def decode_message(self, encoded_message):
        return json.loads(encoded_message.decode())