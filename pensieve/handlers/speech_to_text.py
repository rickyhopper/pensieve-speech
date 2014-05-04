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
    directoryPath = None

    def handle(self, header, data):
        #ensure the request contains the necessary data
        try:
            sampleRate = checkField(header, 'sample_rate')
            numBytes = checkField(header, 'num_bytes')
        except MessageError as e:
            return e.json

        #create directory path for file if there is none
        if self.directoryPath == None:
            path, thisName = os.path.split(os.path.abspath(__file__))
            path += os.sep + datetime.today().isoformat().replace(':','-')
            os.system("mkdir " + path)
            path += os.sep
            self.directoryPath = path
        #create a new file with a unique filepath
        fName = "sound-" + datetime.today().isoformat().replace(':','-');
        m4aFile = open(self.directoryPath + fName + ".m4a", "wb")
        m4aFile.write(data)
        m4aFile.close()
        """
        NOTE: I may have to synchronize this block of the program if we end up doing async processing...
        Otherwise, it will be bad times
        NOTE 2: Concatenating flac files isn't working, so I'm concatenating everything in m4a format
        and then converting the final result to flac for processing.
        """
        os.system("rm " + self.directoryPath + "list.txt")

        if self.audio == None:
            os.system("cp " + self.directoryPath + fName + ".m4a " + self.directoryPath + "workingAudio.m4a")
        else:
            os.system("mv " + self.directoryPath + "workingAudio.m4a " + self.directoryPath + "workingAudio_temp.m4a")
            os.system("echo file '" + self.directoryPath + "workingAudio_temp.m4a' >> " + self.directoryPath + "list.txt")
            os.system("echo file '" + self.directoryPath + fName + ".m4a' >> " + self.directoryPath + "list.txt")
            os.system("ffmpeg -f concat -i " + self.directoryPath + "list.txt -c copy " + self.directoryPath + "workingAudio.m4a")
            os.system("rm " + self.directoryPath + "workingAudio_temp.m4a")
        #run ffmpeg to convert to flac
        os.system("ffmpeg -i " + self.directoryPath + "workingAudio.m4a -acodec flac -ab 16k " + self.directoryPath + "workingAudio.flac")
        #get bytes from working stream
        flacFile = open(self.directoryPath + "workingAudio.flac", "rb")
        flacData = flacFile.read()
        flacFile.close()
        """
        Synchronized block should end here, if/when it's needed
        """
        #set working audio stream
        self.audio = flacData

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
            jsonData = json.loads(str(response).split('\n')[1])
            print jsonData
            if (len(jsonData["result"]) > 0):
                #words found
                #reduce working audio stream to only the most recent file
                os.system("rm " + self.directoryPath + "workingAudio.m4a")
                os.system("mv " + self.directoryPath + fName + ".m4a " + self.directoryPath + "workingAudio.m4a")
            else:
                os.system("rm " + self.directoryPath + fName + ".m4a")
            ret = json.dumps(jsonData)
            os.system("rm " + self.directoryPath + "workingAudio.flac")
            return ret
        except Exception as e:
            print e
            os.system("rm " + self.directoryPath + fName + ".m4a")
            os.system("rm " + self.directoryPath + "workingAudio.flac")
            return invalidValue("life")
