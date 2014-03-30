import cv2
import cv2.cv as cv
import numpy as np
import urllib2
import sys
import json
from datetime import datetime
import os
import subprocess
from threading import Thread

from .base_handler import BaseHandler
from ..helpers import ok, invalidValue, checkField, MessageError


class SpeechToText(BaseHandler):
    audio = None

    def handle(self, header, data):
        #ensure the request contains the necessary data
        try:
            sampleRate = checkField(header, 'sample_rate')
            numBytes = checkField(header, 'num_bytes')
        except MessageError as e:
            return e.json

        #create directory path for file
        directoryPath, thisName = os.path.split(os.path.abspath(__file__))
        directoryPath += os.sep
        #create a new file with a unique filepath
        fName = "sound-" + datetime.today().isoformat().replace(':','-');
        m4aFile = open(directoryPath + fName + ".m4a", "wb")
        m4aFile.write(data)
        m4aFile.close()
        #run ffmpeg to convert to flac
        os.system("ffmpeg -i " + directoryPath + fName + ".m4a -acodec flac -ab 16k " + directoryPath + fName + ".flac")
        #get bytes from flac file
        flacFile = open(directoryPath + fName + ".flac", "rb")
        flacData = flacFile.read()
        flacFile.close()
        #append flac file to working audio stream
        if self.audio == None:
            self.audio = flacData
        else:
            self.audio = self.audio + flacData

        print "Sending audio"

        req = urllib2.Request('https://www.google.com/speech-api/v2/recognize?client=chromium&lang=en-US&key=AIzaSyCnl6MRydhw_5fLXIdASxkLJzcJh5iX0M4', data=self.audio, headers={'Content-Type': 'audio/x-flac; rate=16000;'})

        try:
            #run the request
            result = urllib2.urlopen(req)
        except urllib2.URLError:
            print "Problem encountered analyzing audio... whoops"
            return invalidValue("audio")

        print "Received result"

        response = result.read()
        print response

        try:
            #ensure response is json-formatted (for some reason, this is needed)
            ret = json.dumps(json.loads(str(response)))
        except Exception as e:
            print e
            return invalidValue("life")

        return ret

