import os
import sys

import numpy as np
import open3d as o3d


def import_teeth(teeth_set_no, teeth_folder_path, color, material=None, low=1, high=32):
    objects = []
    for i in range(low, high+1):
        filepath = os.path.join(teeth_folder_path, f'Tooth_{i}.stl')
        if not os.path.isfile(filepath):
            continue

        mesh = o3d.io.read_triangle_mesh(filepath)
        mesh.compute_vertex_normals()
        mesh.paint_uniform_color(color)

        if material is None:
            objects.append(
                {'name': f'Tooth_{i}_{teeth_set_no}', 'geometry': mesh}
                # {'name': f'Tooth_{i}_{teeth_set_no}', 'geometry': mesh, 'material': material}
            )
        else:
            objects.append(
                {'name': f'Tooth_{i}_{teeth_set_no}', 'geometry': mesh, 'material': material}
            )

    return objects


if __name__ == "__main__":
    teeth_folder_path_1 = sys.argv[1]
    teeth_folder_path_2 = sys.argv[2]

    assert os.path.isdir(teeth_folder_path_1), f'{teeth_folder_path_1}: Teeth folder path 1 does not exist'

    assert os.path.isdir(teeth_folder_path_2), f'{teeth_folder_path_2}: Teeth folder path 2 does not exist'

    mat = o3d.visualization.rendering.MaterialRecord()
    mat.base_color = np.array([1, 1, 1, .5])
    mat.shader = "defaultLitTransparency"

    teeth_1 = import_teeth(
        teeth_set_no=1,
        teeth_folder_path=teeth_folder_path_1,
        color=(0, 0.3, 0.9),
        material=mat,
    )

    teeth_2 = import_teeth(
        teeth_set_no=2,
        teeth_folder_path=teeth_folder_path_2,
        color=(0.7, 0.7, 0.7),
    )

    o3d.visualization.draw(teeth_1 + teeth_2)


