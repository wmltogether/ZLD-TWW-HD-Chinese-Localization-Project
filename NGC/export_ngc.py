import codecs
import os
import struct

def readtbl(tbl_name):
    fp = codecs.open("%s"%tbl_name , "rb" , "utf-16")
    lines = fp.readlines()
    tbl = {}
    for line in lines:
        if "=" in line:
            line = line.replace("\r\n" , "")
            code = line.split("=")[0]
            char = line.split("=")[1]
            code = int(code,16)
            tbl[code] = char
    fp.close()
    return tbl

def readBMG(bmg_name ,tbl_name, dest_name):
    fp = open(bmg_name , "rb")
    dest = codecs.open(dest_name , "wb" , "utf-16")
    tbl = readtbl(tbl_name)
    fp.seek(0x24)
    base_offset = struct.unpack(">I" , fp.read(4))[0] + 0x20
    nums = struct.unpack(">H" , fp.read(2))[0]
    fp.seek(0x30)
    for i in xrange(nums):
        fp.seek(0x30 + 0x18 * i)
        (offset ,\
            tid , \
            unk0 , \
            unk1 , \
            unk2 , \
            unk3) = struct.unpack(">6I" , fp.read(0x18))
        offset = offset + base_offset + 8
        fp.seek(offset)
        string = ""
        while True:
            v0 = fp.read(1)
            v0 = ord(v0)
            if v0 == 0x1a:
                v1 = ord(fp.read(1))
                v2 = ord(fp.read(1))
                if v2 == 0xff:
                    v3 = ord(fp.read(1))
                    v4 = ord(fp.read(1))
                    v5 = ord(fp.read(1))
                    if v1 == 7:
                        v6 = ord(fp.read(1))
                        string += ("{%x:%x:%x:%x:%x:%x:%x}"%(v0,v1,v2,v3,v4,v5,v6))
                    else:
                        string += ("{%x:%x:%x:%x:%x:%x}"%(v0,v1,v2,v3,v4,v5))
                else:
                    if v1 == 7:
                        v3 = ord(fp.read(1))
                        v4 = ord(fp.read(1))
                        v5 = ord(fp.read(1))
                        v6 = ord(fp.read(1))
                        string += ("{%x:%x:%x:%x:%x:%x:%x}"%(v0,v1,v2,v3,v4,v5,v6))
                    else:
                        v3 = ord(fp.read(1))
                        v4 = ord(fp.read(1))
                        string += ("{%x:%x:%x:%x:%x}"%(v0,v1,v2,v3,v4))
            elif v0 == 0xa:
                string += ("\r\n")
            elif v0 == 0xd:
                pass
            elif 0x20 <= v0 <= 0x7e:
                string += ("%s"%chr(v0))
            elif v0 > 0x80:
                v1 = ord(fp.read(1))
                if  (v0 * 0x100 + v1) in tbl:
                    char = tbl[v0 * 0x100 + v1]
                else:
                    char = ""
                string += char
            elif v0 == 0:
                break
            else:
                print("error :%x current position:%08x"%(v0 , offset))
                print(string)
                print(hex(fp.tell()))
                break
        dest.write("#### %d ####\r\n%s{end}\r\n\r\n"%(i ,string))
    dest.close()
    fp.close()

readBMG("JPDAT//zel_00.bmg" ,"jp.tbl.txt", "jp-text//zel_00.bmg.txt")
readBMG("ENDAT//zel_00.bmg" ,"jp.tbl.txt", "US-text//zel_00.bmg.txt")
readBMG("CNDAT//zel_00.bmg" ,"ch.tbl.txt", "CN-text//zel_00.bmg.txt")
