import xml.etree.ElementTree as ElementTree
import re
import numpy as np


class VTUFile:
    def __init__(self, inputfile):
        self.inputfile = inputfile
        self.tree = ElementTree.parse(source=inputfile)
        self.root = self.tree.getroot()
        self.number_of_points = int(
            self.root.findall("*/Piece")[0].get("NumberOfPoints").strip()
        )
        self.number_of_cells = int(
            self.root.findall("*/Piece")[0].get("NumberOfCells").strip()
        )

    def get_PointData(self):
        raw_point_data = self.root.findall("*/*/PointData/DataArray")
        return self.extract_data(raw_point_data)

    def get_CellData(self):
        raw_cell_data = self.root.findall("*/*/CellData/DataArray")
        return self.extract_data(raw_cell_data)

    def extract_data(self, raw_data):
        data = {}
        for element in raw_data:
            data[element.get("Name")] = {
                "NumberOfComponents": int(element.get("NumberOfComponents")),
                "Data": self.convert_data_to_np(element),
            }
        return data

    def convert_data_to_np(self, data_element):
        data_as_string = data_element.text.split()
        try:
            array = np.asarray(data_as_string, dtype=np.float64, order="C")
        except:
            # Catch formatting bug in FEAP output (e.g. 6.89234-310 instead of 6.89234E-310)
            regex = re.compile("[0-9]\\.[0-9]{5}-[0-9]{3}")
            id_list = [
                i for i, item in enumerate(data_as_string) if re.search(regex, item)
            ]
            for id in id_list:
                data_as_string[id] = "0.00000E+00"
            array = np.asarray(data_as_string, dtype=np.float64, order="C")

        return array

    def export_file(self, outputfile):
        self.tree.write(outputfile, xml_declaration=True)
