from mathutils import Vector
from math import (
    atan, asin, cos,
    sin, tan, pi,
    radians,
)
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatVectorProperty
from bpy.types import Operator
import bpy
bl_info = {
    "name": "Grinds My Gears",
    "author": "Jonathan Crowder",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Gear",
    "description": "Adds a new Gear Mesh",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


def add_object(self, context):
    # scale_x = self.scale.x
    # scale_y = self.scale.y
    
    verts = []
    r = self.base_diameter / 2
    faces = []
    edges = []

    face = []

    for tooth in range(0, self.teeth):
        turns = tooth / self.teeth

        angle = radians(turns * 360)

        x = r * cos(angle)
        y = r * sin(angle)

        v = Vector((x,y,0))
        verts.append(v)
        face.append(tooth)

    faces.append(face)
    
    mesh = bpy.data.meshes.new(name="Gear")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Gear Mesh"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Gear Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    # scale: FloatVectorProperty(
    #     name="scale",
    #     default=(1.0, 1.0, 1.0),
    #     subtype='TRANSLATION',
    #     description="scaling",
    # )

    teeth = bpy.props.IntProperty(
        name="Z / Tooth Count",
        description="Number of gear teeth",
        default=3, 
        min=3,
        soft_max=256
    )

    base_diameter = bpy.props.FloatProperty(
        name="Base Diameter",
        description="base refers to the root of the teeth, or valley lowest point",
        default=1.0,
        min=0.01,
        soft_max=25
    )

    involute_pitch = bpy.props.FloatProperty(
        # subtype="Involute",
        description="Module / Pitch",
        name="Pitch",
        default=1.0,
        soft_min=1,
        soft_max=25
    )
    involute_pangle = bpy.props.FloatProperty(
        # subtype="Involute",
        description="Involute Pressure Angle (degrees)",
        name="Pressure Angle",
        default=20.0,
        soft_min=10.0,
        soft_max=30
    )

    def execute(self, context):

        add_object(self, context)

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Gear",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
