import codecs,struct
from cStringIO import StringIO

class Base:
    def __init__(self , baseStream):
        self.base_stream = baseStream

    def ReadByte(self):
        return self.base_stream.read(1)

    def ReadBytes(self , count):
        return self.base_stream.read(count)

    def ReadChar(self):
        return ord(self.base_stream.read(1))

    def ReadChars(self , count):
        return struct.unpack('%dB' , self.base_steam.read(count))

    def ReadInt16(self):
        return struct.unpack('h' , self.base_stream.read(2))[0]

    def ReadInt32(self):
        return struct.unpack('i' , self.base_stream.read(4))[0]

    def ReadInt64(self):
        return struct.unpack('q' , self.base_stream.read(8))[0]

    def ReadUInt16(self):
        return struct.unpack('H' , self.base_stream.read(2))[0]

    def ReadUInt32(self):
        return struct.unpack('I' , self.base_stream.read(4))[0]

    def ReadUInt64(self):
        return struct.unpack('Q' , self.base_stream.read(8))[0]

    def ReadFloat(self):
        return struct.unpack('f' , self.base_stream.read(4))[0]

    def ReadBEInt16(self):
        return struct.unpack('>h' , self.base_stream.read(2))[0]

    def ReadBEInt32(self):
        return struct.unpack('>i' , self.base_stream.read(4))[0]

    def ReadBEInt64(self):
        return struct.unpack('>q' , self.base_stream.read(8))[0]

    def ReadBEUInt16(self):
        return struct.unpack('>H' , self.base_stream.read(2))[0]

    def ReadBEUInt32(self):
        return struct.unpack('>I' , self.base_stream.read(4))[0]

    def ReadBEUInt64(self):
        return struct.unpack('>Q' , self.base_stream.read(8))[0]

    def GetString(self):
        string = ""
        while True:
            char = self.base_stream.read(1)
            if ord(char) == 0:
                break
            string += char
        return string

    def WriteInt16(self , value):
        return self.base_stream.write(struct.pack('h' , value))

    def WriteInt32(self , value):
        return self.base_stream.write(struct.pack('i' , value))

    def WriteInt64(self , value):
        return self.base_stream.write(struct.pack('q' , value))

    def WriteUInt16(self , value):
        return self.base_stream.write(struct.pack('H' , value))

    def WriteUInt32(self , value):
        return self.base_stream.write(struct.pack('I' , value))

    def WriteUInt64(self , value):
        return self.base_stream.write(struct.pack('Q' , value))

    def WriteFloat(self , value):
        return self.base_stream.write(struct.pack('f' , value))

    def WriteBEInt16(self , value):
        return self.base_stream.write(struct.pack('>h' , value))

    def WriteBEInt32(self , value):
        return self.base_stream.write(struct.pack('>i' , value))

    def WriteBEInt64(self , value):
        return self.base_stream.write(struct.pack('>q' , value))

    def WriteBEUInt16(self , value):
        return self.base_stream.write(struct.pack('>H' , value))

    def WriteBEUInt32(self , value):
        return self.base_stream.write(struct.pack('>I' , value))

    def WriteBEUInt64(self , value):
        return self.base_stream.write(struct.pack('>Q' , value))

def getCWDHList(name , nums):
    fp = open(name ,"rb")
    fp.seek(0x202010)
    lists = []
    for i in xrange(nums):
        left = ord(fp.read(1))
        glyph = ord(fp.read(1))
        char = ord(fp.read(1))
        lists.append((left,glyph,char))
    fp.close()
    return lists

