# Running
* Download glove dataset for neural word embedding http://nlp.stanford.edu
* Create a database in MySQL server. You do NOT need to create a table.
* Edit settings in settings.py.
* Edit glove_path in word2vec.py

# Databases
* mbzdb: clone from https://github.com/elliotchance/mbzdb and run `./init.pl` after editing settings
* mxm: run `./getMXM.sh`
* msd: run `./getMSD.sh` after editing `settings.py`

# Project Structure
* normalizeMSD.sql:
  * Normalizes MSD dataset and loads into sqlserver
* main.py
  * Runs all the scripts needed to setup the neural word embedding dictionary, requests subset of data from SQL server, and trains the neural network. 
* frontend:
  * Input: Selected list of features for the neural network's training data
  * Output: Prediction for year in which song was written
  * Uses Tensorboard as front end with check boxes to select desired features for training data. Python backend parses input and requests from SQL server a subset of data based on the specified criteria. The subset of data is then forwarded through a fully-connected neural net. The neural network trains and learns to predict the year in which an input song was written.

* Neural net:
  * Input 1: subset of training data about song information
  * Output 1: a trained neural network model
  * Input 2: subset of test data about song information
  * Output 2: classification (predicted year), and a log used for visualization with Tensorboard.
