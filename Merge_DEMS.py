import os
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob


def merge_tifs(input_directory, output_path):
    # Find all the tif files in the input directory
    tif_files = glob.glob(os.path.join(input_directory, '*.tif'))

    # Open all the tif files
    src_files_to_mosaic = []
    for fp in tif_files:
        src = rasterio.open(fp)
        src_files_to_mosaic.append(src)

    # Merge the tif files
    mosaic, out_trans = merge(src_files_to_mosaic)

    # Update the metadata
    out_meta = src.meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans,
        "compress": "lzw"  # Adding compression to reduce file size
    })

    # Write the mosaic to the output file
    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(mosaic)

    print(f"Merged file saved at {output_path}")


if __name__ == "__main__":
    input_directory = r"C:\Users\clinville\Documents\Blender\Pt_Cloud\SLV\DEMS_rescaled"  # Change this to your input directory path
    output_path = r"C:\Users\clinville\Documents\Blender\Pt_Cloud\SLV\DEMS_rescaled\merged_dem.tif"  # Change this to your output file path

    merge_tifs(input_directory, output_path)
