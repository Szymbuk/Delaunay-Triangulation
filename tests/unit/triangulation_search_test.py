import numpy as np

from Projekt.delaunay import Triangulation


def test_find_triangle_returns_active_triangle():
    points = np.array([[0.0, 0.0], [4.0, 0.0], [4.0, 4.0], [0.0, 4.0]])
    triangulation = Triangulation(points, variant="Graph")
    triangulation.triangulate()

    triangle_id, triangle = triangulation.find_triangle(np.array([1.0, 1.0]))

    assert triangle_id in triangulation.get_triangle_ids()
    assert triangle in triangulation.get_triangulation()


def test_find_triangle_rejects_point_outside_triangulation():
    points = np.array([[0.0, 0.0], [4.0, 0.0], [4.0, 4.0], [0.0, 4.0]])
    for variant in ("Graph", "JaW"):
        triangulation = Triangulation(points, variant=variant)
        triangulation.triangulate()

        try:
            triangulation.find_triangle(np.array([2.0, -1.0]))
        except ValueError as error:
            assert "nie należy" in str(error)
        else:
            raise AssertionError(
                f"Punkt spoza triangulacji powinien zgłosić ValueError dla {variant}"
            )


def test_find_triangle_uses_jump_and_walk_trace():
    points = np.array([[0.0, 0.0], [4.0, 0.0], [4.0, 4.0], [0.0, 4.0]])
    triangulation = Triangulation(points, variant="JaW")
    triangulation.triangulate()

    triangle_id, triangle, visited = triangulation.find_triangle(
        np.array([1.0, 1.0]), trace=True
    )

    assert triangle_id in triangulation.get_triangle_ids()
    assert triangle in triangulation.get_triangulation()
    assert visited