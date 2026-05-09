import bpy


class VSProps(bpy.types.PropertyGroup):
    size: bpy.props.FloatProperty(
        name="Sphere Size",
        default=0.08,
        min=0.0001,
    )

    use_all_if_none: bpy.props.BoolProperty(
        name="If none selected → use all verts",
        default=True,
    )
