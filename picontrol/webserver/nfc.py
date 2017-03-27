import sys, os, json
from picontrol import nfc
from picontrol import ndef

class NFC():
    @staticmethod
    def readNFC():
        records = []
        try:
            response = nfc.read()

            if response.type == 'success':
                message = response.data
                for i in range(len(message.records)):
                    records.append(message.records[i].value)
            
            jResponse = { 'type':response.type , 'message':response.message, 'data':{'records':records} }
        except:
            jResponse = { 'type':'error' , 'message':'No records found on the NFC Tag.', 'data':'' }
        return jResponse

    @staticmethod
    def writeNFC(data):
        try:
            gameData = json.loads(data)

            message = ndef.Message()
            message.addTextRecord(gameData['console'])
            message.addTextRecord(gameData['rom'])
            response = nfc.write(message)

            print(response.type)

            jResponse = { 'type':response.type , 'message':response.message, 'data':response.data  }
        except:
            jResponse = { 'type':'error' , 'message':'Unable to write to the NFC Tag.', 'data':'' }
        return jResponse  