def build_cwdh(fntbin_name):
    fp = open(fntbin_name , "rb")
    fs = Base(fp)
    fp.seek(4)
    length = fs.ReadUInt32()
    buffer = StringIO()
    buffer.seek(0)
    base_stream = Base(buffer)
    buffer.write("CWDH")
    base_stream.WriteBEUInt32(length * 3 + 16)
    base_stream.WriteBEUInt16(0)
    base_stream.WriteBEUInt16(length - 1)
    base_stream.WriteBEUInt32(0)
    alists = getCWDHList("CKingMsg.bffnt" , 368)
    for i in xrange(length):
        charid = fs.ReadUInt32()
        x_pos = fs.ReadUInt32()
        y_pos = fs.ReadUInt32()
        c_width = fs.ReadUInt32()
        c_height = fs.ReadUInt32()
        c_index = fs.ReadUInt32()
        if i < 368:
            left = alists[i][0]
            glyph = alists[i][1]
            char = alists[i][2]
        else:
            left = 0x1
            glyph = 0x28
            char = 0x2a
        buffer.write(chr(left))
        buffer.write(chr(glyph))
        buffer.write(chr(char))

    buffer.seek(0,2)
    end_pos = buffer.tell()
    print(hex(end_pos))
    if end_pos % 4 != 0:
        buffer.write("\x00" * (0x4 - end_pos%4))
    buffer.seek(0,2)
    end_pos = buffer.tell()
    buffer.seek(4)
    base_stream.WriteBEUInt32(end_pos)
    cwdhdata = buffer.getvalue()
    fp.close()
    return cwdhdata


def build_cmap(string):
    length = len(string)
    buffer = StringIO()
    buffer.seek(0)
    base_stream = Base(buffer)
    buffer.write("CMAP")
    base_stream.WriteBEUInt32(length * 4 + 18)
    base_stream.WriteBEUInt16(0)
    base_stream.WriteBEUInt16(0XFFFF)
    base_stream.WriteBEUInt16(2)
    base_stream.WriteBEUInt16(0)
    base_stream.WriteBEUInt32(0)
    base_stream.WriteBEUInt16(length)
    for i in xrange(length):
        char = string[i]
        uchar = struct.unpack("H" ,char.encode("utf-16")[2:])[0]
        base_stream.WriteBEUInt16(uchar)
        base_stream.WriteBEUInt16(i)
    buffer.seek(0,2)
    end_pos = buffer.tell()
    print(hex(end_pos))
    if end_pos % 4 != 0:
        buffer.write("\x00" * (0x4 - end_pos%4))
    buffer.seek(0,2)
    end_pos = buffer.tell()
    buffer.seek(4)
    base_stream.WriteBEUInt32(end_pos)
    cmapdata = buffer.getvalue()
    return cmapdata



def fix_bffnt(fnt_name ,fbin_name,str_name):
    fp = open(fnt_name , "rb+")
    base_stream = Base(fp)
    fp.seek(0x10)
    fp.write("\x00\x04")
    fp.seek(0X2C)
    CWDHOffset = base_stream.ReadBEUInt32() # 0x2C cwdh offset
    CMAPOffset = base_stream.ReadBEUInt32() # 0x30 cwdh offset
    CWDHOffset -= 8
    CMAPOffset -= 8
    fp.seek(0x50)
    FLIM_OFFSET = base_stream.ReadBEUInt32() # 0x50 flim offset
    fp.seek(FLIM_OFFSET)
    cgfx_nums = 10
    for i in xrange(cgfx_nums):
        cgfx = open("inGTX//font.%d.gtx"%i , "rb")
        cgfx.seek(0xfc)
        data = cgfx.read(0x80000)
        cgfx.close()
        fp.write(data)
    fp.seek(CWDHOffset)
    fp.truncate()
    cwdhdata = build_cwdh(fbin_name)
    string = codecs.open(str_name,"rb" , "utf-16").read()
    cmapdata = build_cmap(string)
    fp.write(cwdhdata)
    tmp0 = fp.tell()
    fp.write(cmapdata)
    fp.seek(0x30)
    fp.write(struct.pack(">I" , tmp0 + 8))
    fp.seek(0,2)
    all = fp.tell()
    fp.seek(0xc)
    fp.write(struct.pack(">I" , all))
    fp.close()

fix_bffnt("inBFFNT\\font.bffnt" , "Message.BIN","CKingMsg.bffnt_charlist.txt" )






