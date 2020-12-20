
from webscrappers.spider_manager import SpiderManager

class TaskManager:
    def __init__(self):
        pass

    def trigger_task(self, message):
        if message == "coucou":
            response = "hibou"

        if message == "processeur":
            availability = self.get_processor_availability()
            response = availability


        return response
        
    def get_processor_availability(self):
        sm = SpiderManager()
        # TODO: put these in params
        stocks = sm.execute_spiders(["processor_ldlc", "processor_topachat"])
        #print(stocks)
        # isolate spiders thar didn't work and those that had unexpected values
        success = True
        error_keys = []
        unexpected_keys = []
        for key, value in stocks.items():
            if value["success"] == False:
                if value["parsed"]:
                    unexpected_keys.append(key)
                    success = False
                else:
                    error_keys.append(key)
        
        # print appropriate message
        message = ""
        if not success:
            message += "PROCESSEEEEEEUR!!!! \n"
            for uk in unexpected_keys:
                message += uk+" "
            message += "a trouvé un processeur!\n"
        else:
            message += "pas de processeur en vue..\n"
        if error_keys:
            for ek in error_keys:
                message += ek + " "
            message += "n'a pas fonctionné"
        
        return message