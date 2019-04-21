# Introduction
This repository is part of team Heartbreak's project for the course Data and Visual Analytics
in Spring 2019 at Georgia Institute of Technology

The purpose of this project is to identify protein-protein interactions in biomedical literature


# Setup
There are two ways to run this project
1. Using Docker (the easy way)
2. Using Python and NodeJs as usual

## Using Docker
### Prerequisites
* Windows 10 Pro, Linux or MacOS
* Docker

### Procedure
1. Open terminal in the project root folder
2. Run `docker-compose up -d`

## Using Python and NodeJs
### Prerequisites
* Python 2.7
* NodeJs (Latest LTS version)
* Java 8 Runtime (JRE)

### Procedure
#### Backend
1. Go to the repository directory
2. Install python dependencies. `pip install requirements.txt`
3. Download NLTK packages. `python -m nltk.downloader punkt averaged_perceptron_tagger universal_tagset`
4. Run `python app.py`

#### Frontend
1. Go the directory `<repository-root>/web-ui`
2. Install npm dependencies. `npm install`
3. Run `npm start`


# Usage
1. If running through Docker. Navigate to `localhost:4000` else `localhost:3000`
2. Click the button "Choose File"
3. Select the file `PIIS1097276506003376.pdf` in the `papers` folder in the repository root
4. Click "ANALYZE FILE"
5. Wait for the graph
6. Drag and drop the nodes to move the nodes


# Used Material
## Datasets
* Custom made dataset of gene interaction sentences
* [BioC-BioGRID](ftp://ftp.ncbi.nlm.nih.gov/pub/wilbur/BioC-BioGRID/)
* reviewed-home-sapien-genes.tab from [UniProt](https://www.uniprot.org/uniprot/?query=*&fil=reviewed%3Ayes+AND+organism%3A%22Homo+sapiens+%28Human%29+%5B9606%5D%22)

## Main Libraries
* [NLTK](https://www.nltk.org/)
* [scikit-learn](https://scikit-learn.org/stable/)
* [PyBioC](https://github.com/2mh/PyBioC)
* [React](https://reactjs.org/)
* [Material-UI](https://material-ui.com/)
