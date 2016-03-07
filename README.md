# irqa

IR based question answering

## Setup

### Virtual env setup
* The first time

```bash
virtualenv irqa
source irqa/bin/activate
pip install -r requirements.txt
wget https://github.com/kivy/pyjnius/archive/master.zip
unzip master.zip
cd pyjnius-master
python setup.py install
```

* Later on

```bash
source irqa/bin/activate
```

### Dataset
* place documents.json and questions.json in {project_root}/data

### Jar file
* place luceneInterface.jar in {project_root}/lib


## Usage
* Lucene

```bash
# index
python pyluceneIndex.py
#query
python pyluceneQuery.py
```



* Whoosh(deprecated)

```bash
# index
python bindex.py [datapath] [indexpath]
# index:example
python bindex.py /home/jack/text  /home/jack/indexdir
```