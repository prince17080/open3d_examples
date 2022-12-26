import argparse
import errno
import os.path
import shutil

import numpy as np
import open3d as o3d


def renew_folder(folder_path):
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)

    os.makedirs(folder_path)


# To detect the collision between teeth using Ray casting operation in open3d
def check_collision(
        mesh: o3d.geometry.TriangleMesh,
        mesh2: o3d.geometry.TriangleMesh,
):
    scene = o3d.t.geometry.RaycastingScene()
    mesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh_legacy=mesh)

    _ = scene.add_triangles(mesh)

    query_points = o3d.core.Tensor(np.asarray(mesh2.vertices), dtype=o3d.core.Dtype.Float32)

    signed_distance = scene.compute_signed_distance(query_points)
    minimum_distance = min(signed_distance.numpy())

    return minimum_distance


# To detect if a point is outside the tooth
def is_point_outside_the_tooth(
        mesh: o3d.geometry.TriangleMesh,
        points,
):
    scene = o3d.t.geometry.RaycastingScene()
    mesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh_legacy=mesh)

    _ = scene.add_triangles(mesh)

    query_points = o3d.core.Tensor(np.asarray(points), dtype=o3d.core.Dtype.Float32)

    # Compute the signed distance for N random points
    signed_distance = scene.compute_signed_distance(query_points)
    minimum_distance = min(signed_distance.numpy())

    return minimum_distance > 0


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mesh1_path",
        "-m1p",
        help="path of STL file for mesh1 with file extension"
    )

    parser.add_argument(
        "--mesh2_path",
        "-m1p",
        help="path of STL file for mesh2 with file extension"
    )

    parser.add_argument(
        "--output-folder",
        "-of",
        help="path to save the output mesh, if any",
    )

    args = parser.parse_args()

    if not os.path.isfile(args.mesh1_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.mesh1_path)

    if not os.path.isfile(args.mesh2_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.mesh2_path)

    renew_folder(args.output_folder)

    return args


if __name__ == "__main__":
    args = get_arguments()

    mesh1 = o3d.io.read_triangle_mesh(filename=args.mesh1_path)
    mesh2 = o3d.io.read_triangle_mesh(filename=args.mesh2_path)

    collision_distance = check_collision(
        mesh=mesh1,
        mesh2=mesh2,
    )

    print(f'Collision distance between the given 2 meshes is {collision_distance}')
