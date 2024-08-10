import json
import pdal
import rasterio
import numpy as np

def colorize_point_cloud(input_las, input_tif, output_las, noise_class):
    # Open the TIFF file
    with rasterio.open(input_tif) as src:
        # Read the RGB bands
        red = src.read(1)
        green = src.read(2)
        blue = src.read(3)
        transform = src.transform

    # PDAL pipeline to read the LAS file
    pipeline = [
        {
            "type": "readers.las",
            "filename": input_las
        },
        {
            "type": "filters.range",
            "limits": f"Classification![{noise_class}]"
        },
        {
            "type": "filters.colorization",
            "raster": input_tif,
            "dimensions": "Red,Green,Blue"
        },
        {
            "type": "writers.las",
            "filename": output_las
        }
    ]

    # Convert the pipeline to JSON
    pipeline_json = json.dumps(pipeline)

    # Print the pipeline for debugging purposes
    print("PDAL Pipeline JSON:")
    print(pipeline_json)

    # Execute the pipeline
    pdal_pipeline = pdal.Pipeline(pipeline_json)
    try:
        count = pdal_pipeline.execute()
        print(f"Number of points processed: {count}")
    except RuntimeError as e:
        print(f"Error executing PDAL pipeline: {e}")
        raise

if __name__ == "__main__":
    input_las = r"C:\Users\clinville\Documents\GitHub\Visualization_tools\test_Data\colorization\SW_1-1.las"
    input_tif = r"C:\Users\clinville\Documents\GitHub\Visualization_tools\test_Data\colorization\SW_1-1.tif"
    output_las = r"C:\Users\clinville\Documents\GitHub\Visualization_tools\test_Data\colorization\output_colorized.las"
    noise_class = '18:19'

    colorize_point_cloud(input_las, input_tif, output_las, noise_class)
