import bpy

from .utils import (
    MAP_KEY,
    enter_mode,
    get_all_vertex_indices,
    get_selected_vertex_indices,
    hard_bind_to_vertex_exact,
    mesh_world_positions,
)


class VS_OT_create(bpy.types.Operator):
    bl_idname = "vs.create"
    bl_label = "Create Spheres"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        src = context.active_object

        if not src or src.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}

        props = context.scene.vs_props
        prev_mode = src.mode

        if src.mode == 'EDIT':
            indices = get_selected_vertex_indices(src)
        else:
            indices = []

        if not indices and props.use_all_if_none:
            indices = get_all_vertex_indices(src)

        if not indices:
            self.report({'ERROR'}, "No vertices selected")
            return {'CANCELLED'}

        enter_mode(src, 'OBJECT')
        positions = mesh_world_positions(src)

        created_names = []
        for v_index in indices:
            world_pos = positions[v_index]
            bpy.ops.mesh.primitive_uv_sphere_add(radius=props.size, location=world_pos)
            child = bpy.context.active_object
            hard_bind_to_vertex_exact(child, src, world_pos, v_index)
            created_names.append(child.name)

        src[MAP_KEY] = created_names
        enter_mode(src, prev_mode)

        self.report({'INFO'}, f"Created {len(created_names)} bound sphere(s)")
        return {'FINISHED'}


class VS_OT_delete_created(bpy.types.Operator):
    bl_idname = "vs.delete_created"
    bl_label = "Delete Created"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        src = context.active_object

        if not src or src.type != 'MESH':
            self.report({'ERROR'}, "Select the source mesh object")
            return {'CANCELLED'}

        names = list(src.get(MAP_KEY, []))
        removed = 0

        for name in names:
            obj = bpy.data.objects.get(name)
            if obj:
                bpy.data.objects.remove(obj, do_unlink=True)
                removed += 1

        if MAP_KEY in src:
            del src[MAP_KEY]

        self.report({'INFO'}, f"Deleted {removed} sphere(s)")
        return {'FINISHED'}
