import numpy as np

from Project.utils.custom_types import PointIndex, Triangle, TriangleIndex
from Project.utils.triangle_search.directed_graph_dfs import dfs_trianglation_point


def test_dfs_triangulation_finds_triangle_containing_point():
    points = np.array([[0, 0], [10, 0], [0, 10], [4, 0], [0, 4]])
    triangles: list[Triangle] = [
        (PointIndex(0), PointIndex(1), PointIndex(2)),
        (PointIndex(0), PointIndex(3), PointIndex(4)),
    ]
    child_graph = [{TriangleIndex(1)}, set()]

    result = dfs_trianglation_point(
        np.array([1, 1]),
        TriangleIndex(0),
        triangles,
        child_graph,
        points,
    )

    assert result[0] == TriangleIndex(1)
