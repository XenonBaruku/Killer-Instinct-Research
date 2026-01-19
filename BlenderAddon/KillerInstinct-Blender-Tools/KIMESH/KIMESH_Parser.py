from ..COMMON.Reader import FStream
    
class KIMESHParser():
    def __init__(self, path = None, data = None):
        self.path = path
        if data is None:
            with open(path, "rb") as msh_file:
                data = msh_file.read()
        self.fileStream = FStream(data)
    
    def read(self):
        fs = self.fileStream
        fileType = fs.readUInt32()
        fileVersion = fs.readUInt32()
        if fileType != 1 or fileVersion != 21:
            raise RuntimeError("Invalid KIMESH file: {}".format(self.path))
        dataEntry = fs.readUInt32()
        dataInfoCount = fs.readUInt32()
        dataInfo3Count = fs.readUInt32()
        unkU32 = fs.readUInt32()
        unkU32 = fs.readUInt32()
        dataInfoEntry = fs.readUInt32()
        unkU32 = fs.readUInt32()
        dataInfo3Entry = fs.readUInt32()
        unkU32 = fs.readUInt32()
        dataInfo4Entry = fs.readUInt32()

        fs.seek(dataInfoEntry + 2 * 80 + 12)
        faceChunkEntry = fs.readUInt32() + dataEntry + 12
        fs.seek(dataInfoEntry + 3 * 80 + 12)
        vertexChunkEntry = fs.readUInt32() + dataEntry + 12
        fs.seek(dataInfoEntry + 4 * 80 + 12)
        weightChunkEntry = fs.readUInt32() + dataEntry + 12
        fs.seek(dataInfoEntry + 5 * 80 + 12)
        unkBoneInfoChunkEntry = fs.readUInt32() + dataEntry + 12

        dataInfo2Entry = dataInfoEntry + 6 * 80 + 12
        fs.seek(dataInfo2Entry + 2 * 24 + 16)
        meshCount = fs.readUInt32()
        meshInfo1Entry = fs.readUInt32() + dataEntry + 94
        fs.seek(dataInfo2Entry + 14 * 24 + 20)
        meshInfo2Entry = fs.readUInt32() + dataEntry + 12
        fs.seek(dataInfo2Entry + 19 * 24 + 20)
        nameChunkOffset1 = fs.readUInt32()
        fs.seek(dataInfo2Entry + 23 * 24 + 20)
        nameChunkOffset2 = fs.readUInt32()
        nameChunkEntry = nameChunkOffset1 + nameChunkOffset2 + dataEntry + 12

        meshInfos = []
        vertexCountSum = 0
        faceCountSum = 0
        fs.seek(meshInfo1Entry)
        for i in range(meshCount):
            meshInfo = {}
            fs.cursor += 22
            meshInfo['UVType'] = fs.readUInt32()
            meshInfo['faceIndexStart'] = fs.readUInt32()
            faceCount = fs.readUInt32()
            meshInfo['faceCount'] = faceCount
            faceCountSum += faceCount
            vertexCount = fs.readUInt32()
            meshInfo['vertexCount'] = vertexCount
            vertexCountSum += vertexCount
            unkU32 = fs.readUInt32()
            unkU32 = fs.readUInt32()
            meshInfo['faceIndexCount'] = fs.readUInt32()
            faceCount2 = fs.readUInt32()
            fs.cursor += 378
            meshInfos.append(meshInfo)

        fs.seek(meshInfo2Entry)
        for i in range(meshCount):
            meshInfos[i]['vertexDataSize'] = fs.readUInt32()
            meshInfos[i]['vertexDataOffset'] = fs.readUInt32()
            fs.cursor += 32
            meshInfos[i]['weightDataSize'] = fs.readUInt32()
            meshInfos[i]['weightDataOffset'] = fs.readUInt32()
            fs.cursor += 32

        fs.seek(vertexChunkEntry)
        for i in range(meshCount):
            vertices = []
            fs.seek(vertexChunkEntry + meshInfos[i]['vertexDataOffset'])
            if meshInfos[i]['vertexDataSize'] == 20:
                for j in range(meshInfos[i]['vertexCount']):
                    vertices.append([fs.readFloat32(), fs.readFloat32(), fs.readFloat32()])
                    fs.cursor += 8
            meshInfos[i]['vertices'] = vertices
        
        fs.seek(faceChunkEntry)
        for i in range(meshCount):
            faces = []
            fs.seek(faceChunkEntry + meshInfos[i]['faceIndexStart'] * 2)
            for j in range(meshInfos[i]['faceCount']):
                faces.append([ 
                    fs.readUInt16(),
                    fs.readUInt16(),
                    fs.readUInt16()
                ])
            meshInfos[i]['faces'] = faces

        self.names = []
        fs.seek(nameChunkEntry)
        for i in range(meshCount + 2):
            self.names.append(fs.readString())

        for i in range(meshCount):
            meshInfos[i]['name'] = self.names[i + 1]

        return meshInfos


        
if __name__ == '__main__':
    file_path = 'D:/KI/SPLIT_CHAR_RIPTOR_PAK/characters/riptor/riptor.kimesh'
    KIMESHParser(path=file_path).read()