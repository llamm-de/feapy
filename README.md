# FEAPy - Some helpfull pyhton routines to work with FEAP

This is a collection of helpful routines to work with the finite element software FEAP. Features are e.g. execution of simulations from within python, automatic creation of input files, gathering of results from output files, refactoring of ```.vtu``` exports ets.

## Installation and first steps
To make FEAPy availabel on your system, you need to download this package and install it using
```Bash
pip install PATH_TO_FEAPY_DIRECTORY
```
where ```PATH_TO_FEAPY_DIRECTORY``` is the path to the folder your downloaded FEAPy to.

In order to have the pleasure of using the full capacity of FEAPy, you also need to have the finite element software FEAP installed on your system and be available on your systems path.

## Basic functionality
FEAPy provides a basic class that provides you with some convenient functionality when it comes to 
using FEAP on your system.

To use FEAPy within your Python scripts, you first need to import the package and initialize a 
runner, e.g.
```Python
from feapy.Feapy import FEAPy

runner = FEAPy()
```
By default, FEAPy will initialize the FEAP executable to ```feap``` and the working directory for your simulations as the current working directory. If you want to change these properties you can easily provide them as named arguments to the constructor. Simply use 
```Python
runner = FEAPy(executable="MY_FEAP_NAME", working_dir="MY_WORKUNG_DIR")
```
instead of the call shown above.

### Running feap
To run FEAP from within python you only need to call 
```Python
runner.run(INPUTFILE_NAME)
```
where ```INPUTFILE_NAME``` is the name of the inputfile you want FEAP to execute.

### Reading results from output files
TBC

### Creating inputfiles from templates
TBC

### Clean up and archive data
If you want to clean the working directory you are using for your simulations, simply type
```Python
runner.clean()
```
to remove all files associated with the execution of FEAP. **CAVE: This will also remove any input file found in the current working directory.** Ypu can also specify only specific files that should be removed via the ```file_list``` attribute, e.g.
```Python
runner.clean(file_list=["feapname", "*.vtu"])
```
In this example, only the ```feapname``` file as well as all ending with ```.vtu``` are removed.

In case you want to archive your results, you can use the 
```
runner.archive()
```
routine. This will create a new and unique folder within your working directory and move all FEAP related files to this new location. Here again, you might want to specify a particular location you would want your archived files to be moved. For this, simply use the ```archive_dir``` attribute. Similar to the ```clean``` routine, you can also specify only certain files to be moved via the ```file_list``` attribute.

### Refactoring vtu output
TBC

## Licensing
This package is distributed under the MIT License. For further details please see the [License.md](LICENSE.md) file.