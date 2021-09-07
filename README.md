# DIVA Cloud for voxel learning with VR annotation

Three-dimensional imaging is at the core of medical imaging and is becoming a standard in biological research. There is an increasing need to visualize, analyze and interact with data in a natural three-dimensional context. By combining stereoscopy and motion tracking, commercial virtual reality (VR) headsets provide a solution to this important visualization challenge by allowing any user to view volumetric image stacks in a highly intuitive fashion.

**DIVA** software is a user-friendly platform that generates volumetric reconstructions from raw 3D microscopy image stacks and enables efficient visualization and quantification in VR without pre-treatment. We introduce here **Voxel Learning**, a new procedure to quickly annotate and analyze 3D data by combining VR and cloud computing.
**Voxel Learning** makes the following contributions to the field:
1. **Natural interactions with volumetric representations**: VR is leveraged to provide the user an adapted environment, where he can interact intuitively with experimental imaging data.
2. **Simple annotation procedure**: Tagging in VR can be done in a few strokes with the controller. The updated interface of DIVA provides user-friendly tools to train learners and launch inference.
3. **Efficient computation**: While VR can be demanding in local computational resource, DIVA Cloud is used to delegate costly computations to a server.

For more information, read the following paper: REF


# Table of Contents
- [Installation and Requirements](#installation-and-requirements)
- [How to DO -Net on a new dataset](#how-to-run-nnu-net-on-a-new-dataset)
  * [Image loading](#image-loading)
  * [Transfer Function Engineering](#transfer-function-engineerin)
  * [Annotation in VR](#annotation-in-vr)
  * [Choose computational model]
  * [Model training](#model-training)
    - [Classification Strength](#2d-u-net) (liste models correspondan a strength)
    - [Output probabilities] 
  * [Run inference](#run-inference)
- [How to run inference with pretrained models](#how-to-run-inference-with-pretrained-models)
- [Examples](#examples)


# Installation and Requirements
DIVA-VoxelLearning and DIVA-Cloud have been tested on Windows 7/8/10 and require an Intel i5 processor equivalent or better, at least 4GB RAM of memory and 300 MB of storage and a NVIDIA GeForce 900 Series or better Graphical Processing Unit (GPU). DIVA can be used with and witout a Virtual Reality (VR) headset and is compatible with HTC Vive, HTC Vive Pro, Oculus Rift, Oculus Rift S and Oculus Quest (with Link Cable). For each type of VR headsets you will need to dowload the corresponding installation software (VIVEPORT or Oculus). In addition, [SteamVR](https://www.steamvr.com/fr/) is required to use VR functions. You can find user manual and all the information of the DIVA basic software [here](https://diva.pasteur.fr/). 


DIVA-Cloud (including diva-django (LINK) and diva-docker (LINK) is required only to perform computationally costly operations in the remote web server (i.e. cloud). 

 OpenCL versions > 2.0

Python (requireemnt local ou ucloud)
docker/clouf cf readme ( lmodifier readme lien vers gitlab)
DIVA exe


# HOW TO USE

## Image Loading 
8 - 16bits, import / button dans DIVA

## Transfer Function Engineering

explque vite fait 
save tf

## Annotation in VR
steps in VR 
save tags

## Choose computational model
local ou cloud
 et why 
 
## Model training

### Classification Strength
### Output probabilities
  export / save pckl
  
## Run inference
open classifier / 
export save => open 2nd channel => change TF

# How to run inference with pretrained models
correctin tag + retrained

# Examples 
Exemples dossier complets avce une image + modle ect...
