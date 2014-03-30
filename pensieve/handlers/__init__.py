from .handshake import Handshake
from .image import Image
from .speech_to_text import SpeechToText


messageHandlers = {
    'handshake': Handshake(),
    'image': Image(),
    'stt': SpeechToText()
    }
