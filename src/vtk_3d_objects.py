import dataclasses

import vtk


@dataclasses.dataclass
class Vector3d:
    x: float
    y: float
    z: float

    def __add__(self, other):
        return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3d(self.x - other.x, self.y - other.y, self.z - other.z)


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
    cube_actor.SetOrigin(center.x, center.y, center.z)
    return cube_actor


def new_point(center: Vector3d, radius: float, color: vtk.vtkColor3d) -> vtk.vtkActor:
    point = vtk.vtkSphereSource()
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
    point_actor.SetOrigin(center.x, center.y, center.z)
    return point_actor


def new_cylinder(
        center: Vector3d, radius: float, height: float, rotation: Vector3d, color: vtk.vtkColor3d
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
    cylinder_actor.SetOrigin(center.x, center.y, center.z)
    cylinder_actor.RotateX(rotation.x)
    cylinder_actor.RotateY(rotation.y)
    cylinder_actor.RotateZ(rotation.z)

    return cylinder_actor


def new_polyline(points: list[Vector3d], color: vtk.vtkColor3d) -> vtk.vtkActor:
    # Create a vtkPoints object and store the points in it
    vtk_points = vtk.vtkPoints()
    for point in points:
        vtk_points.InsertNextPoint([point.x, point.y, point.z])

    vtk_polyline = vtk.vtkPolyLine()
    vtk_polyline.GetPointIds().SetNumberOfIds(len(points))
    for i in range(len(points)):
        vtk_polyline.GetPointIds().SetId(i, i)

    # Create a cell array to store the lines in and add the lines to it
    vtk_cells = vtk.vtkCellArray()
    vtk_cells.InsertNextCell(vtk_polyline)

    # Create a polydata to store everything in
    vtk_polydata = vtk.vtkPolyData()

    # Add the points to the dataset
    vtk_polydata.SetPoints(vtk_points)

    # Add the lines to the dataset
    vtk_polydata.SetLines(vtk_cells)

    # Setup actor and mapper
    polydata_mapper = vtk.vtkPolyDataMapper()
    polydata_mapper.SetInputData(vtk_polydata)

    polydata_actor = vtk.vtkActor()
    polydata_actor.SetMapper(polydata_mapper)
    polydata_actor.GetProperty().SetColor(color)  # noqa
    return polydata_actor


def new_text(text: str, size: int, position: tuple[int, int],
             frame: bool,
             color: vtk.vtkColor3d,
             bg_color: vtk.vtkColor3d,
             f_color: vtk.vtkColor3d) -> vtk.vtkTextActor:
    text_actor = vtk.vtkTextActor()
    text_actor.SetInput(text)
    text_property = text_actor.GetTextProperty()
    text_property.SetFontFamilyToArial()
    text_property.SetJustificationToCentered()
    text_property.BoldOn()
    text_property.SetFontSize(size)
    text_property.SetColor(color)
    text_property.SetFrameWidth(6)
    text_property.SetBackgroundColor(bg_color)
    text_property.SetFrame(frame)
    text_property.SetFrameColor(f_color)
    text_property.SetBackgroundOpacity(100)
    text_actor.SetDisplayPosition(*position)

    return text_actor
