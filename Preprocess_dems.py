import os
import rasterio
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np


def get_min_max(tif_path):
    with rasterio.open(tif_path) as src:
        array = src.read(1, masked=True)
        return tif_path, array.min(), array.max()


def detect_outliers(values):
    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return lower_bound, upper_bound


def process_directory(directory):
    tif_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.tif')]

    results = []
    with ProcessPoolExecutor() as executor:
        future_to_tif = {executor.submit(get_min_max, tif): tif for tif in tif_files}
        for future in as_completed(future_to_tif):
            tif_path, min_val, max_val = future.result()
            results.append((tif_path, min_val, max_val))
            print(f"Processed {tif_path}: min={min_val}, max={max_val}")

    min_values = [min_val for _, min_val, _ in results]
    max_values = [max_val for _, _, max_val in results]

    min_lower_bound, min_upper_bound = detect_outliers(min_values)
    max_lower_bound, max_upper_bound = detect_outliers(max_values)

    filtered_min_values = [val for val in min_values if min_lower_bound <= val <= min_upper_bound]
    filtered_max_values = [val for val in max_values if max_lower_bound <= val <= max_upper_bound]

    global_min = min(filtered_min_values)
    global_max = max(filtered_max_values)

    print(f'\nMin: {global_min}\nMax: {global_max}')
    return global_min, global_max


def rescale_and_write_tif(tif_path, global_min, global_max, output_directory):
    with rasterio.open(tif_path) as src:
        array = src.read(1, masked=True)
        rescaled_array = ((array - global_min) / (global_max - global_min) * 65535).astype(np.uint16)

        profile = src.profile
        profile.update(dtype=rasterio.uint16, nodata=0)

        output_path = os.path.join(output_directory, os.path.basename(tif_path))
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(rescaled_array, 1)

    print(f"Written rescaled file: {output_path}")


def rescale_all_tifs(directory, output_directory, global_min, global_max):
    tif_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.tif')]

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    total_files = len(tif_files)
    completed_files = 0

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(rescale_and_write_tif, tif, global_min, global_max, output_directory) for tif in
                   tif_files]
        for future in as_completed(futures):
            completed_files += 1
            print(f"Rescaled {completed_files}/{total_files} files", end='\r')


if __name__ == "__main__":
    directory = r"C:\Users\clinville\Documents\Blender\Pt_Cloud\SLV\DEMS"  # Change this to your directory path
    output_directory = r"C:\Users\clinville\Documents\Blender\Pt_Cloud\SLV\DEMS_rescaled"  # Change this to your output directory path

    overall_min, overall_max = process_directory(directory)
    rescale_all_tifs(directory, output_directory, overall_min, overall_max)
    print("\nCompleted rescaling all TIFF files.")
