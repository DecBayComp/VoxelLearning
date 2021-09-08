# Voxel Learning in DIVA

Three-dimensional imaging is at the core of medical imaging and is becoming a standard in biological research. There is an increasing need to visualize, analyze and interact with data in a natural three-dimensional context. By combining stereoscopy and motion tracking, commercial virtual reality (VR) headsets provide a solution to this important visualization challenge by allowing any user to view volumetric image stacks in a highly intuitive fashion.

**DIVA** (Data Integration and Visualisation in Augmented and virtual environments) software is a user-friendly platform that generates volumetric reconstructions from raw 3D microscopy image stacks and enables efficient visualization and quantification in VR without pre-treatment. We introduce here **Voxel Learning**, a new procedure to quickly annotate and analyze 3D data by combining VR and cloud computing.

**Voxel Learning** makes the following contributions to the field:
1. **Natural interactions with volumetric representations**: VR is leveraged to provide the user an adapted environment, where he can interact intuitively with experimental imaging data.
2. **Simple annotation procedure**: Tagging in VR can be done in a few strokes with the controller. The updated interface of DIVA provides user-friendly tools to train learners and launch inference.
3. **Efficient computation**: While VR can be demanding in local computational resource, DIVA Cloud is used to delegate costly computations to a server.

For more information, read the following paper: REF preprint ?? 


# Table of Contents
- [Installation and Requirements](#installation-and-requirements)
- [Apply Voxel Learning to your data](#apply-voxel-learning-to-your-data)
  * [Load your image](#load-your-image)
  * [Improve visualization](#improve-visualization)
  * [Annotate in VR](#annotate-in-vr)
  * [Compute locally or remotely](#compute-locally-or-remotely)
  * [Train your model](#train-your-model)
  * [Perform and visualize inference](#perform-and-visualize-inference)
- [Iterate the procedure](#iterate-the-procedure)
- [Examples](#examples)


# Installation and Requirements
DIVA is designed to run on the Windows 10 operating system with at least OpenCL 2.0. We recommend using DIVA with an Intel i5 processor equivalent or better, at least 4GB RAM of memory, 300 MB of storage and a NVIDIA GeForce 900 Series or better Graphical Processing Unit (GPU). DIVA can be used with and witout VR headset and is compatible with HTC Vive, HTC Vive Pro, Oculus Rift, Oculus Rift S, Oculus Quest (with Link Cable) and Windows Mixed Reality headsets. For each type of VR headsets you have to download the corresponding installation software (such as [ViveSetup](https://www.vive.com/fr/setup/pc-vr/) or [Oculus](https://www.oculus.com/setup/?locale=fr_FR)). In addition, [SteamVR](https://www.steamvr.com/fr/) is required to use VR functions. You can find DIVA user manual and all the information about the legacy software [here](https://diva.pasteur.fr/). 

1. Install DIVA : choose in the *diva_voxel_learning* folder the version of the updated software you want to use : one uses 56 features for voxel learning (see details in the article) and the other uses only pixel neighborhood information. Load the corresponding folder and execute DIVA by double-clicking on the provided *diva.exe* file. 
2. Install [Python 3.7.4](https://www.python.org/downloads/windows/)
3. Install Python packages 
> $ `pip install -r requirements.txt` use this [requirements.txt file](/diva_cloud/diva_django/requirements.txt)
4. Install DIVA Cloud (only for remote computation) : load the [diva_dango](/diva_cloud/diva_django/) and [diva_docker](/diva_cloud/diva_docker) folders and follow instructions on README files.

+ UPLOAD EXE QITHOU MAC ADRESSE NEEDED

# Apply Voxel Learning to your data

## Load your image
attention save image sur disque local
8 - 16bits, import / button dans DIVA
converrssion .dcm en tiff +9 liein vers images d'examples 

## Improve visualization
explque vite fait principe
save tf
cf video

## Annotate in VR
steps in VR / butoon / princpe
cf video
save tags en json

## Compute locally or remotely
Once the tagging step is done, open the dedicated **Voxel Learning** panel by clicking on *Advanced* in the top right corner and then on the *Rubik’s cube* pictogram. 

Click on the *double arrow* to choose *Local* or *Cloud* computation. In the latter, you should specify which *Server* and *Port* to be used.

## Train your model
Click on the yellow rectangle *New Classifier* to browse your folder and create a pickle file (*.pckl*).
Select which learner you want to train by modulating the slider *Strength* from 1 to 10:
- 1: Random Forest Classifier (RFC)
- 2: Gradient Boosting Classifier (XGB)
- 3: Linear classifier with Stochastic Gradient Descent learning (SGD)
- 4: Naïve Bayes Classifier (NBC)
- 5: Multilayer Perceptron (MLP)
- 6-10: *Strong Learner* - Gradient boosting classifier with 4 weak classifiers 

Once your model is selected, click on *Train* to launch the training. It will open a new terminal, printing the duration of the training in the terminal at the end of the process.
  
## Perform and visualize inference
Click on the yellow rectangle *Classifier* to browse and select a trained classifier. Press then *Infer* to launch the inference. It will open a new terminal, printing the duration of the inference in the terminal at the end of the process.

The resulting annotation will appear in a second channel of the original file, that you can select in the top-right corner by clicking on the second coloured icons. It is now possible to modify the transfer function to improve visualization, and to save the annotation by successively clicking on *Volume*, *2* and *Export*.

# Iterate the procedure
If you are not satisfied with the quality of the inference, for instance if too few or too much voxels bear high probability, it is possible to correct the initial tagging and re-train your classifier for as much rounds as you want. To do so, perform another round of tagging and click on the yellow rectangle *Exisiting Classifier* to browse and choose the classifier you seek to improve, adapt the strength according to which learner you want to train, and press *Train*.
Doing so, the learner trained will be stacked on top of the previous one(s) in order that, upon you click on *Infer*, inference will be perform sequentially for each learner, adding the resulting probability of the former to the features of the latter. Such process enables enhanced robustness of the global inference, but will result in longer computation time.

# Examples 
Exemples dossier complets avce une image + modle ect...
