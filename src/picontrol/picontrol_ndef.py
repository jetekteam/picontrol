#NDEF Record Format

# Prefixes for NDEF Records (to identify record type)
NDEF_WELLKNOWNRECORD                = 0x1

NDEF_RECORDTYPE_TEXT                = 0x54
NDEF_RECORDTYPE_URI                 = 0x55

NDEF_TEXT_UNICODE                   = 0x01
NDEF_TEXT_UTF8                      = 0x02

NDEF_URIPREFIX_NONE                 = 0x00
NDEF_URIPREFIX_HTTP_WWWDOT          = 0x01
NDEF_URIPREFIX_HTTPS_WWWDOT         = 0x02
NDEF_URIPREFIX_HTTP                 = 0x03
NDEF_URIPREFIX_HTTPS                = 0x04
NDEF_URIPREFIX_TEL                  = 0x05
NDEF_URIPREFIX_MAILTO               = 0x06
NDEF_URIPREFIX_FTP_ANONAT           = 0x07
NDEF_URIPREFIX_FTP_FTPDOT           = 0x08
NDEF_URIPREFIX_FTPS                 = 0x09
NDEF_URIPREFIX_SFTP                 = 0x0A
NDEF_URIPREFIX_SMB                  = 0x0B
NDEF_URIPREFIX_NFS                  = 0x0C
NDEF_URIPREFIX_FTP                  = 0x0D
NDEF_URIPREFIX_DAV                  = 0x0E
NDEF_URIPREFIX_NEWS                 = 0x0F
NDEF_URIPREFIX_TELNET               = 0x10
NDEF_URIPREFIX_IMAP                 = 0x11
NDEF_URIPREFIX_RTSP                 = 0x12
NDEF_URIPREFIX_URN                  = 0x13
NDEF_URIPREFIX_POP                  = 0x14
NDEF_URIPREFIX_SIP                  = 0x15
NDEF_URIPREFIX_SIPS                 = 0x16
NDEF_URIPREFIX_TFTP                 = 0x17
NDEF_URIPREFIX_BTSPP                = 0x18
NDEF_URIPREFIX_BTL2CAP              = 0x19
NDEF_URIPREFIX_BTGOEP               = 0x1A
NDEF_URIPREFIX_TCPOBEX              = 0x1B
NDEF_URIPREFIX_IRDAOBEX             = 0x1C
NDEF_URIPREFIX_FILE                 = 0x1D
NDEF_URIPREFIX_URN_EPC_ID           = 0x1E
NDEF_URIPREFIX_URN_EPC_TAG          = 0x1F
NDEF_URIPREFIX_URN_EPC_PAT          = 0x20
NDEF_URIPREFIX_URN_EPC_RAW          = 0x21
NDEF_URIPREFIX_URN_EPC              = 0x22
NDEF_URIPREFIX_URN_NFC              = 0x23

class Record(object):
    def __init__(self):
        # defaults
        self.ndefType = NDEF_WELLKNOWNRECORD
        self.recordType = NDEF_RECORDTYPE_TEXT
        self.definition = NDEF_TEXT_UTF8
        self.language = "en"
        self.value = ""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)        

    def setValue(self, value):
        self.value = value
    
    def getValue(self):
        return self.value
    
    def setNdefType(self, type):
        self.recordType = type

    def getNdefType(self):
        return self.ndefType

    def setRecordType(self, type):
        self.recordType = type

    def getRecordType(self):
        return self.recordType

    def setDefinition(self, definition):
        self.definition = definition

    def getDefinition(self):
        return self.definition

    def setLanguage(self, language):
        self.language = language

    def getLanguage(self):
        return self.language

class Message(object):
    def __init__(self):
        self.records = []
        self.buffer = bytearray()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def setRecords(self, records):
        self.records = records

    def getRecords(self):
        return self.records

    def setBuffer(self, buffer):
        self.buffer = buffer

    def getBuffer(self):
        return self.buffer

    def addTextRecord(self, value):
        # Initialize record
        record = Record()

        # Add value
        record.value = value

        # Add record to message
        self.records.append(record)

        # Return the new record
        return self.records[len(self.records) - 1]

    def addUriRecord(self, prefix, value):
        # Initialize record
        record = Record()

        # Set record type
        record.recordType = NDEF_RECORDTYPE_URI

        # Set prefix
        record.definition = prefix

        # Add value
        record.value = value

        # Add record to message
        self.records.append(record)

        # Return the new record
        return self.records[len(self.records) - 1]

    def addRecord(self, ndefType, recordType, definition, language, value):
        # Initialize record
        record = Record()

        # Add record type
        if (recordType != NDEF_RECORDTYPE_TEXT and recordType != NDEF_RECORDTYPE_URI):
            print('You can only add Text or URI records')
            return NONE
        record.type = type

        # Add record definition
        record.definition = definition

        # Add language
        record.language = language

        # Add value
        record.value = value

        # Add record to message
        self.records.append(record)

        # Return the new record
        return self.records[len(self.records) - 1]

    def delRecord(self, index):
        # delete record at index
        del self.records[index]

    def encode(self):
        # calc payloadLength
        payloadLength = 0
        records = self.getRecords()
        recordCount = len(records)

        for i in range(recordCount):
            payloadLength += len(records[i].value) + 7
        
        buffer = bytearray(payloadLength + 3)
        buffer[0] = 0x03 # Indicates NDEF Record
        buffer[1] = payloadLength
        buffer[2] = 0xd1 # no chunks
        if recordCount >= 2:
            buffer[2] = 0x91 # has chunks

        # loop through records and add to buffer
        bufferIndex = 3
        for i in range(recordCount):
            buffer[bufferIndex] = records[i].ndefType
            bufferIndex += 1
            buffer[bufferIndex] = len(records[i].value) + 3
            bufferIndex += 1
            buffer[bufferIndex] = records[i].recordType
            bufferIndex += 1
            buffer[bufferIndex] = records[i].definition
            bufferIndex += 1
            buffer[bufferIndex] = records[i].language[:1]
            bufferIndex += 1
            buffer[bufferIndex] = records[i].language[1:]
            bufferIndex +=1 

            for r in range(len(records[i].value)):
                buffer[bufferIndex] = str(records[i].value[r])
                bufferIndex += 1

            buffer[bufferIndex] = 0xfe # End NDEF Record
            
            if recordCount >= 2 and i <= recordCount - 3:
                buffer[bufferIndex] = 0x11 # indicates start of next record 
                bufferIndex += 1
            
            elif recordCount >= 2 and i <= recordCount - 2:
                buffer[bufferIndex] = 0x51 # indicates start of last record 
                bufferIndex += 1

        self.setBuffer(buffer)

        return self.getBuffer()

    def decode(self):
        buffer = self.getBuffer()
        records = []

        ndef = buffer[0]
        payloadLength = buffer[1]
        chunker = buffer[2]

        if ndef == 0x03: # we have a NDEF record
            recordParser = []
            for i in range(3,len(buffer)):
                if buffer[i] == 0x11 or buffer[i] == 0x51 or buffer[i] == 0xfe: # we hit the end of a record
                    record = Record()
                    record.ndefType = recordParser[0]
                    record.recordType = chr(recordParser[2])
                    record.definition = recordParser[3]
                    record.language = ''.join(chr(i) for i in recordParser[4:6])
                    record.value = ''.join(chr(i) for i in recordParser[6:])
                    records.append(record)
                    recordParser = []
                else:
                    recordParser.append(buffer[i])
                if buffer[i] == 0xfe: # this is the end of the message, exit loop
                    break      

        self.setRecords(records)
        return self.getRecords()
