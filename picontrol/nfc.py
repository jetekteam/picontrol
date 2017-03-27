import time, binascii, json
from picontrol import PN532 #Adafruit_PN532 as PN532
from picontrol import ndef

SCLK = 4 #2 
MISO = 17 #15
MOSI = 27 #17
CS   = 22 #18

DEFAULT_KEY = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
DEFAULT_KEY_A = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
NDEF_A = [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5]
NDEF_B = [0xD3, 0xF7, 0xD3, 0xF7, 0xD3, 0xF7]

# response class, used for outputs
class response(object):
    def __init__(self):
        self.type = ''
        self.data = ''
        self.message = ''

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def getPn532():
    try:
        pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
        pn532.begin()
        pn532.SAM_configuration()
        return pn532
    except:
        return None

def createBlockMatrix(data):
    byteMatrix = [[None for x in range(16)] for y in range(44)]
    valueArray = []
    while data:
        valueArray.append(data[:16].ljust(16))
        data = data[16:]

    idx = 0
    while idx < len(byteMatrix):
        byteMatrix[idx] = bytearray(16)
        if len(valueArray) > idx:
            byteMatrix[idx] = bytearray(valueArray[idx])
        idx = idx + 1
        
    return byteMatrix

def createPageMatrix(data):
    byteMatrix = [[None for x in range(4)] for y in range(35)]
    valueArray = []
    while data:
        valueArray.append(data[:4].ljust(4))
        data = data[4:]

    idx = 0
    while idx < len(byteMatrix):
        byteMatrix[idx] = bytearray(4)
        if len(valueArray) > idx:
            byteMatrix[idx] = bytearray(valueArray[idx])
        idx = idx + 1
        
    return byteMatrix

def blockArray():
    blocks = []
    skipper = 0
    for i in range(4,64):
        skip = False
        if skipper == 3:
            skipper = -1
            skip = True
        if skip == False:
            blocks.append(i)
        skipper += 1
    return blocks

def isBlockEmpty(block):
    isEmpty = True
    for char in block:
        if char != 0x00:
            isEmpty = False
    return isEmpty

def write(message):
    resp = response()
    buffer = message.encode()
    pn532 = getPn532()    
    cardType = 'unknown'

    if pn532 != None:

        maxAttempts = 5
        attempts = 0

        uid = pn532.read_passive_target()
        while uid is None:
            if attempts >= maxAttempts:
                resp.type = 'error'
                resp.message = 'Unable to find tag, try reseating or tapping the tag and try again.'
                resp.data = ''
                pn532.shutdown()
                
                return response
            uid = pn532.read_passive_target()
            attempts = attempts + 1
            time.sleep(.5)

        if len(uid) == 4:
            # we have a mifare classic
            cardType = 'mifareclassic'
        elif len(uid) == 7:
            # we have a mifare ultralight or ntag2xx
            cardType = 'ntag2xx'

        if cardType == 'mifareclassic':    
            # if isFormated() == False:
            #     format()    

            blocks = blockArray()
            bytesToWrite = createBlockMatrix(buffer)

            # we got a uid, now write the data
            for block in range(len(blocks)):
                if not pn532.mifare_classic_authenticate_block(uid, blocks[block], PN532.MIFARE_CMD_AUTH_B, DEFAULT_KEY):
                    resp.type = 'error'
                    resp.message = 'Failed to authenticate block {0} with the card.'.format(block)
                    resp.data = ''
                    pn532.shutdown()

                    return resp
                data = bytesToWrite[block]

                if not pn532.mifare_classic_write_block(blocks[block], data):
                    resp.type = 'error'
                    resp.message = 'Failed to write block {0}!'.format(block)
                    resp.data = ''
                    pn532.shutdown()

                    return resp

                if isBlockEmpty(data):
                    break

            resp.type = 'success'
            resp.message = 'Message written successfully.'
            resp.data = ''
        
        elif cardType == 'ntag2xx':
            blocks = blockArray()
            bytesToWrite = createPageMatrix(buffer)

            #print(bytesToWrite)
            
            # data starts at page 4
            page = 4
            for i in range(0,34):
                byteIndex = i*4
                data = buffer[byteIndex:byteIndex+4]
                len_diff = 4 - len(data)
                data += "\0"*len_diff

                #print(len(data))
                #print(map(hex,data))

                if not pn532.ntag2xx_write_page(page, data):
                    resp.type = 'error'
                    resp.message = 'Failed to write page {0}!'.format(page)
                    resp.data = ''
                    pn532.shutdown()

                    return resp
                page+=1
                
                if isBlockEmpty(data):
                    break

            resp.type = 'success'
            resp.message = 'Message written successfully.'
            resp.data = ''

        # shutdown, were done writing
        pn532.shutdown()
    else:
        resp.type = 'error'
        resp.message = 'Unable to find NFC Device.'
        resp.data = ''

    return resp

