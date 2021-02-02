import json
import jsonpickle
import binascii
import base64
from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.util import get_ipc_directory
from mycroft.util.log import LOG
from mycroft.util.parse import normalize
from mycroft import intent_file_handler
from ovos_utils.messagebus import get_mycroft_bus, listen_for_message
from ovos_utils import wait_for_exit_signal
from ovos_utils.lang import get_tts

import os
import subprocess
from queue import Queue, Empty

class RemoteTTS(MycroftSkill):
    """
        The skill handles remote TTS 
        implementation in Mycroft Core
    """
    def __init__(self):
        super().__init__('RemoteTTS')
    
    def initialize(self):
        listen_for_message("speak", self.send_audio_data, bus=self.bus)
        
    def send_audio_data(self, message):
        utterance = message.data["utterance"]
        audio_loc = get_tts(utterance)
        with open(audio_loc, 'rb') as f:
            content = f.read()
        audio_data = content.hex()
        con_utf = bytearray.fromhex(audio_data)
        bmessage = base64.b64encode(con_utf)
        send_barray = jsonpickle.encode(bmessage)
        self.bus.emit(Message("remote.tts.audio", {"wave": send_barray}))

def create_skill():
    return RemoteTTS()
