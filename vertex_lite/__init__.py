bl_info = {
    "name": "Vertex Lite",
    "author": "Blackwall",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > N-panel > Vertex Lite",
    "description": "Create spheres hard-bound to mesh vertices",
    "category": "Object",
}

from .properties import VSProps
from .operators import VS_OT_create, VS_OT_delete_created
from .ui import VS_PT_panel

classes = (
    VSProps,
    VS_OT_create,
    VS_OT_delete_created,
    VS_PT_panel,
)


def register():
    import bpy
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.vs_props = bpy.props.PointerProperty(type=VSProps)


def unregister():
    import bpy
    if hasattr(bpy.types.Scene, "vs_props"):
        del bpy.types.Scene.vs_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
