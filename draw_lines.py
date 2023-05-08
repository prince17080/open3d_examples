import json
import os.path
import sys

import numpy as np
import open3d as o3d

def get_line_object(
        point1: np.array,
        point2: np.array,
        color
):
    points = np.vstack(
        (
            point1,
            point2
        )
    )

    lines = [
        [0, 1],
    ]

    colors = [color]

    line = o3d.geometry.LineSet()
    line.points = o3d.utility.Vector3dVector(points)
    line.lines = o3d.utility.Vector2iVector(lines)
    line.colors = o3d.utility.Vector3dVector(colors)

    return line


def get_json_object(filepath: str):
    # Opening JSON file
    f = open(filepath)

    # returns JSON object as a dictionary
    json_obj = json.load(f)

    # Closing file
    f.close()

    return json_obj


def swap_z_and_y_coordinates(point: dict):
    return np.asarray([point["_x"], point["_z"], point["_y"]])


def get_points_on_the_tooth_surface_through_tool(self, points_filepath):
    if not os.path.isfile(points_filepath):
        assert self.is_dummy, f'ERROR: Initial points json file not present for the not missing {self.name}'
        return

    points_picked = get_json_object(points_filepath)

    return swap_z_and_y_coordinates(points_picked["top_point1"]), swap_z_and_y_coordinates(points_picked["top_point2"]),


    self.crown_front = {
        "pcd_surface_point": o3d.geometry.PointCloud(o3d.utility.Vector3dVector([
            swap_z_and_y_coordinates(points_picked["front_point"]),
        ])),
    }

    self.update_crown_front_point()


def main(
        case_folder: str,
        points_folder: str,
        axes_folder: str,
):
    o3d_meshes = []
    for i in range(17, 32):
        tooth_file = os.path.join(case_folder, f'Tooth_{i}.stl')
        if not os.path.isfile(tooth_file):
            continue

        o3d_mesh = o3d.io.read_triangle_mesh(tooth_file)
        o3d_mesh.compute_vertex_normals()

        points_filepath = os.path.join(points_folder, f'Tooth_{i}_points.json')
        left_point, right_point, front_point = get_points_on_the_tooth_surface_through_tool(points_filepath)
        pcd_left_point = o3d.geometry.PointCloud(o3d.utility.Vector3dVector([
            left_point
        ]))
        pcd_right_point = o3d.geometry.PointCloud(o3d.utility.Vector3dVector([
            right_point
        ]))
        pcd_center_point = o3d.geometry.PointCloud(o3d.utility.Vector3dVector([
            (left_point + right_point) / 2
        ]))


if __name__ == "__main__":
    teeth_case_folder = sys.argv[1]
    points_folder = sys.argv[2]
    axes_folder = sys.argv[3]

    main(teeth_case_folder, points_folder, axes_folder)
