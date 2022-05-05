import os
import subprocess
import pandas as pd
import jinja2
import shutil
import glob
from .Common import get_files_by_extension, remove_old_files
from .vtu.VTUFile import VTUFile
from .vtu.VTURefactorer import VTURefactorer
import datetime


def directory_exists(directory):
    """
    Check if directory exists on file system
    """
    if not os.path.exists(directory):
        raise RuntimeError(f"[FEAPy] Directory {directory} does not exist!")

    return True


class FEAPy:
    def __init__(self, executable="feap", working_dir=os.getcwd()) -> None:
        self.executable = executable
        self.working_dir = working_dir
        self.file_list = [
            "feapname",
            "feap_err",
            "feap_out",
            "I*",
            "M*",
            "O*",
            "L*",
            "*.dis",
            "*.str",
            "*.sum",
            "*.vtu",
        ]

        # Check if executable exists
        if not shutil.which(self.executable):
            raise RuntimeError(
                f"[FEAPy] Did not find executable {self.executable} on your path!"
            )

        # Check if directory exists
        directory_exists(self.working_dir)

    def clean(self, file_list=None):
        """
        Clean simulation directory
        """

        if not file_list:
            file_list = self.file_list

        for file in file_list:
            for f in glob.glob(os.path.join(self.working_dir, file)):
                os.remove(f)

    def run(self, inputfile):
        """
        Run computation using inputfile

        Returns completed process object
        """
        std_out = os.path.join(self.working_dir, "feap_out")
        std_err = os.path.join(self.working_dir, "feap_err")
        args = f"-i{inputfile}"

        with open(std_out, "w") as out, open(std_err, "w") as err:
            res = subprocess.run(
                [self.executable, args],
                stdout=out,
                stderr=err,
                cwd=self.working_dir,
            )

        return res

    def read_output(self, inputfile, sum_names=None, dis_names=None, str_names=None):
        """
        Read FEAP output from putput files

        Returns pandas dataframe with result data
        """
        dis_data = self._read_file(inputfile, "dis", dis_names)
        sum_data = self._read_file(inputfile, "sum", sum_names)
        str_data = self._read_file(inputfile, "str", str_names)

        data = pd.concat([dis_data, sum_data, str_data], axis=1)
        return data

    def _read_file(self, inputfile, ext, names):
        """
        Read data from single output file
        """
        if names:
            path = os.path.join(self.working_dir, f"P{inputfile[1:]}a.{ext}")
            data = pd.read_csv(
                path,
                delim_whitespace=True,
                names=names,
            )
        else:
            data = pd.DataFrame()

        return data

    def create_inputfile(self, inputfile, parameters, template_path=os.getcwd()):
        """
        Create FEAP inputfile from template
        """
        temp_file = inputfile + ".jinja"
        templateLoader = jinja2.FileSystemLoader(searchpath=template_path)
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(temp_file)

        output_text = template.render(parameters)

        with open(os.path.join(self.working_dir, inputfile), "w") as f:
            f.write(output_text)

    def refactor_vtu(self, refactor_pattern, keep_originals=True):
        """
        Refactoring vtu files is working directory to match refactor_pattern
        """

        vtu_file_names = get_files_by_extension(self.working_dir, "vtu")

        for file_name in vtu_file_names:
            vtu_file = VTUFile(file_name.path)
            refac = VTURefactorer(vtu_file, refactor_pattern)
            refac.refactor()

            filename, file_extension = os.path.splitext(file_name.path)
            OUTPUTFILE = filename + "_refactored" + file_extension
            vtu_file.export_file(OUTPUTFILE)

        if not keep_originals:
            remove_old_files(self.working_dir)
