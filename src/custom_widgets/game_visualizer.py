import logging

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.qt import QVTKRenderWindowInteractor
import vtk

import vtk_3d_objects

logger = logging.getLogger(__name__)


class GameVisualizerWidget(QVTKRenderWindowInteractor.QVTKRenderWindowInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 3D Objects
        self.blocks: list[vtk.vtkActor] = []
        self.stick_trail_data: list[vtk_3d_objects.Vector3d] = []
        self.plane = None
        self.stick = None
        self.stick_trail: list[vtk.vtkActor] = []

        # Initialize VTK renderer
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(vtkNamedColors().GetColor3d("Silver"))
        self.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.GetRenderWindow().GetInteractor()

        # Initialize scene
        self.init_scene()
        self.renderer.ResetCamera()
        self.interactor.Initialize()

    def update_function(self):
        for i in range(100):
            self.append_stick_traject(
                vtk_3d_objects.Vector3d(0.0, i * 0.1, (-(-(i**2)) * 0.1) + 10)
            )

        self.fall_block(2)
        self.reset_blocks()

    def init_scene(self) -> None:
        # Create cubes.
        for i in range(-2, 3):
            cube = vtk_3d_objects.new_cube(
                vtk_3d_objects.Vector3d(0.0, float(i) * 10, 1.0),
                vtk_3d_objects.Vector3d(1.0, 1.0, 2.0),
                vtkNamedColors().GetColor3d("Banana"),
            )
            self.blocks.append(cube)
            self.renderer.AddActor(cube)

        # Create plane
        self.plane = vtk_3d_objects.new_cube(
            vtk_3d_objects.Vector3d(0.0, 0.0, 0.0),
            vtk_3d_objects.Vector3d(60.0, 60.0, 0.0),
            vtkNamedColors().GetColor3d("green"),
        )

        self.renderer.AddActor(self.plane)

        # Create cylinder
        # self.stick = vtk_3d_objects.new_cylinder(
        #     vtk_3d_objects.Vector3d(20.0, 0.0, 20.0),
        #     0.4,
        #     2.5,
        #     vtkNamedColors().GetColor3d("indigo"),
        # )

        # self.renderer.AddActor(self.stick)

    def reset_scene(self) -> None:
        self.renderer.RemoveAllViewProps()
        self.renderer.GetRenderWindow().Render()

    def reset_stick(self) -> None:
        pass

    def reset_blocks(self) -> None:
        for block_index in range(len(self.blocks)):
            self.reset_block(block_index)

    def reset_block(self, block_index: int) -> None:
        try:
            if self.blocks[block_index].GetOrientation()[1] == -90:
                self.blocks[block_index].RotateY(90)
                self.renderer.GetRenderWindow().Render()
                logger.info(f"Reset block {block_index}")
            else:
                logger.warning(
                    f"Can't reset block {block_index}, already reset {self.blocks[block_index].GetOrientation()}"
                )
        except IndexError:
            logger.error(f"Invalid block index {block_index}")

    def fall_block(self, block_index: int) -> None:
        try:
            if self.blocks[block_index].GetOrientation()[1] == 0:
                self.blocks[block_index].RotateY(-90)
                self.renderer.GetRenderWindow().Render()
            else:
                logger.warning(
                    f"Can't fall block {block_index}, is not standing {self.blocks[block_index].GetOrientation()}"
                )
        except IndexError:
            logger.error(f"Invalid block index {block_index}")

    def append_stick_traject(self, location: vtk_3d_objects.Vector3d) -> None:
        self.stick_trail_data.append(location)
        point = vtk_3d_objects.new_point(
            location, 0.1, vtkNamedColors().GetColor3d("red")
        )
        self.stick_trail.append(point)
        self.renderer.AddActor(point)
        self.renderer.GetRenderWindow().Render()
