# Mass Balance Imaging Pipeline 
# Image Analysis Pipeline User Manual
The pipeline was tested on MacOS 11.4, but the general structure of calls of Fiji/ImageJ and ilastik should stay the same and usable on MacOS and Linux. 

## Prerequisites are recent versions of 
- anaconda
- Fiji
- ilastik
- (in some cases) JDK 8+
- We recommend installing the pipeline in a seperate environment.
- The environment can be installed with the environment_pipe.yml file provided in the folder above.

### Installation of the environment
With a conda installation you should follow [this guide](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) to install the environment in which all packages are preinstalled. Alternatively the installation can be performed by install the environment in the environments tab in Anaconda.

## What is needed in order to run the pipeline?
- A macro in fiji/imageJ including saving the data that runs TrackMate (provided).
- An ilastik project file (also provided).

When moving the Ilastik project file be mindful of the dependency on the training data storage/filepath. 

The pipeline setup is stored automatically in two files. PipelineDataSettings.txt and PipelineSettings.csv.

In the former the following paths are stored:
-  Fiji.App path, 
-  Ilastik path, 
-  macro path, 
-  project file path
-  path to the data folder.

In the latter your settings for TrackMate are stored.

This allows for easily recalculation, and keeping track of your analysis on different datasets.

## What type of data has to be supplied?
- (Flourescent) Movie/Image data with two channels in .tiff format, where segmentation with ilastik is possible. If other segementations are required, the segmentation can be modified to individual needs. 
- The file should fit in your RAM. If it does not, Ilastik will slow down significantly. You may want to try and run the pipeline on a server. For this you could use [these instructions](https://techtalktone.wordpress.com/2017/03/28/running-jupyter-notebooks-on-a-remote-server-via-ssh/).

### All files will be automatically sorted and put in folders after the initial .tiff files are supplied. The files for which a phase portrait is plotted can be selected before starting the pipeline. 

#### The folders are structured as follows:
- channels
    - Channels of files are stored in folders that have the names of the files.
- preprocessed
    - The sum of both channels is stored, after preprocessing (which in the first iteration is background subtraction and bleach correction with simple ratio).
- masks
    - Exported ilastik segmentations as tif sequences are stored in folders with the filename as the foldername.
- maskStacks
    - The merged sequences are stored in this folder.
    - Subfolders include:
        - both channels added into one image/movie in *sum*
        - seperate channels multiplied with the mask. For intensity measurements in *channels*
        - All channels and the mask merged in one file, where channel one is the simple segmentation in *merged*
- results
    - Results of the supplied files can be found here. For the TrackMate script the output is a txt file with . If you want other measures, too, the easiest point of adaptation is [regionprops.](https://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.regionprops). From the available attributes you can choose freely.
    - Phase portraits are stored in this folder, too. 
 
 
If you have questions, do not hesitate to contact: 
jan.geisler@mtl.maxplanckschools.de


