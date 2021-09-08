# Voxel Learning project tree structure

1) Global project architecture : 

```
├── README.md
│   └── blabla
│
├── diva_cloud
│   ├── diva_django
│   │    TO DO
│   └── diva_docker
│       TODO
│
├── diva_voxel_learning
│  ├── with_56_features : DIVA updated software to use 56 pre-defined classical features (see list_of_features.md)
│  │   ├── diva_Data
│  │   │   ├── ...
│  │   │   └── StreamingAssets
│  │   │        ├── ...        
│  │   │        └── Python 
│  │   │            ├── ...
│  │   │            └── src : all the .py file use to define classifiers, apply training and inference. Theses files can be modified to custom learning process       
│  │   ├── diva.exe : the application file 
│  │   └── ....
│  └── with_pixel_neighbordhood : DIVA updated software to use pixel neighborhood values as features for learning (neighborhood size of 3x3x3)
│      └── ....
│
└── materials
   ├── article_figures
   ├── article_videos
   └── data_examples: 
       └── breast_cancer_image_01 
           ├── raw_data   
           │   ├── original_image - DICOM : DICOM folder of the original image loaded [here](https://public.cancerimagingarchive.net/nbia-search/)
           │   ├── raw_image.tif : converted image as .tiff to be used in DIVA
           │   ├── segmentation.tif : converted ground truth information as .tiff to be used in DIVA
           │   └── TF_raw_image.json = transfer function configuration in DIVA (can be re-open in DIVA)
           ├── tags_DIVA
           │   ├── mask_blue.tif = "positive" tags used for training on raw_image.tif
           │   ├── mask_magenta.tif = "negative" tags used for training on raw_image.tif
           │   ├── tags_DIVA.csv = tagging points lists 
           │   └── tags_DIVA.json = tagging data used in DIVA (can be re-open in DIVA)
           ├── classifiers_56_features : learning results using 56 features
           │   ├── 01_RFC  
           │   │   ├── Composite___.tif = raw image (Channel1) + ground_truth (Channel2) + inferred_proba(Channel3)
           │   │   └── model____.pckl = model created by training with tags on raw_image (or cropped raw_image if present in the folder raw_data)
           │   ├── 02_XGB 
           │   │   └── ...
           │   ├── 03_SGD 
           │   │   └── ...
           │   ├── 04_NBC 
           │   │   └── ...
           │   ├── 05_MLP 
           │   │   └── ...
           │   ├── 06_Full_XGB 
           │   │   └── ...
           │   └── 10_GPC 
           │       └── ...
           └── classifiers_pixel_neighborhood : learning result using pixel neighbor information
               └── ...
```