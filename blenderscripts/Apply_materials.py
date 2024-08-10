import bpy

def create_material(material_name, color=(1, 0, 0, 1)):
    # Create a new material
    material = bpy.data.materials.new(name=material_name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
    return material

def assign_material_to_all_meshes(material):
    # Loop through all objects in the scene
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            # Make sure the object uses the material
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)

# Create a new material with the desired name and color
material_name = "NewMaterial"
color = (1, 0, 0, 1)  # RGBA for red color
material = create_material(material_name, color)

# Assign the created material to all mesh objects in the scene
assign_material_to_all_meshes(material)
