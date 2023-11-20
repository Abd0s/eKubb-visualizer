import logging

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.qt import QVTKRenderWindowInteractor
import vtk

import vtk_3d_objects

import config

logger = logging.getLogger(__name__)

team_a: bool = False
team_b: bool = True


class GameVisualizerWidget(QVTKRenderWindowInteractor.QVTKRenderWindowInteractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 3D Objects
        # Blocks
        self.blocks_team_a: list[vtk.vtkActor] = []  # 0
        self.blocks_team_b: list[vtk.vtkActor] = []  # 1
        # Stick
        self.stick_trail_data: list[vtk_3d_objects.Vector3d] = []
        self.stick = None
        self.stick_trail: list[vtk.vtkActor] = []
        # Playing-field
        self.plane = None
        # Calibration point
        self.calibration_point = None

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
                vtk_3d_objects.Vector3d(0.0, i * 0.1, (-(-(i ** 2)) * 0.1) + 10)
            )

        self.fall_block(team_a, 2)

    def init_scene(self) -> None:
        # Create cubes.
        # team A
        for i in range(-(config.block_count // 2), (config.block_count // 2) + 1):
            if not (config.block_count % 2 == 0 and i == 0):
                cube = vtk_3d_objects.new_cube(
                    vtk_3d_objects.Vector3d(-config.playing_field_size[0] / 2,
                                            float(i) * (config.playing_field_size[1] / config.block_count), 1.0),
                    vtk_3d_objects.Vector3d(1.0, 1.0, 2.0),
                    vtkNamedColors().GetColor3d("Banana"),
                )
                self.blocks_team_a.append(cube)
                self.renderer.AddActor(cube)
        # team B
        for i in range(-(config.block_count // 2), (config.block_count // 2) + 1):
            if not (config.block_count % 2 == 0 and i == 0):
                cube = vtk_3d_objects.new_cube(
                    vtk_3d_objects.Vector3d(config.playing_field_size[0] / 2,
                                            float(i) * (config.playing_field_size[1] / config.block_count), 1.0),
                    vtk_3d_objects.Vector3d(1.0, 1.0, 2.0),
                    vtkNamedColors().GetColor3d("Banana"),
                )
                self.blocks_team_b.append(cube)
                self.renderer.AddActor(cube)

        # Create plane (playing field)
        self.plane = vtk_3d_objects.new_cube(
            vtk_3d_objects.Vector3d(0.0, 0.0, 0.0),
            vtk_3d_objects.Vector3d(config.playing_field_size[0] + config.playing_field_padding,
                                    config.playing_field_size[1] + config.playing_field_padding, 0.0),
            vtkNamedColors().GetColor3d("green"),
        )

        self.renderer.AddActor(self.plane)

        # Create calibration point
        self.calibration_point = vtk_3d_objects.new_point(vtk_3d_objects.Vector3d(config.calibration_point[0], config.calibration_point[1], 0.0), 1.0,
                                                          vtkNamedColors().GetColor3d("yellow"))

        self.renderer.AddActor(self.calibration_point)

        # Create cylinder
        self.stick = vtk_3d_objects.new_cylinder(
            vtk_3d_objects.Vector3d(20.0, 0.0, 20.0),
            0.4,
            2.5,
            vtkNamedColors().GetColor3d("indigo"),
        )

        self.renderer.AddActor(self.stick)

        self.debug_init()

    def debug_init(self) -> None:
        # Origin
        origin = vtk_3d_objects.new_point(vtk_3d_objects.Vector3d(0.0, 0.0, 0.0), 1.0,
                                          vtkNamedColors().GetColor3d("red"))
        self.renderer.AddActor(origin)

    def reset_scene(self) -> None:
        self.renderer.RemoveAllViewProps()
        self.renderer.GetRenderWindow().Render()

        # 3D Objects reset
        # Blocks
        self.blocks_team_a: list[vtk.vtkActor] = []  # 0
        self.blocks_team_b: list[vtk.vtkActor] = []  # 1
        # Stick
        self.stick_trail_data: list[vtk_3d_objects.Vector3d] = []
        self.stick = None
        self.stick_trail: list[vtk.vtkActor] = []
        # Playing-field
        self.plane = None

    def reset_stick(self) -> None:
        pass

    def reset_blocks(self) -> None:
        for block_index in range(len(self.blocks_team_a)):
            self.reset_block(team_a, block_index)

        for block_index in range(len(self.blocks_team_b)):
            self.reset_block(team_b, block_index)

    def reset_block(self, team: bool, block_index: int) -> None:
        blocks = self.blocks_team_b if team else self.blocks_team_b
        try:
            if blocks[block_index].GetOrientation()[1] == -90:
                blocks[block_index].RotateY(90)
                self.renderer.GetRenderWindow().Render()
                logger.info(f"Reset block {block_index}")
            else:
                logger.warning(
                    f"Can't reset block {block_index}, already reset {blocks[block_index].GetOrientation()}"
                )
        except IndexError:
            logger.error(f"Invalid block index {block_index}")

    def fall_block(self, team: bool, block_index: int) -> None:
        blocks = self.blocks_team_b if team else self.blocks_team_b
        try:
            if blocks[block_index].GetOrientation()[1] == 0:
                blocks[block_index].RotateY(-90)
                self.renderer.GetRenderWindow().Render()
            else:
                logger.warning(
                    f"Can't fall block {block_index}, is not standing {blocks[block_index].GetOrientation()}"
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
