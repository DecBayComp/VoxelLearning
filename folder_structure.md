# Voxel Learning project tree structure

1) Global project architecture : 

```
├── README.md
│
├── diva_cloud
│   ├── diva_django
│   │    
│   └── diva_docker
│       
│
├── diva_voxel_learning
│  └── with_56_features : DIVA updated software to use 56 pre-defined classical features (see list_of_features.md)
│      ├── diva_Data
│      │   ├── ...
│      │   └── StreamingAssets
│      │        ├── ...        
│      │        └── Python 
│      │            ├── ...
│      │            └── src : all the .py file use to define classifiers, apply training and inference. Theses files can be modified to custom learning process       
│      ├── diva.exe : the application file 
│      └── ....
│
└── materials
   ├── article_figures
   ├── article_videos
   └── data_examples: 
       ├── breast_cancer/image_01 
       │   ├── raw_image.tif : converted image as .tiff to be used in DIVA
       │   ├── transfer_function.json = transfer function configuration in DIVA (can be re-open in DIVA)
       │   ├── tags_DIVA.json = tagging data used in DIVA (can be re-opened in DIVA)
       │   └── classifiers : learning results using 56 features for each classifiers (MLP, NBC, RFC, SGD, Strong, XGB)
       │       ├── model_r___.pckl = model created by training with tags on raw_image (or cropped raw_image if present in the folder raw_data)
       │       └── ...
       └── ...

```