def read():
    # Format to NDEF if not already
    message = ndef.Message()
    resp = response()
    blocks = blockArray()
    pn532 = getPn532()    
    cardType = 'unknown'

    if pn532 != None:

        resp.type = ""
        resp.message = ""
        resp.data = ""

        bufferFromCard = ''
        maxAttempts = 2
        attempts = 0

        uid = pn532.read_passive_target()
        while uid is None:
            if attempts >= maxAttempts:
                resp.type = 'error'
                resp.message = 'Unable to find tag, try reseating or tapping the tag and try again.'
                resp.data = ''
                pn532.shutdown()

                return resp
            uid = pn532.read_passive_target()
            attempts = attempts + 1
            time.sleep(.2)    

        if len(uid) == 4:
            # we have a mifare classic
            cardType = 'mifareclassic'
        elif len(uid) == 7:
            # we have a mifare ultralight or ntag2xx
            cardType = 'ntag2xx'

        if cardType == 'mifareclassic':
            # if isFormated() == False:
            #     format()    

            # We got a uid, now read the data
            for block in range(len(blocks)):
                if not pn532.mifare_classic_authenticate_block(uid, blocks[block], PN532.MIFARE_CMD_AUTH_B, DEFAULT_KEY):
                    resp.type = 'error'
                    resp.message = 'Failed to authenticate block {0} with the card.'.format(block)
                    resp.data = ''
                    pn532.shutdown()

                    return resp
                else:
                    data = pn532.mifare_classic_read_block(blocks[block])
                    if data is None:
                        resp.type = 'error'
                        resp.message = 'Failed to read block {0}!'.format(block)
                        resp.data = ''
                        pn532.shutdown()

                        return resp
                    else:
                        if isBlockEmpty(data):
                            break
                        bufferFromCard += data

            message.setBuffer(bufferFromCard)
            message.decode()

            resp.type = "success"
            resp.message = "success"
            resp.data = message

        elif cardType == 'ntag2xx':
            # data starts at page 4
            for page in range(4,39):
                data = pn532.ntag2xx_read_page(page)
                if data is None:
                    resp.type = 'error'
                    resp.message = 'Failed to read page {0}!'.format(page)
                    resp.data = ''
                else:
                    if isBlockEmpty(data):
                        break
                    bufferFromCard += data

            if bufferFromCard[0] != 0x3:
                #we move forward 5 bytes to get us to the ndef records
                newBuffer = bufferFromCard[5:]
                bufferFromCard = newBuffer

            message.setBuffer(bufferFromCard)
            message.decode()

            resp.type = "success"
            resp.message = "success"
            resp.data = message

        # shutdown, were done reading
        pn532.shutdown()
    else:
        resp.type = 'error'
        resp.message = 'Unable to find NFC Device.'
        resp.data = ''
        
    return resp

def isFormated():
    resp = response()
    pn532 = getPn532()

    maxAttempts = 5
    attempts = 0

    uid = pn532.read_passive_target()
    while uid is None:
        if attempts >= maxAttempts:
            resp.type = 'error'
            resp.message = 'Unable to find tag, try reseating or tapping the tag and try again.'

            return resp
        uid = pn532.read_passive_target()
        attempts = attempts + 1
        time.sleep(.5)    

    # We got a uid, now read
    if not pn532.mifare_classic_authenticate_block(uid, 1, PN532.MIFARE_CMD_AUTH_B, DEFAULT_KEY):
        return False
    
    sectorbuffer1 = pn532.mifare_classic_read_block(1)
    sectorbuffer2 = pn532.mifare_classic_read_block(2)
    
    sb1 = binascii.hexlify(sectorbuffer1)
    sb2 = binascii.hexlify(sectorbuffer2)
    t1 = ''.join('{:02x}'.format(x) for x in [0x14, 0x01, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1])
    t2 = ''.join('{:02x}'.format(x) for x in [0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1])

    if sb1 == t1 and sb2 == t2:
        return True
    else:
        return False

