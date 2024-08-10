import laspy
import open3d as o3d
import numpy as np
from pathlib import Path
import os
from concurrent.futures import ProcessPoolExecutor, as_completed


def process_las_file(las_file_path, ply_folder, exclude_classes):
    try:
        las_to_ply = Path(las_file_path)
        ply_folder = Path(ply_folder)
        ply_folder.mkdir(parents=True, exist_ok=True)
        ply_file = str(ply_folder.joinpath(las_to_ply.stem + ".ply"))

        # Read the LAS file
        print(f"Reading LAS file: {las_file_path}")
        las = laspy.read(las_file_path)
        print(f"Number of points in LAS file: {len(las.points)}")

        # Extract point data
        mask = ~np.isin(las.classification, exclude_classes)
        points = np.vstack((las.x[mask], las.y[mask], las.z[mask])).transpose()

        print(f"Extracted {points.shape[0]} points after excluding classes {exclude_classes}")

        # Check the shape and type of the points array
        print(f"Points array shape: {points.shape}")

        # Create Open3D Point Cloud object
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        # Save the point cloud to a PLY file
        o3d.io.write_point_cloud(ply_file, pcd)
        print(f"Converted {las_file_path} to {ply_folder}")

        # Delete the original LAS file
        os.remove(las_file_path)
        print(f"Deleted original LAS file: {las_file_path}")

    except Exception as e:
        print(f"An error occurred processing {las_file_path}: {e}")


def las_to_ply(las_folder, ply_folder,filetype, exclude_classes=[]):
    las_files = list(Path(las_folder).glob(f'*.{filetype}'))
    print(las_files)
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_las_file, las_file, ply_folder, exclude_classes) for las_file in las_files]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    filetype= "laz"
    las_folder = 'C:\\Users\\clinville\\Documents\\Blender\\Pt_Cloud\\SLV'
    ply_folder = 'C:\\Users\\clinville\\Documents\\Blender\\Pt_Cloud\\SLV\\ply'
    exclude_classes = [18]  # Replace with the class numbers you want to exclude
    las_to_ply(las_folder, ply_folder,filetype, exclude_classes)
