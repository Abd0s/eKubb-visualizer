import dataclasses

import vtk


@dataclasses.dataclass
class Vector3d:
    x: float
    y: float
    z: float


def new_cube(center: Vector3d, size: Vector3d, color: vtk.vtkColor3d) -> vtk.vtkActor:
    cube = vtk.vtkCubeSource()
    cube.SetXLength(size.x)
    cube.SetYLength(size.y)
    cube.SetZLength(size.z)

    cube.SetCenter(center.x, center.y, center.z)
    cube.Update()

    # Mapper
    cube_mapper = vtk.vtkPolyDataMapper()
    cube_mapper.SetInputData(cube.GetOutput())

    # Actor
    cube_actor = vtk.vtkActor()
    cube_actor.SetMapper(cube_mapper)
    cube_actor.GetProperty().SetColor(color)  # noqa
    return cube_actor


def new_point(center: Vector3d, radius: float, color: vtk.vtkColor3d) -> vtk.vtkActor:
    point = vtk.vtkPointSource()
    point.SetRadius(radius)
    point.SetCenter(center.x, center.y, center.z)
    point.Update()

    # Mapper
    point_mapper = vtk.vtkPolyDataMapper()
    point_mapper.SetInputData(point.GetOutput())

    # Actor
    point_actor = vtk.vtkActor()
    point_actor.SetMapper(point_mapper)
    point_actor.GetProperty().SetColor(color)  # noqa
    return point_actor


def new_cylinder(
    center: Vector3d, radius: float, height: float, color: vtk.vtkColor3d
) -> vtk.vtkActor:
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetRadius(radius)
    cylinder.SetHeight(height)
    cylinder.SetResolution(80)
    cylinder.SetCenter(center.x, center.y, center.z)
    cylinder.Update()

    # Mapper
    cylinder_mapper = vtk.vtkPolyDataMapper()
    cylinder_mapper.SetInputData(cylinder.GetOutput())

    # Actor
    cylinder_actor = vtk.vtkActor()
    cylinder_actor.SetMapper(cylinder_mapper)
    cylinder_actor.GetProperty().SetColor(color)  # noqa
    return cylinder_actor
