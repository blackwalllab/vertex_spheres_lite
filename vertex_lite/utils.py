import bpy
import bmesh
from mathutils import Matrix, Vector

MAP_KEY = "vs_created_objects"


def enter_mode(obj, mode):
    if bpy.context.active_object != obj:
        bpy.context.view_layer.objects.active = obj
    if obj.mode != mode:
        bpy.ops.object.mode_set(mode=mode)


def get_selected_vertex_indices(mesh_obj):
    bm = bmesh.from_edit_mesh(mesh_obj.data)
    bm.verts.ensure_lookup_table()
    return [v.index for v in bm.verts if v.select]


def get_all_vertex_indices(mesh_obj):
    return list(range(len(mesh_obj.data.vertices)))


def mesh_world_positions(mesh_obj):
    return [mesh_obj.matrix_world @ v.co for v in mesh_obj.data.vertices]


def hard_bind_to_vertex_exact(child, parent_mesh, world_target, v_index):
    child.parent = parent_mesh
    child.parent_type = 'VERTEX'
    child.parent_vertices = [int(v_index), int(v_index), int(v_index)]
    child.matrix_parent_inverse = Matrix.Identity(4)
    bpy.context.view_layer.update()

    mesh_world_inv = parent_mesh.matrix_world.inverted()
    vertex_local = parent_mesh.data.vertices[v_index].co.copy()
    desired_local = mesh_world_inv @ world_target
    local_delta = desired_local - vertex_local

    if local_delta.length <= 1e-8:
        child.location = Vector((0.0, 0.0, 0.0))
    else:
        child.location = local_delta

    child.rotation_euler = (0.0, 0.0, 0.0)
    bpy.context.view_layer.update()
