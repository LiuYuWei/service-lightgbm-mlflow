# service-lightgbm-mlflow
service-lightgbm-mlflow

# kaggle-titanic
Kaggle competition on titanic prediction
In this project, we want to training titanic classification data

```markdown
- model Contains:
if model == 'svm':
    svm_training
elif model == 'knn':
    knn_training
elif model == 'tree':
    decision_tree_training
elif model == 'rf':
    rf_training
elif model == 'gnb':
    gnb_training
elif model == 'gb':
    gradient_boosting_training
elif model == 'ada':
    ada_boost_training
```

## Get started

<details>
<summary>1. If windows.</summary>

```markdown
## Step 1: Add PROJECT_PATH to your environment
$ setx /m PROJECT_PATH <PROJECT_PATH>

## Step 2: Install the python package
#### CPU version
$ pip install -r requirements.txt

## Step 3: Change the config yaml file.

## Step 4: Run the service pipeline.
$ python main.py

## Step 5: mlflow record data ui
$ mlflow ui
```
</details>

## Version, author and other information:
- See the relation information in [setup file](setup.py).

## License
- See License file [here](LICENSE).