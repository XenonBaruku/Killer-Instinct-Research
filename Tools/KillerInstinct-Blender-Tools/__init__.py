bl_info = {
    "name": "Killer Instinct Blender Tools",
    "author": "XenonValstrax",
    "blender": (2, 93, 0),
    "version": (0, 0, 2),
    "description": "Import mesh from game Killer Instinct (2013)",
    "warning": "",
    "category": "Import-Export",
}

import bpy
from bpy.types import Context, Menu

from .KIMESH.KIMESH_UI import KIMESH_Import


class KI_import_menu(bpy.types.Menu):
    bl_label = "Killer Instinct"
    bl_idname = "KI_MT_menu_import"

    def draw(self, context):
        self.layout.operator(KIMESH_Import.bl_idname, text="Mesh Files (.KIMSH)", icon="MESH_DATA")

def draw_import_menu(self: Menu, context: Context) -> None:
    self.layout.menu(KI_import_menu.bl_idname)

# Drag & drop import, for blender version 4.1 or later.
if bpy.app.version >= (4, 1, 0):
    class KIMESH_FH_drag_import(bpy.types.FileHandler):
        bl_idname = "KIMESH_FH_drag_import"
        bl_label = "KIMESH drag & drop file handler"
        bl_import_operator = "kimesh.import"
        bl_file_extensions = ".KIMESH"

        @classmethod
        def poll_drop(cls, context):
            return (context.area and context.area.type == 'VIEW_3D')

def register() -> None:
    bpy.utils.register_class(KIMESH_Import)
    bpy.utils.register_class(KI_import_menu)
    if bpy.app.version >= (4, 1, 0):
        bpy.utils.register_class(KIMESH_FH_drag_import)
    bpy.types.TOPBAR_MT_file_import.append(draw_import_menu)
    pass

def unregister() -> None:
    bpy.utils.unregister_class(KIMESH_Import)
    bpy.utils.unregister_class(KI_import_menu)
    if bpy.app.version >= (4, 1, 0):
        bpy.utils.unregister_class(KIMESH_FH_drag_import)
    bpy.types.TOPBAR_MT_file_import.remove(draw_import_menu)
    pass

if __name__ == "__main__":
    register()