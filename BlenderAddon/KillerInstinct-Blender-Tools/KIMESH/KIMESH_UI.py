import bpy
import os
import addon_utils

from bpy.types import Panel, Operator, OperatorFileListElement
from bpy.props import CollectionProperty, StringProperty, BoolProperty, EnumProperty
from bpy_extras.io_utils import ImportHelper

from .KIMESH_Loader import loadKIMESH


class KIMESH_Import_Panel:
    @staticmethod
    def draw_options(panel: Panel | Operator, context) -> None:
        box = panel.layout.box()
        box.label(text="Options", icon="SETTINGS")
        col = box.column()
        col.row().prop(panel, "createCollections")
        col.separator()
        col.row().prop(panel, "fixRotation")
        col.separator()
        # col.row().prop(panel, "mergeMeshes")
        # col.separator()
        # col.row().prop(panel, "importMaterials")
        # col.separator()
        # if panel.importMaterials:
        #     col.row().label(text="Texture Interpolation: ")
        #     col.row().prop(panel, "textureInterpolation")
        #     col.separator()


class KIMESH_Import(bpy.types.Operator, ImportHelper):
    '''Import Killer Instinct KIMESH Files'''
    bl_idname = "kimesh.import"
    bl_label = 'Import KIMESH'
    bl_options = {'PRESET', 'UNDO'}
    filename_ext = "*.KIMESH"

    files: CollectionProperty(type=OperatorFileListElement)
    directory : StringProperty(
			subtype = 'DIR_PATH',
			options = {'SKIP_SAVE'}
	)
    filter_glob: StringProperty(default="*.KIMESH")

    createCollections: BoolProperty(
        name = "Create Collections", 
        description = "Create collections for imported meshes, bounding planes, etc.",
        default = True
    )
    mergeMeshes: BoolProperty(
        name = "Merge Meshes", 
        description = "Merge imported meshes.",
        default = False
    )
    fixRotation: BoolProperty(
        name = "Fix Rotation", 
        description = "Convert imported objects from Y up to Z up.",
        default = True
    )
    importMaterials: BoolProperty(
        name = "Import Materials", 
        description = "Import textures and auto setup materials. Make sure textures path in addon preferences is set correctly.",
        default = True
    )
    textureInterpolation: EnumProperty(
        #name ="Interpolation",
        name = "",
		description = "Interpolation mode for imported textures",
		items = [
                ("Linear", "Linear", "Linear interpolation."),
                ("Closest", "Closest", "Closest interpolation."),
				("Cubic", "Cubic", "Cubic interpolation."),
                ("Smart", "Smart", "Smart interpolation.")
			   ],
        default = "Linear"
    )

    def draw(self, context):
        KIMESH_Import_Panel.draw_options(self, context)
    
    def execute(self, context):

        if self.files:
            folder = (os.path.dirname(self.filepath))
            filepaths = [os.path.join(folder, x.name) for x in self.files]
        else:
            filepaths = [str(self.filepath)]
        
        for filepath in filepaths:
            objs, warnings = loadKIMESH(filepath, None, self.createCollections, self.mergeMeshes, self.fixRotation, self.importMaterials, self.textureInterpolation)
            for warning in warnings:
                self.report({"WARNING"}, warning)
        return {"FINISHED"}
    
    def invoke(self, context, event):
        if self.directory:
            context.window_manager.invoke_props_dialog(self)
        else:
            context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}