from plyfile import PlyData, PlyElement
import os
import numpy as np


def split_large_ply(file_path, num_chunks):
    # Load the PLY file
    ply_data = PlyData.read(file_path)

    # Extract the vertex elements
    vertex_data = ply_data['vertex']

    total_vertices = len(vertex_data)
    vertex_chunk_size = total_vertices // num_chunks

    print(f'Total vertices: {total_vertices}')
    print(f'Vertex chunk size: {vertex_chunk_size}')

    output_dir = 'ply_chunks'
    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_chunks):
        start_vertex_idx = i * vertex_chunk_size
        end_vertex_idx = start_vertex_idx + vertex_chunk_size if i < num_chunks - 1 else total_vertices

        # Extract the chunk data
        vertex_chunk = vertex_data[start_vertex_idx:end_vertex_idx]

        # Create new PLY elements for the chunks
        vertex_element = PlyElement.describe(vertex_chunk, 'vertex')

        # Create a new PLY file for the chunk
        chunk_ply_data = PlyData([vertex_element])
        chunk_file_path = os.path.join(output_dir, f'chunk_{i + 1}.ply')
        chunk_ply_data.write(chunk_file_path)

        print(f'Saved {chunk_file_path}')

    print('PLY file split into chunks successfully.')


# Usage example
split_large_ply(r"P:\23105_NHAP_2023_2024\US_PAC_Islands\project\Saipan_pts.ply", 10)

