import bpy
from pathlib import Path

# Define the path to your PLY file
ply_folder_path = r"C:\Users\clinville\Documents\Blender\Pt_Cloud\Saipan\ply_chunks"
ply_files = list(Path(ply_folder_path).glob("*.ply"))

# Function to import the PLY file
def import_ply_file(ply_files):

    for index,ply in enumerate(ply_files):

        bpy.ops.wm.ply_import(filepath=str(ply))
        imported_object = bpy.context.selected_objects[0]
        imported_object.hide_viewport = True


# Call the function to import the PLY file
import_ply_file(ply_files)
