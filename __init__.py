import os

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft.audio import wait_while_speaking 

__author__ = 'Chirag'

class WhatCanYouDoSkill(MycroftSkill):

    def __init__(self):
        super(WhatCanYouDoSkill, self).__init__(name="WhatCanYouDoSkill")
        
    @intent_handler(IntentBuilder("").require("What").require("Can").require("Do"))
    def handle_what_can_do__intent(self, message):
        # tell user what he can do
        self.speak_dialog("what.i.can") 
        
        # execute function getSkills -> get list of installed skills
        self.getSkills() 

    def getSkills(self):
        # get list of skills via msm and search for "installed"
        self.myskills = os.popen('msm list | grep installed').read() 
        self.myskills = self.myskills.replace('\n', ', ').replace('\r', ', ').replace('[installed],', ',').replace('\t', '') # replace unwanted characters and make nice list
        # get number of skills
        nr_skills = len(self.myskills.split()) 

        if nr_skills < 1: # if msm did not give us what we want (no matter why) do alternative skill search
           self.myskills = os.popen('ls /opt/mycroft/skills/').read() # Get folders in /opt/mycroft/skills
           self.myskills = self.myskills.replace('\n', ', ').replace('\r', ', ').replace('\t', '') # replace unwanted characters and make nice list
           nr_skills = len(self.myskills.split()) # get number of skills
        
        if nr_skills < 1: # if msm and alternative skill search fails than tell user that we couldn't do the job
           wait_while_speaking() # always wait
           self.speak_dialog("not.found") # tell user that we couldn't do the job
           return # if all fails, return
        # always wait
        wait_while_speaking() 
        # we found skills -> yeah. tell user how many!
        self.speak_dialog('found', {'nrskills': nr_skills}) 
        # always wait
        wait_while_speaking() 
        # ask user if we should give him a list of all his skills.
        self.should_getskills = self.get_response('ask.getskills') 
        # get list of confirmation words
        self.yes_words = set(self.translate_list('yes')) 
        # execute function listSkills -> if user confirmed -> give him a list of all his skills, else -> exit
        self.listSkills() 
      
    def listSkills(self):
        if self.should_getskills: # if user said something
           resp_getskills = self.should_getskills.split() # split user sentence into list
           if any(word in resp_getskills for word in self.yes_words): # if any of the words from the user sentences is yes
              self.speak_dialog('my.skills') # Introduction that we will give user list of skills
              self.speak(self.myskills.strip()) # tell user list of skills
           else: # no word in sentence from user was yes
              self.speak_dialog('no.skills') # give user feedback

    def shutdown(self):
        super(WhatCanYouDoSkill, self).shutdown()

    def stop(self):
        pass

def create_skill():
    return WhatCanYouDoSkill()
