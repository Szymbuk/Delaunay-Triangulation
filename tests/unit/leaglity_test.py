from Project.utils.custom_types import PointIndex, TriangleIndex, Triangle
from Project.utils.triangle_operations.legality import turned_points


def test_turned_points_returns_correct_points():
    adjacency_graph = {
        (PointIndex(0), PointIndex(1)): (TriangleIndex(0), TriangleIndex(1)),
    }
    triangles: list[Triangle] = [
        (PointIndex(0), PointIndex(1), PointIndex(2)),
        (PointIndex(1), PointIndex(0), PointIndex(3)),
    ]

    result = turned_points(
        PointIndex(0),
        PointIndex(1),
        adjacency_graph,
        triangles,
    )

    assert set(result) == {PointIndex(2), PointIndex(3)}
