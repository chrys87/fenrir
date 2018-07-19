#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# HTTP + URL packages
import httplib2
from urllib.parse import urlencode, quote # For URL creation
import time
# To play wave files
import pygame
import math # For ceiling


# Mary server informations
mary_host = "127.0.0.1"
mary_port = "59125"

# Input text
input_text = "das ist ein test das ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testdas ist ein testd"
# Build the query
query_hash = {"INPUT_TEXT":input_text,
              "INPUT_TYPE":"TEXT", # Input text
              "LOCALE":"de",
              "VOICE":"bits3", # Voice informations  (need to be compatible)
              "OUTPUT_TYPE":"AUDIO",
              "AUDIO":"WAVE", # Audio informations (need both)
              }
starttime = time.time()
query = urlencode(query_hash)
#print("query = \"http://%s:%s/process?%s\"" % (mary_host, mary_port, query))

# Run the query to mary http server
h_mary = httplib2.Http()
#print("http://%s:%s/process?" % (mary_host, mary_port), "POST", query)
resp, content = h_mary.request("http://%s:%s/process?" % (mary_host, mary_port), "POST", query)

#  Decode the wav file or raise an exception if no wav files
if (resp["content-type"] == "audio/x-wav"):
    # Write the wav file
    f = open("/tmp/output_wav.wav", "wb")
    f.write(content)
    f.close()
    # Play the wav file
    pygame.mixer.init(frequency=16000) # Initialise the mixer
    #s = pygame.mixer.Sound(content)    
    s = pygame.mixer.Sound("/tmp/output_wav.wav")
    print(str(time.time() -starttime))
    s.play()
    print(str(time.time() -starttime))    
    pygame.time.wait(int(math.ceil(s.get_length() * 1000)))

else:
    raise Exception(content)
