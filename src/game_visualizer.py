import logging

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.qt import QVTKRenderWindowInteractor
import vtk

import vtk_3d_objects

logger = logging.getLogger()


class GameVisualizerWidget(QVTKRenderWindowInteractor.QVTKRenderWindowInteractor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cubes = []
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(vtkNamedColors().GetColor3d("Silver"))
        self.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.GetRenderWindow().GetInteractor()

        self.init_scene()
        self.renderer.ResetCamera()
        self.interactor.Initialize()

    def init_scene(self) -> None:
        # Create cubes.
        for i in range(0, 5):
            cube = vtk_3d_objects.new_cube(vtk_3d_objects.Vector3d(0.0, float(i) * 10, 0.0),
                                           vtk_3d_objects.Vector3d(1.0, 1.0, 2.0))
            self.cubes.append(cube)
            self.renderer.AddActor(cube)

    def update_function(self):
        self.cubes[0].RotateX(30)
        self.renderer.GetRenderWindow().Render()
