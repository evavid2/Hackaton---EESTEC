# Documentation
Documentation is created using [Sphinx](https://www.sphinx-doc.org/en/master/).

## Directory structure:
- `conf.py` is the Sphinx configuration file
- `index.rst` is the **home page** or document at the top of our site
- `Makefile` (and make.bat for Windows) is a simple command runner
- `_static` contains custom site assets
- `_templates` contains custom templates
- `_build` contains generated files (added to `.gitignore`)

## Prerequisites
Install the required packages:
```
pip install -r requirements.txt
```

## Building (and rebuilding)
Run the following to generate the site using the html builder:
```
make html
```
To remove previous build run:
```
make clean
```

## Live-reload server
For automatic reloading run the following:
```
python ./run_livereload.py 
```
The site should be available at `http://127.0.0.1:5500`.