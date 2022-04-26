import numpy as np
from numpy import linalg as LA
import xml.etree.ElementTree as ElementTree


class VTURefactorer:
    def __init__(self, vtufile, refactoring_pattern):
        self.vtu_file = vtufile
        self.pattern = refactoring_pattern

    def refactor(self):
        # Refactor data
        refactored_data = {}
        point_data = self.vtu_file.get_PointData()
        for key in self.pattern:
            if key in point_data:
                refactored_data[key] = self.refactor_by_pattern(
                    point_data[key],
                    self.vtu_file.number_of_points,
                    self.pattern[key],
                )
            else:
                raise RuntimeError("{} not found in PointData.".format(key))

        # Add refactored data to tree
        for key in self.pattern:
            for new_key in refactored_data[key]:
                parent = self.vtu_file.root.findall("*/*/PointData")
                child = ElementTree.SubElement(parent[0], "DataArray")
                child.set("type", "Float64")
                child.set("Name", new_key)
                child.set(
                    "NumberOfComponents",
                    str(refactored_data[key][new_key]["NumberOfComponents"]),
                )
                child.set("format", "ascii")
                child.text = " ".join(map(str, refactored_data[key][new_key]["Data"]))

        # Remove refactored fields
        for key in self.pattern:
            for parent in self.vtu_file.root.findall("*/*/PointData"):
                for element in parent.findall("DataArray"):
                    if element.get("Name") == key:
                        parent.remove(element)

    def reshape_data(self, dataset, num_entities):
        num_components = dataset["NumberOfComponents"]
        raw_data = dataset["Data"]
        data = np.ndarray(shape=(num_entities, num_components))

        for i in range(num_entities):
            data[i, :] = raw_data[i * num_components : ((i + 1) * num_components)]

        return data

    def refactor_by_pattern(self, dataset, num_entities, pattern):
        data = self.reshape_data(dataset, num_entities)

        refactored_data = {}
        for key in pattern:
            length = pattern[key]["Len"]
            start = pattern[key]["Start"]
            refactored_data[key] = {}
            refactored_data[key]["NumberOfComponents"] = length

            new_array = np.zeros(length * num_entities)
            for i in range(num_entities):
                entity_data = data[i, start : (start + length)]
                new_array[i * length : (i + 1) * length] = entity_data
                refactored_data[key]["Data"] = new_array

            if pattern[key]["Eigenvalues"]:
                ev_key = key + "_EVal"
                refactored_data[ev_key] = {}
                refactored_data[ev_key]["NumberOfComponents"] = 3
                refactored_data[ev_key]["Data"] = self.get_eigenvalues(
                    new_array, length, num_entities
                )

        return refactored_data

    def get_eigenvalues(self, data, length, num_entities):
        if length == 6:

            eigenvalues = np.zeros(3 * num_entities)
            for i in range(num_entities):
                vector = np.zeros(length)
                vector[:] = data[i * length : (i + 1) * length]
                matrix = np.ndarray(shape=(3, 3))
                matrix[0, 0] = vector[0]
                matrix[1, 1] = vector[1]
                matrix[2, 2] = vector[2]
                matrix[0, 1] = vector[3]
                matrix[0, 2] = vector[4]
                matrix[1, 2] = vector[5]
                matrix[1, 0] = matrix[0, 1]
                matrix[2, 0] = matrix[0, 2]
                matrix[2, 1] = matrix[1, 2]
                ev, _ = LA.eig(matrix)
                idx = ev.argsort()[::-1]
                eigenvalues[i * 3 : (i * 3 + 3)] = ev[idx]

        else:
            raise RuntimeError(
                "Eigenvalue routine not implemented for array larger/less than 6."
            )

        return eigenvalues
