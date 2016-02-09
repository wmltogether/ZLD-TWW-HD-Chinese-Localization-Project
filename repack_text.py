import codecs,struct,os
from glob import iglob
from cStringIO import StringIO
import binascii
def makestr(lines):
    string_list = []
    head_list = []
    num = len(lines)
    for index,line in enumerate(lines):
        if u'####' in line:
            head_list.append(line[5:-7])
            i = 1
            string = ''
            while True:
                if index+i >= num:
                    break
                if '####' in lines[index+i]:
                    break
                string += lines[index+i]
                i += 1
            string_list.append(string[:-4])
    return string_list

def dir_fn(adr):
    dirlst=[]
    for root,dirs,files in os.walk(adr):
        for name in files:
            adrlist=os.path.join(root, name)
            dirlst.append(adrlist)
    return dirlst

def findctr_code(string , original_text):
    if "{1a" in string:
        print("error : CODE ERROR %s"%string)
        return None
    if not "}" in string:
        print(u"error :[%s] >> } code is missing \n text: [%s]"%(string , original_text))
        return ""
    pos = 0
    ctr_str = ""
    mark = 0
    while pos < len(string):
        char = string[pos]
        if char == "{":
            ctr_str += char
            mark = 1
            pos += 1

        elif char == "}":
            ctr_str += char
            break
        else:
            ctr_str += char
            mark = 1
            pos += 1
    return ctr_str[1:-1]

def string2hex(string):
    if "{end}" in string:
        string = string.split("{end}")[0] + "{end}"
    else:
        string = string + "{end}"
    string = string.replace("\r" , "")
    string = string.replace("\n" , "\r\n")
    hex = ""
    pos = 0
    tmp_ctr = ""
    while pos < len(string):
        char = string[pos]
        if char == "{":
            ctr_str = findctr_code(string[pos:],string)
            if ctr_str.lower() == "end":
                hex += "0000"
            elif ":" in ctr_str.lower():
                items = ctr_str.split(":")
                for v in items:
                    ss = struct.unpack(">H" , struct.pack(">H" ,int(v,16)))[0]
                    hex += ("%04x"%ss)
            elif "E0" in ctr_str.upper():
                items = ctr_str
                ss = struct.unpack(">H" , struct.pack(">H" ,int(items,16)))[0]
                hex += ("%04x"%ss)
            else:
                print(u"error :[%s] >> code is unrecognized\n text:[%s]"%(ctr_str,string))
            pos += len(ctr_str) + 2
        else:
            char_code = struct.unpack(">H",char.encode('utf-16be'))[0]
            hex += "%04x"%char_code
            pos += 1
    dd = hex.lower()
    return binascii.a2b_hex(dd)

def build_block(base_offset , string_list):
    buffer = StringIO()
    buffer.write("TXT2")
    buffer.write("\x00\x00\x00\x00" * 3)
    buffer.write(struct.pack(">I" , len(string_list)))
    buffer.write("\x00\x00\x00\x00" * len(string_list))
    tmp = buffer.tell()
    for i in xrange(len(string_list)):
        buffer.seek(tmp)
        boffset = buffer.tell()

        string = string_list[i]
        bin = string2hex(string)
        buffer.write(bin)
        tmp = buffer.tell()
        buffer.seek(0x14 + i * 4)
        buffer.write(struct.pack(">I" , boffset - 0x10))
    buffer.seek(0,2)
    end = buffer.tell()
    buffer.seek(4)
    buffer.write(struct.pack(">I" , end  - 0x10))
    data = buffer.getvalue()
    if not len(data)%0x10 == 0:
        data += ("\xAB" * (0x10 - len(data)%0x10))
    return data


def repack_text(fn):
    fp = open("JPJA/%s"%fn , 'rb')
    o_buffer = fp.read()
    fp.seek(0)
    cnlines = codecs.open("cnTEXT//%s.txt"%fn , "rb" , "utf-16").readlines()
    string_list = makestr(cnlines)

    dest = StringIO()
    dest.write(o_buffer)
    dest.seek(0)
    if not os.path.exists("import/%s"%fn.replace("." , "_")):
        os.makedirs("import/%s"%fn.replace("." , "_"))
    dest2 = open("import//%s//%s"%(fn.replace("." , "_") , fn) , "wb")
    currentPos = 0
    pos = 0x20
    fp.seek(pos)
    while pos < os.path.getsize("JPJA/%s"%fn):
        fp.seek(pos)
        sig = fp.read(4)
        if sig == "LBL1":
            block_size, = struct.unpack(">I" , fp.read(4))
            padding = fp.read(8)
            block = fp.read(block_size)
            if block_size%0x10 != 0:
                null = fp.read(0x10 - block_size%0x10)
            pos = fp.tell()
        if sig == "ATR1":
            block_size, = struct.unpack(">I" , fp.read(4))
            padding = fp.read(8)
            block = fp.read(block_size)
            if block_size%0x10 != 0:
                null = fp.read(0x10 - block_size%0x10)
            pos = fp.tell()
        if sig == "TSY1":
            block_size, = struct.unpack(">I" , fp.read(4))
            padding = fp.read(8)
            block = fp.read(block_size)
            if block_size%0x10 != 0:
                null = fp.read(0x10 - block_size%0x10)
            pos = fp.tell()
        if sig == "TXT2":
            currentPos = pos
            break
    if currentPos > 0:
        dest.seek(currentPos)
        dest.truncate()
        block_data = build_block(currentPos , string_list)
        dest.write(block_data)
        end = dest.tell()
        dest.seek(0x12)
        dest.write(struct.pack(">I" , end))
    dest2.write(dest.getvalue())
    dest2.close()
    fp.close()
fl = dir_fn("cntext")
for fn in fl:
    fn = fn.split("\\")[-1]
    repack_text(fn[:-4])
