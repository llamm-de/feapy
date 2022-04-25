import os
import re
import pandas as pd
import meshio
import numpy as np


class Postprocessor:
    def __init__(self, working_directory):
        self.workin_directory = working_directory

    def get_volume(self, deformed=True, dataframe=True, normalize=True):
        vtu_files = self._get_files("vtu")
        vol = []
        timestep = []

        for file in vtu_files:
            mesh_data = meshio.read(file.path)
            vol.append(self._volume(mesh_data, deformed))
            timestep.append(file.id)

        if normalize:
            ref = vol[0]
            for entry in vol:
                entry = entry / ref

        if dataframe:
            return pd.DataFrame({"timestep": timestep, "volume": vol})

        return vol, timestep

    def _volume(self, mesh_data, deformed):
        """
        Compute volume for overall mesh
        """
        volume = 0
        for i in range(len(mesh_data.cells_dict["hexahedron"])):
            volume += self._get_element_volume(i, mesh_data, deformed)
        return volume

    def _get_element_volume(
        self,
        element_number,
        mesh_data,
        deformed,
        tet_connectivity=[
            [1, 2, 3, 6],
            [0, 1, 3, 4],
            [1, 4, 5, 6],
            [3, 4, 6, 7],
            [1, 3, 4, 6],
        ],
    ):
        """
        Compute volume for specific element

        This method devides the hexahedron element into five tetrahedra for which
        the volume can easily be calculated analytically.
        """
        vertices = self._get_element_vertices(element_number, mesh_data, deformed)
        volume = 0
        for tet in range(5):
            # Construct vertex coordinate matrix for tetrahedron
            tet_vertex_matrix = np.zeros((4, 4))
            for i, tet_vertex in enumerate(tet_connectivity[tet]):
                tet_vertex_matrix[i, 0:3] = vertices[tet_vertex]
                tet_vertex_matrix[i, 3] = 1

            # Sum up volume
            volume += abs(np.linalg.det(tet_vertex_matrix)) / 6

        return volume

    def _get_element_vertices(self, element_number, mesh_data, deformed):
        """
        Get list of vertex coordinates for a specific element
        """
        coordinates = []
        element_connectivity = mesh_data.cells_dict["hexahedron"][element_number]
        for node_id in element_connectivity:
            local_coordinates = mesh_data.points[node_id]

            if deformed:
                displacements = mesh_data.point_data["Displacements"][node_id][0:3]
                local_coordinates = mesh_data.points[node_id] + displacements

            coordinates.append(local_coordinates)

        return coordinates

    def _get_files(self, extension):
        """
        Get files by extension from directory

        Returns a list of vtu_file objects
        """
        regex = re.compile(r"\d+")
        files = []
        for file in os.listdir(self.workin_directory):
            if file.endswith(f".{extension}") or file.endswith(extension):
                f = vtu_file(
                    os.path.join(self.workin_directory, file),
                    int(regex.findall(file)[0]),
                )
                files.append(f)
                continue
        files.sort(key=lambda x: x.path)

        return files


class vtu_file:
    """
    Simple dataclass to store information about vtu_files
    """

    def __init__(self, path, id):
        self.path = path
        self.id = id
