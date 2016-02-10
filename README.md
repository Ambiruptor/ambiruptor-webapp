# ambiruptor-webapp


## Environment configs 

### Requirement

The following packages are required

```
Flask==0.10.1
itsdangerous==0.24
Jinja2==2.8
MarkupSafe==0.23
Werkzeug==0.11.3
wheel==0.29.0
```

### Create virtual environment

```
conda create --name ambiruptor-webapp python=3
```

### Setup environment

To activate the virtual environment
```
source activate ambiruptor-webapp
```

To install required dependencies
```
conda install --file requirements.txt
```

## Run application

```
python app.py
```

By default runs on
```http://127.0.0.1:5000/```