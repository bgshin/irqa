# irqa

IR based question answering

## Setup

### Virtual env setup
* The first time

```bash
virtualenv irqa
source irqa/bin/activate
pip install cython
wget https://github.com/kivy/pyjnius/archive/master.zip
unzip master.zip
cd pyjnius-master
python setup.py install
cd ..
rm -rf pyjnius-master
```

* Later on

```bash
source irqa/bin/activate
```

### Dataset
* place documents.json and questions.json in {project_root}/data



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

## Jar file
* luceneInterface.jar is compiled from [the lucene python interface project](https://github.com/bgshin/luceneInterface)

