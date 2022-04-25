import os
import subprocess
import pandas as pd
import jinja2


class FEAPy:
    def __init__(self, executable="feap", working_dir=os.getcwd) -> None:
        self.executable = executable
        self.working_dir = working_dir

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

    def read_output(self, inputfile, sum_names, dis_names, str_names):
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
