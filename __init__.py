from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
import subprocess

#TEMPERATURE METHOD
def temp():
    scale = ""
    output = subprocess.getoutput("/opt/vc/bin/vcgencmd measure_temp")
    
    #Devide and keep only the <<number'C>>
    output = output.split('=',2)
    output= output[1]
    #Devide again to keep only the number
    output = output.split("'",2)
    temp = output[0]
    scale = output[1]
    
    if scale == "C":
        scale = "celsius"
    elif scale == "F":
        scale = "fahrenheit"
    elif scale == "K":
        scale = "kelvin"
    
    
    return temp , scale

#RAM METHOD
def ram(word):
    total = subprocess.getoutput("cat /proc/meminfo | awk 'FNR == 1 {print $2}'")
    free = subprocess.getoutput("cat /proc/meminfo | awk 'FNR == 3 {print $2}'")
    total  = int(total) / 1000
    free = int(free) / 1000
    used = total - free
    
    used_perc = ((total - free) / total) * 100
    free_perc = (free / total) * 100
    
   
    if word == "free":
        output_num = free
        output_perc = free_perc
    elif word == "used":
        output_num = used
        output_perc = used_perc
    
    
    return int(output_num) , round(output_perc,1)
    

#DISK METHOD
def disk():
    scale = ""
    
    #Used disk memory percentage
    used_perc = subprocess.getoutput("df -h | awk 'FNR == 2 {print $5}'")
    used = used_perc.split('%',1)
    used = used[0]
    
    #Free memory in GB or MB
    free = subprocess.getoutput("df -h | awk 'FNR == 2 {print $4}'")
    if "G" in free:
        scale = "gigabytes"
        output = free.split("G",2)
    elif "M" in free:
        scale = "megabytes"
        output = free.split("M",2)
    free_number = output[0]
    
    return used , free_number , scale
    
    
    
class RpiInfo(MycroftSkill):
    
    def __init__(self):
        super().__init__()
        self.learning = True
        
    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        my_setting = self.settings.get('my_setting')

    
    #FREE MEMORY HANDLER
    @intent_handler('memory_free.intent')
    def handle_free_memory(self, message):
        try:
            
            memory_num , memory_perc = ram("free")
        
            self.speak_dialog('memory_free',{'number': memory_num ,'number_perc': memory_perc })
            #self.speak_dialog('hello')
        except:
            self.speak.dialog('error')
    
    
    #USED MEMORY HANDLER
    @intent_handler('memory_used.intent')
    def handle_used_memory(self, message):
        try:
            
            memory_num , memory_perc = ram("used")
        
            self.speak_dialog('memory_used',{'number':memory_num , 'number_perc': memory_perc })
        except:
            self.speak.dialog('error')
            
            
    #TEMPERATURE HANDLER        
    @intent_handler('temperature.intent')
    def handle_temp(self, message):
        a , b = temp()
        try:
            self.speak_dialog('temperature',{'temp':a , 'scale':b})

        except:
            self.speak.dialog('error')
    
    
    #DISK HANDLER
    @intent_handler('disk.intent')
    def handle_disk(self, message):
        used , free , sc = disk()
        try:
            self.speak_dialog('disk',{'usage':used , 'memory':free , 'scale': sc})
        except:
            self.speak.dialog('error')
    
    def stop(self):
        pass

    
    
def create_skill():
    return RpiInfo()



