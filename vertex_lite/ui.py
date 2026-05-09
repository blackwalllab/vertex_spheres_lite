import bpy


class VS_PT_panel(bpy.types.Panel):
    bl_label = "Vertex Spheres Lite"
    bl_idname = "VS_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vertex Lite'

    def draw(self, context):
        layout = self.layout
        props = context.scene.vs_props

        layout.prop(props, "size")
        layout.prop(props, "use_all_if_none")
        layout.separator()
        layout.operator("vs.create")
        layout.operator("vs.delete_created", icon='TRASH')
