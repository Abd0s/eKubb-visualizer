import dataclasses

from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper
)
from vtkmodules.vtkCommonColor import vtkNamedColors
import dataclasses


@dataclasses.dataclass
class Vector3d:
    x: float
    y: float
    z: float


def new_cube(center: Vector3d, size: Vector3d) -> vtkActor:
    cube = vtkCubeSource()

    cube.SetXLength(size.x)
    cube.SetYLength(size.y)
    cube.SetZLength(size.z)

    cube.SetCenter(center.x, center.y, center.z)
    cube.Update()

    # mapper
    cubeMapper = vtkPolyDataMapper()
    cubeMapper.SetInputData(cube.GetOutput())

    # Actor.
    cubeActor = vtkActor()
    cubeActor.SetMapper(cubeMapper)
    cubeActor.GetProperty().SetColor(vtkNamedColors().GetColor3d('Banana'))
    return cubeActor


def new_cylinder(center: Vector3d, size: Vector3d) -> vtkActor:
    pass
