"""PyQt widget visualizing the eKubb game using VTK

"""
import logging
import random

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.qt import QVTKRenderWindowInteractor
import vtk
from PyQt5 import QtCore

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
        self.stick_trail_data: list[
            tuple[vtk_3d_objects.Vector3d, vtk_3d_objects.Vector3d]
        ] = []
        self.stick: vtk.vtkActor | None = None
        self.stick_trail: list[vtk.vtkActor] = []
        self.playing_team: bool = team_b
        # Playing-field
        self.plane = None
        # Initialize VTK renderer
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(vtkNamedColors().GetColor3d("Silver"))
        self.GetRenderWindow().AddRenderer(self.renderer)
        self.renderer.GetActiveCamera().SetViewAngle(45)
        self.interactor = self.GetRenderWindow().GetInteractor()
        # Text
        self.illegal_throw_indicator = None
        # Initialize scene
        self.init_scene()
        self.renderer.ResetCamera()
        self.interactor.Initialize()

    def init_scene(self) -> None:
        """Initialises the scene to the starting state by creating the blocks, playig field and other 3D objects."""
        # Create cubes.
        # team A
        for i in range(-(config.block_count // 2), (config.block_count // 2) + 1):
            if not (config.block_count % 2 == 0 and i == 0):
                cube = vtk_3d_objects.new_cube(
                    vtk_3d_objects.Vector3d(
                        -config.playing_field_size[0] / 2,
                        float(i) * (config.playing_field_size[1] / config.block_count),
                        1.0,
                    ),
                    vtk_3d_objects.Vector3d(1.0, 1.0, 2.0),
                    vtkNamedColors().GetColor3d("Banana"),
                )
                self.blocks_team_a.append(cube)
                self.renderer.AddActor(cube)
        # team B
        for i in range(-(config.block_count // 2), (config.block_count // 2) + 1):
            if not (config.block_count % 2 == 0 and i == 0):
                cube = vtk_3d_objects.new_cube(
                    vtk_3d_objects.Vector3d(
                        config.playing_field_size[0] / 2,
                        float(i) * (config.playing_field_size[1] / config.block_count),
                        1.0,
                    ),
                    vtk_3d_objects.Vector3d(1.0, 1.0, 2.0),
                    vtkNamedColors().GetColor3d("Banana"),
                )
                self.blocks_team_b.append(cube)
                self.renderer.AddActor(cube)

        # Create plane (playing field)
        self.plane = vtk_3d_objects.new_cube(
            vtk_3d_objects.Vector3d(0.0, 0.0, -2.5),
            vtk_3d_objects.Vector3d(
                config.playing_field_size[0] + config.playing_field_padding,
                config.playing_field_size[1] + config.playing_field_padding,
                5.0,
            ),
            vtkNamedColors().GetColor3d("green"),
        )

        play_field_lines_x_1 = vtk_3d_objects.new_cube(
            vtk_3d_objects.Vector3d(0.0, config.playing_field_size[1] / 2, 0.1),
            vtk_3d_objects.Vector3d(config.playing_field_size[0], 0.25, 0.0),
            vtkNamedColors().GetColor3d("black"),
        )

        play_field_lines_x_2 = vtk_3d_objects.new_cube(
            vtk_3d_objects.Vector3d(0.0, -config.playing_field_size[1] / 2, 0.1),
            vtk_3d_objects.Vector3d(config.playing_field_size[0], 0.25, 0.0),
            vtkNamedColors().GetColor3d("black"),
        )

        play_field_lines_y_1 = vtk_3d_objects.new_cube(
            vtk_3d_objects.Vector3d(config.playing_field_size[0] / 2, 0.0, 0.1),
            vtk_3d_objects.Vector3d(0.25, config.playing_field_size[1], 0.0),
            vtkNamedColors().GetColor3d("black"),
        )

        play_field_lines_y_2 = vtk_3d_objects.new_cube(
            vtk_3d_objects.Vector3d(-config.playing_field_size[0] / 2, 0.0, 0.1),
            vtk_3d_objects.Vector3d(0.25, config.playing_field_size[1], 0.0),
            vtkNamedColors().GetColor3d("black"),
        )

        play_field_lines_middle = vtk_3d_objects.new_cube(
            vtk_3d_objects.Vector3d(0.0, 0.0, 0.1),
            vtk_3d_objects.Vector3d(0.25, config.playing_field_size[1], 0.0),
            vtkNamedColors().GetColor3d("black"),
        )

        self.renderer.AddActor(play_field_lines_middle)
        self.renderer.AddActor(play_field_lines_y_1)
        self.renderer.AddActor(play_field_lines_y_2)
        self.renderer.AddActor(play_field_lines_x_1)
        self.renderer.AddActor(play_field_lines_x_2)
        self.renderer.AddActor(self.plane)

        # Create calibration point
        calibration_point_a = vtk_3d_objects.new_point(
            vtk_3d_objects.Vector3d(
                config.calibration_point_a[0],
                config.calibration_point_a[1],
                config.calibration_point_a[2],
            ),
            1.0,
            vtkNamedColors().GetColor3d("yellow"),
        )

        self.renderer.AddActor(calibration_point_a)

        calibration_point_b = vtk_3d_objects.new_point(
            vtk_3d_objects.Vector3d(
                config.calibration_point_b[0],
                config.calibration_point_b[1],
                config.calibration_point_b[2],
            ),
            1.0,
            vtkNamedColors().GetColor3d("blue"),
        )

        self.renderer.AddActor(calibration_point_b)

        # Create cylinder
        calibration_point = (
            config.calibration_point_b
            if self.playing_team
            else config.calibration_point_a
        )
        self.stick = vtk_3d_objects.new_cylinder(
            vtk_3d_objects.Vector3d(
                calibration_point[0], calibration_point[1], calibration_point[2]
            ),
            config.stick_radius,
            config.stick_height,
            vtk_3d_objects.Vector3d(90.0, 0.0, 0.0),
            vtkNamedColors().GetColor3d("indigo"),
        )

        self.renderer.AddActor(self.stick)

        if config.debug:
            self.debug_init()

    def debug_init(self) -> None:
        """Creates debuging objects."""
        # Origin
        origin = vtk_3d_objects.new_point(
            vtk_3d_objects.Vector3d(0.0, 0.0, 0.0),
            1.0,
            vtkNamedColors().GetColor3d("red"),
        )
        self.renderer.AddActor(origin)

    def update_function(self):
        """Called when the demo button is pressed."""
        self.indicate_illegal_throw()
        self.reset_stick()
        self.fall_block(team_a, 0)

    def draw_dummy_traject(self, block_index: int):
        if block_index == 0:
            x = [i * 0.04 for i in range(200)]
            y = [1 - (i * 0.013) for i in range(200)]
            z = [-0.0476 * (i**2) + 0.281 * i + 0.8 for i in x]

            x = [i * -10 for i in x]
            y = [i * 10 for i in y]
            z = [i * 10 for i in z]
            for i in range(200):
                self.append_stick_traject(
                    vtk_3d_objects.Vector3d(x[i] - 20, y[i], z[i]),
                    vtk_3d_objects.Vector3d(90.0, 10.0 * i, 15.0 * i),
                )
        elif block_index == 1:
            x = [i * 0.04 for i in range(200)]
            y = [2 - (i * 0.01) for i in range(200)]
            z = [-0.0476 * (i**2) + 0.281 * i + 0.8 for i in x]

            x = [i * -10 for i in x]
            y = [i * 10 for i in y]
            z = [i * 10 for i in z]
            for i in range(200):
                self.append_stick_traject(
                    vtk_3d_objects.Vector3d(x[i] - 20, y[i], z[i]),
                    vtk_3d_objects.Vector3d(90.0, 10.0 * i, 15.0 * i),
                )

        elif block_index == 2:
            x = [i * 0.04 for i in range(200)]
            y = [(i * 0.008) for i in range(200)]
            z = [-0.0476 * (i**2) + 0.281 * i + 0.8 for i in x]

            x = [i * -10 for i in x]
            y = [i * 10 for i in y]
            z = [i * 10 for i in z]
            for i in range(200):
                self.append_stick_traject(
                    vtk_3d_objects.Vector3d(x[i] - 20, y[i], z[i]),
                    vtk_3d_objects.Vector3d(90.0, 10.0 * i, 15.0 * i),
                )

        else:
            logger.error(f"Invalid block index: {block_index}")

    def reset_scene(self) -> None:
        """Empty the scene and reset the instance state."""
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
        """Resets the stick and throwstick trajectory to the calibration point."""
        for trail in self.stick_trail:
            self.renderer.RemoveActor(trail)

        self.renderer.RemoveActor(self.stick)

        self.stick_trail_data: list[vtk_3d_objects.Vector3d] = []
        self.stick_trail: list[vtk.vtkActor] = []

        # Create cylinder
        calibration_point = (
            config.calibration_point_b
            if self.playing_team
            else config.calibration_point_a
        )
        self.stick = vtk_3d_objects.new_cylinder(
            vtk_3d_objects.Vector3d(
                calibration_point[0], calibration_point[1], calibration_point[2]
            ),
            config.stick_radius,
            config.stick_height,
            vtk_3d_objects.Vector3d(90.0, 0.0, 0.0),
            vtkNamedColors().GetColor3d("indigo"),
        )

        self.renderer.AddActor(self.stick)
        self.renderer.GetRenderWindow().Render()

    def reset_blocks(self) -> None:
        """Resets all blocks in the game."""
        for block_index in range(len(self.blocks_team_a)):
            self.reset_block(team_a, block_index)

        for block_index in range(len(self.blocks_team_b)):
            self.reset_block(team_b, block_index)

    def reset_block(self, team: bool, block_index: int) -> None:
        """Resets the given block to stand up again.

        Args:
            team: The team of whoes block to reset.
            block_index: The index of the block to reset.
        """
        blocks = self.blocks_team_b if team else self.blocks_team_a
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
        """Updates the given block to have fallen over.

        Args:
            team: The team of whoes block to fall over.
            block_index: The index of the block to fall over.
        """
        blocks = self.blocks_team_b if team else self.blocks_team_a
        try:
            if blocks[block_index].GetOrientation()[1] == 0:
                blocks[block_index].RotateY(-90)
                blocks[block_index].RotateX(random.randrange(-15, 15))
                self.renderer.GetRenderWindow().Render()
            else:
                logger.warning(
                    f"Can't fall block {block_index}, is not standing {blocks[block_index].GetOrientation()}"
                )
        except IndexError:
            logger.error(f"Invalid block index {block_index}")

    def move_block(
        self, team: bool, block_index: int, location: vtk_3d_objects.Vector3d
    ) -> None:
        """Move the given block to the new given location.

        Args:
            team: The team of whoes block to move.
            block_index: The index of the block to move.
            location: The new location of the block.
        """
        blocks = self.blocks_team_b if team else self.blocks_team_a
        try:
            self.renderer.RemoveActor(blocks[block_index])
            moved_block = vtk_3d_objects.new_cube(
                location,
                vtk_3d_objects.Vector3d(1.0, 1.0, 2.0),
                vtkNamedColors().GetColor3d("Banana"),
            )

            moved_block.SetOrientation(*blocks[block_index].GetOrientation())
            blocks[block_index] = moved_block
            self.renderer.AddActor(moved_block)
        except IndexError:
            logger.error(f"Invalid block index {block_index}")

        self.renderer.GetRenderWindow().Render()

    def append_stick_traject(
        self, location: vtk_3d_objects.Vector3d, rotation: vtk_3d_objects.Vector3d
    ) -> None:
        """Append a new location of the throwstick and update the shown trajectory and throwstick.

        Args:
            location: The coordiantes of the new position to append
            rotation: The rotation change of the throwstick to append
        """
        calibration_point = (
            config.calibration_point_b
            if self.playing_team
            else config.calibration_point_a
        )
        # Update trial
        self.stick_trail_data.append((location, rotation))
        point = vtk_3d_objects.new_point(
            location
            + vtk_3d_objects.Vector3d(
                calibration_point[0], calibration_point[1], calibration_point[2]
            ),
            0.3,
            vtkNamedColors().GetColor3d("red"),
        )
        self.stick_trail.append(point)
        self.renderer.AddActor(point)
        # Move stick
        self.renderer.RemoveActor(self.stick)
        self.stick = self.stick = vtk_3d_objects.new_cylinder(
            location
            + vtk_3d_objects.Vector3d(
                calibration_point[0], calibration_point[1], calibration_point[2]
            ),
            config.stick_radius,
            config.stick_height,
            rotation,
            vtkNamedColors().GetColor3d("indigo"),
        )
        self.renderer.AddActor(self.stick)
        self.renderer.GetRenderWindow().Render()

    def indicate_illegal_throw(self) -> None:
        """Shows an indicator informing about an illegal throw."""
        if self.illegal_throw_indicator is not None:
            self.renderer.RemoveActor(self.illegal_throw_indicator)

        indicate_position = (
            self.renderer.GetRenderWindow().GetActualSize()[0] // 2,
            self.renderer.GetRenderWindow().GetActualSize()[1] // 2,
        )
        self.illegal_throw_indicator = vtk_3d_objects.new_text(
            "--------------------\nONGELDIGE WORP!\n--------------------",
            100,
            indicate_position,
            True,
            vtkNamedColors().GetColor3d("white"),
            vtkNamedColors().GetColor3d("red"),
            vtkNamedColors().GetColor3d("white"),
        )
        self.renderer.AddActor(self.illegal_throw_indicator)
        self.renderer.GetRenderWindow().Render()

        QtCore.QTimer().singleShot(5000, self.decay_illegal_throw_indicate)

    def decay_illegal_throw_indicate(self) -> None:
        """Removes the illigal throw indicator if one exists."""
        try:
            self.renderer.RemoveActor(self.illegal_throw_indicator)
        except:  # noqa (disable IDE warning for to broad excep statement), specific execption should be added
            pass

        self.illegal_throw_indicator = None
        self.renderer.GetRenderWindow().Render()