def format():
    resp = response()
    pn532 = getPn532()    

    sectorbuffer1 = [0x14, 0x01, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1]
    sectorbuffer2 = [0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1, 0x03, 0xE1]
    sectorbuffer3 = [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0x78, 0x77, 0x88, 0xC1, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

    # sectorbuffer4 = [0x03, 0x00, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    # sectorbuffer5 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    # sectorbuffer6 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    # sectorbuffer7 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7F, 0x07, 0x88, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    # Note 0xA0 0xA1 0xA2 0xA3 0xA4 0xA5 must be used for key A
    # for the MAD sector in NDEF records (sector 0)

    maxAttempts = 5
    attempts = 0

    uid = pn532.read_passive_target()
    while uid is None:
        if attempts >= maxAttempts:
            resp.type = 'error'
            resp.message = 'Unable to find tag, try reseating or tapping the tag and try again.'
            resp.data = ''

            return resp
        uid = pn532.read_passive_target()
        attempts = attempts + 1
        time.sleep(.5)    

    # We got a uid, now format
    if not pn532.mifare_classic_authenticate_block(uid, 1, PN532.MIFARE_CMD_AUTH_B, DEFAULT_KEY):
        resp.type = 'error'
        resp.message = 'Failed to authenticate block {0} with the card.'.format(1)
        resp.data = ''

        return resp
    else:
        # Write block 1 and 2 to the card
        if not pn532.mifare_classic_write_block(1, sectorbuffer1):
            resp.type = 'error'
            resp.message = 'Failed to write block 1!'
            resp.data = ''

            return resp
        if not pn532.mifare_classic_write_block(2, sectorbuffer2):
            resp.type = 'error'
            resp.message = 'Failed to write block 2!'
            resp.data = ''

            return resp
        # Write key A and access rights to the card
        if not pn532.mifare_classic_write_block(3, sectorbuffer3):
            resp.type = 'error'
            resp.message = 'Failed to write block 3!'
            resp.data = ''
        
            return resp

    # We got a uid, now format
    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B, DEFAULT_KEY):
        resp.type = 'error'
        resp.message = 'Failed to authenticate block {0} with the card.'.format(4)
        resp.data = ''

        return resp
    else:
        # Write block 1 and 2 to the card
        if not pn532.mifare_classic_write_block(4, sectorbuffer4):
            resp.type = 'error'
            resp.message = 'Failed to write block 4!'
            resp.data = ''

            return resp

    i = 7
    while i <= 63:
        if pn532.mifare_classic_authenticate_block(uid, i, PN532.MIFARE_CMD_AUTH_B, DEFAULT_KEY):
            if not pn532.mifare_classic_write_block(i, sectorbuffer7):
                print('unable to write block ' + str(i))
        i += 4

    resp.type = 'success'
    resp.message = ''
    resp.data = ''

    pn532.shutdown()

    return resp

def dumpMAD():
    resp = response()
    pn532 = getPn532()

    maxAttempts = 5
    attempts = 0

    uid = pn532.read_passive_target()
    while uid is None:
        if attempts >= maxAttempts:
            resp.type = 'error'
            resp.message = 'Unable to find tag, try reseating or tapping the tag and try again.'

            return resp
        uid = pn532.read_passive_target()
        attempts = attempts + 1
        time.sleep(.5)    

    # We got a uid, now read
    for block in range(0,64):

        if not pn532.mifare_classic_authenticate_block(uid, block, PN532.MIFARE_CMD_AUTH_B, DEFAULT_KEY):
            return False
        else:
            
            sectorbuffer = pn532.mifare_classic_read_block(block)
            sb = binascii.hexlify(sectorbuffer)

            print(sb)
    
