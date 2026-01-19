from os import path, walk
from sys import argv
from struct import unpack, pack

fourCCDict = {
    2147483649 : b'DXT1',
    2147483653 : b'DXT5',
    6 : b'ATI2'
}

DDS_Struct_DX9 = b'DDS |\x00\x00\x00\x07\x10\n\x00{A}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x04\x00\x00\x00{B}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x10@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00{C}'

class FStream():
    def __init__(self, data):
        self.cursor = 0
        self.data = data

    def read(self, data_type, data_size):
        result = unpack(data_type, self.data[self.cursor:self.cursor+data_size])[0]
        self.cursor += data_size
        return result
    def seek(self, offset, /, *, relative = False):
        if not relative:
            self.cursor = offset
        else:
            self.cursor += offset
    def tell(self):
        return self.cursor

    def readUInt32(self):  return self.read("I", 4)
    def readString(self):
        STR = ""
        while(True):
            char = self.read("B", 1)
            if char != 0:
                STR += chr(char)
            else:
                break
        return STR

def KITexConv():
    dir_list = []
    kitex_file_list = []
    for arg in argv:
        if path.exists(arg) and path.isdir(arg):
            dir_list.append(arg)
        elif (path.exists(arg) and path.isfile(arg)) and (".kitex" in arg or ".KITEX" in arg):
            kitex_file_list.append(arg)
    
    for dir in dir_list:
        for root, dirs, files in walk(dir):
            for file in files:
                if ".kitex" in file or ".KITEX" in file: 
                    file_path = path.join(root, file)
                    kitex_file_list.append(file_path)

    for kitex_filepath in kitex_file_list:
        with open(kitex_filepath, 'rb') as kitexFile:
            data = kitexFile.read()
            fileStream = FStream(data)

            fileStream.seek(0x8)
            dataEntry = fileStream.readUInt32()

            fileStream.seek(0x6C)
            sizeX = fileStream.readUInt32()
            sizeY = fileStream.readUInt32()
            depth = fileStream.readUInt32()
            mipmapCount = fileStream.readUInt32()
            fileStream.cursor += 4
            fourCC = fileStream.readUInt32()
            fileStream.cursor += 12
            pitchOrLinearSize = fileStream.readUInt32()

            fileStream.seek(dataEntry + 132)
            source = fileStream.readString()
            imageData = fileStream.data[fileStream.cursor:]

            dds_path = kitex_filepath[:-6] + '.dds'
            if not path.exists(dds_path):
                with open(dds_path, 'wb+') as DDSFile:
                    DDSFile.write(
                        DDS_Struct_DX9.replace( b'{A}', pack('5I', sizeY, sizeX, pitchOrLinearSize, depth, mipmapCount) ).replace( b'{B}', fourCCDict[fourCC] ).replace( b'{C}', imageData )
                    )
            

if __name__ == '__main__':
    if len(argv) > 1:
        KITexConv()