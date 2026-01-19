import bpy
import os

from math import radians

from .KIMESH_Parser import KIMESHParser

def loadKIMESH(filePath, collection=None, createCollections=False, mergeMeshes=None, fixRotation=False, importMaterials=False, textureInterpolation=None):
    warnings = []

    parsedKIMESHData = KIMESHParser(path=filePath)
    meshInfos = parsedKIMESHData.read()

    fileNameFull = os.path.basename(filePath)
    fileName = os.path.basename(filePath).split(".")[0]
    if collection is None:
        master_collection = bpy.context.scene.collection
        if createCollections:
            col = bpy.data.collections.new(fileName)
            master_collection.children.link(col)
        else:
            col = master_collection
    else:
        col = collection

    returnedObjects = []

    if bpy.context.scene.view_settings.view_transform != 'Standard':
        bpy.context.scene.view_settings.view_transform = 'Standard'  # Closer to game color profile.

    for meshInfo in meshInfos:
        meshNew = bpy.data.meshes.new(meshInfo['name'])
        obj = bpy.data.objects.new(meshNew.name, meshNew)
        col.objects.link(obj)
        obj.rotation_mode = 'XYZ'
        meshNew.from_pydata(meshInfo['vertices'], [], meshInfo['faces'])
        
        bpy.context.view_layer.objects.active = obj

        if fixRotation:
            obj.rotation_euler[0] = radians(90)

        if hasattr(meshNew, 'create_normals_split'):
            meshNew.create_normals_split()
        meshNew.polygons.foreach_set('use_smooth', [True]*len(meshNew.polygons))
        #meshNew.normals_split_custom_set_from_vertices(vertexInfos['normals'])
        if hasattr(meshNew, 'use_auto_smooth'):
            meshNew.use_auto_smooth = True
        if hasattr(meshNew, 'free_normals_split'):
            meshNew.free_normals_split()

        returnedObjects.append(obj)

    return returnedObjects, warnings