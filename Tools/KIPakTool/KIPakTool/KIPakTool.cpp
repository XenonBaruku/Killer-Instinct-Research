#include <iostream>
#include <fstream>
#include <filesystem>
#include <unordered_map>
#include <string>

using namespace std;

unordered_map<short, string> fileExtensions = {
    {2, ".kimesh"},
    {3, ".kimat"},
    {4, ".kitex"},
    {13, ".CinematicShot.xml"},
    {21, ".EventList.xml"},
    {22, ".MeshAttachmentInfo.xml"},
    {28, ".kihkx"},
    {29, ".hkAnim"},
    {33, ".bnk"},
    {53, ".ProceduralAnimationData.xml"}
};


void createDirectoryRecursive(filesystem::path& path)
{
    if (path.empty()) return;

    filesystem::path parentPath = path.parent_path();

    if (!filesystem::exists(parentPath))
    {
        createDirectoryRecursive(parentPath);
        filesystem::create_directory(path);
    }
    else
    {
        filesystem::create_directory(path);
    }
}

int unpack(char* path)
{
    char* buffer = (char*)malloc(4);
    if (buffer == NULL)
    {
        perror("malloc");
        return(1);
    }

    ifstream fs;
    fs.open(path, ios::binary);
    if (!fs.is_open())
    {
        free(buffer);
        return(2);
    }
    fs.seekg(0, ios::beg);

    filesystem::path fullPakPath = path;
    filesystem::path unpackedFolder = fullPakPath.parent_path() / fullPakPath.stem();
    cout << unpackedFolder << endl;

    if (!filesystem::exists(unpackedFolder) || !filesystem::is_directory(unpackedFolder))
    {
        try
        {
            filesystem::create_directory(unpackedFolder);
        }
        catch (...)
        {
            free(buffer);
            return(4);
        }
    }

    unsigned int signature;
    fs.read(buffer, sizeof(unsigned int));
    memcpy(&signature, buffer, sizeof(int));

    if (signature != 1598767440)
    {
        free(buffer);
        fs.close();
        return(3);
    }

    unsigned int version;
    fs.read(buffer, sizeof(unsigned int));
    memcpy(&version, buffer, sizeof(unsigned int));

    if (version != 4)
    {
        free(buffer);
        fs.close();
        return(3);
    }

    unsigned int unknUInt32Header_0;
    fs.read(buffer, sizeof(unsigned int));
    memcpy(&unknUInt32Header_0, buffer, sizeof(unsigned int));

    unsigned int type;
    fs.read(buffer, sizeof(unsigned int));
    memcpy(&type, buffer, sizeof(unsigned int));

    unsigned int fileCount;
    fs.read(buffer, sizeof(unsigned int));
    memcpy(&fileCount, buffer, sizeof(unsigned int));

    unsigned int nameCount;
    fs.read(buffer, sizeof(unsigned int));
    memcpy(&nameCount, buffer, sizeof(unsigned int));

    unsigned int unknInfoTblCount;
    fs.read(buffer, sizeof(unsigned int));
    memcpy(&unknInfoTblCount, buffer, sizeof(unsigned int));

    printf("%u\n%u\n%u\n%u\n%u\n%u\n%u\n", signature, version, unknUInt32Header_0, type, fileCount, nameCount, unknInfoTblCount);

    unsigned int i;

    if (unknInfoTblCount > 0)
    {
        unsigned int CRC;
        unsigned int unknInfoCount;
        for (i = 0; i < unknInfoTblCount; i++)
        {
            fs.read(buffer, sizeof(unsigned int));
            memcpy(&CRC, buffer, sizeof(unsigned int));

            fs.read(buffer, sizeof(unsigned int));
            memcpy(&unknInfoCount, buffer, sizeof(unsigned int));

            for (unsigned int j = 0; j < unknInfoCount; j++)
            {
                fs.read(buffer, 4);
            }
        }
    }

    if (nameCount > 0)
    {
        unsigned int CRC;
        unsigned int length;
        char* nameString;
        for (i = 0; i < nameCount + 1; i++)
        {
            fs.read(buffer, sizeof(unsigned int));
            memcpy(&CRC, buffer, sizeof(unsigned int));
            fs.read(buffer, sizeof(unsigned int));
            memcpy(&length, buffer, sizeof(unsigned int));
            nameString = new char[length];
            fs.read(nameString, length);
        }
    }

    if (fileCount > 0)
    {
        char* pathString = (char*)malloc(240);
        if (pathString == NULL)
        {
            perror("malloc");
            free(buffer);
            return(1);
        }
        unsigned short unknUInt16File_0;
        unsigned short unknUInt16File_1;
        unsigned int offset;
        unsigned int unknUInt32File_0;
        unsigned int size;
        unsigned short fileType;
        unsigned short fileIndex;
        unsigned short unknUInt16File_2;

        filesystem::path filePath;
        filesystem::path directoryPath;
        for (i = 0; i < fileCount; i++)
        {
            fs.read(pathString, 240);

            fs.read(buffer, sizeof(unsigned short));
            memcpy(&unknUInt16File_0, buffer, sizeof(unsigned short));

            fs.read(buffer, sizeof(unsigned short));
            memcpy(&unknUInt16File_1, buffer, sizeof(unsigned short));

            fs.read(buffer, sizeof(unsigned int));
            memcpy(&offset, buffer, sizeof(unsigned int));

            fs.read(buffer, sizeof(unsigned int));
            memcpy(&unknUInt32File_0, buffer, sizeof(unsigned int));

            fs.read(buffer, sizeof(unsigned int));
            memcpy(&size, buffer, sizeof(unsigned int));

            fs.read(buffer, sizeof(unsigned short));
            memcpy(&fileType, buffer, sizeof(unsigned short));

            fs.read(buffer, sizeof(unsigned short));
            memcpy(&fileIndex, buffer, sizeof(unsigned short));

            fs.read(buffer, sizeof(unsigned short));
            memcpy(&unknUInt16File_2, buffer, sizeof(unsigned short));

            cout << pathString << endl;
            
            auto it = fileExtensions.find(fileType);
            if (it != fileExtensions.end())
            {
                filePath = unpackedFolder / pathString += fileExtensions[fileType];
            }
            else
            {
                filePath = unpackedFolder / pathString += ".";
                filePath = filePath += to_string((unsigned int)fileType);
            }
            directoryPath = filePath.parent_path();
            try
            {
                createDirectoryRecursive(directoryPath);
            }
            catch (...)
            {
                continue;
            }

            if (!filesystem::exists(filePath))
            {
                ofstream fsExt(filePath, ios::binary);
                unsigned int returnPos = fs.tellg();
                fs.seekg(offset, ios::beg);
                char* fileData = new char[size];
                fs.read(fileData, size);
                fsExt.write(fileData, size);
                fsExt.close();
                fs.seekg(returnPos, ios::beg);
                delete[] fileData;
            }
        }
        
        free(pathString);
    }

    free(buffer);
    fs.close();
    return(0);
}

int test()
{
    char pakPathTest[31] = "D:/KI/TEST/STAGE_13_RIPTOR.PAK";
    return(unpack(pakPathTest));
}

int main(int args, char** argv)
{
    for (int i = 1; i < args; i++)
    {
        cout << argv[i] << endl;
        unpack(argv[i]);
    }
    //return(test());
    return(0);
}
