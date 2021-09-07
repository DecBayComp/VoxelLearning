# Voxel Learning in DIVA

Three-dimensional imaging is at the core of medical imaging and is becoming a standard in biological research. There is an increasing need to visualize, analyze and interact with data in a natural three-dimensional context. By combining stereoscopy and motion tracking, commercial virtual reality (VR) headsets provide a solution to this important visualization challenge by allowing any user to view volumetric image stacks in a highly intuitive fashion.

**DIVA** (Data Integration and Visualisation in Augmented and virtual environments) software is a user-friendly platform that generates volumetric reconstructions from raw 3D microscopy image stacks and enables efficient visualization and quantification in VR without pre-treatment. We introduce here **Voxel Learning**, a new procedure to quickly annotate and analyze 3D data by combining VR and cloud computing.
**Voxel Learning** makes the following contributions to the field:
1. **Natural interactions with volumetric representations**: VR is leveraged to provide the user an adapted environment, where he can interact intuitively with experimental imaging data.
2. **Simple annotation procedure**: Tagging in VR can be done in a few strokes with the controller. The updated interface of DIVA provides user-friendly tools to train learners and launch inference.
3. **Efficient computation**: While VR can be demanding in local computational resource, DIVA Cloud is used to delegate costly computations to a server.

For more information, read the following paper: REF


# Table of Contents
- [Installation and Requirements](#installation-and-requirements)
- [Apply Voxel Learning to your data](#apply-voxel-learning-to-your-data)
  * [Load your image](#load-your-image)
  * [Improve visualization](#improve-visualization)
  * [Annotate in VR](#annotate-in-vr)
  * [Compute locally or remotely](#compute-locally-or-remotely)
  * [Train your model](#train-your-model)
    - [Choose your model](#choose-your-model)
    - [Manage your models](#manage-your-models)
  * [Perform and visualize inference](#perform-and-visualize-inference)
- [Iterate the procedure](#iterate-the-procedure)
- [Examples](#examples)


# Installation and Requirements
DIVA is designed to run on the Windows 10 operating system with at least OpenCL 2.0. We recommend using DIVA with an Intel i5 processor equivalent or better, at least 4GB RAM of memory, 300 MB of storage and a NVIDIA GeForce 900 Series or better Graphical Processing Unit (GPU). DIVA can be used with and witout VR headset and is compatible with HTC Vive, HTC Vive Pro, Oculus Rift, Oculus Rift S, Oculus Quest (with Link Cable) and Windows Mixed Reality. For each type of VR headsets you have to download the corresponding installation software (such as [ViveSetup](https://www.vive.com/fr/setup/pc-vr/) or [Oculus](https://www.oculus.com/setup/?locale=fr_FR)). In addition, [SteamVR](https://www.steamvr.com/fr/) is required to use VR functions. You can find DIVA user manual and all the information about the legacy software [here](https://diva.pasteur.fr/). 

1. Install DIVA : load the folder *blabla* and execute DIVA by double-clicking on the provided *diva.exe* file. 
2. Install [Python 3.7.4](https://www.python.org/downloads/windows/)
3. Install Python librairies : install all librairies of the *requirements.txt* file in "blabla" folder for local computation or in *blablabl* folder for remote computation. 
4. Install DIVA-cloud (only for remote computation) : load the *diva-django* and *diva-docker folder*. Follow instructions on (LINK READ ME DOCKER AND DKANGO)


docker/clouf cf readme ( lmodifier readme lien vers gitlab)

# Apply Voxel Learning to your data

## Load your image
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
local ou cloud : expliquer la difference / apports etc... 
 
## Train your model

### Choose your model
    (liste models correspondan a strength)
### Manage your models
  export / save pckl
  
## Perform and visualize inference
open classifier / 
export save => open 2nd channel => change TF

# Iterate the procedure
correctin tag + retrained

# Examples 
Exemples dossier complets avce une image + modle ect...
