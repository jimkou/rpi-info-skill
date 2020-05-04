from mycroft import MycroftSkill, intent_file_handler


class RpiInfo(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('info.rpi.intent')
    def handle_info_rpi(self, message):
        memory = ''
        number = ''
        number_perc = ''
        scale = ''
        temp = ''
        usage = ''

        self.speak_dialog('info.rpi', data={
            'number_perc': number_perc,
            'usage': usage,
            'temp': temp,
            'memory': memory,
            'scale': scale,
            'number': number
        })


def create_skill():
    return RpiInfo()

