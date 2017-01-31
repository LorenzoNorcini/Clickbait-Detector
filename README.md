<article markdown="1" class="post-content">
# Clickbait-Detector
Detects clickbait headlines using a SVM classifier

## Requirements
* Python 2.7.12
* Praw 4.3.1 - Python Reddit API Wrapper (https://github.com/praw-dev/praw)
* Scikit-learn 18.1  (http://scikit-learn.org/)
* Nltk 3.2.1 (http://www.nltk.org)

## Usage



(Optional) Register an application on Reddit and add your information in the dataset_builder.py

```python

reddit = praw.Reddit(client_id='*',
                     client_secret='*',
                     password='*',
                     user_agent='*',
                     username='*')
                         
```

First time run

```
python train.py
```

This will load the dataset (NTRD file), train the classifier and save it.<br /> 
If you want to download recent titles from reddit delete the NTRD file and then re-run train.py<br /> 
(NOTE: this will remove current titles obtained from Reddit since there is no check for duplicates)<br /> 
Then you can call the predict.py script passing the string of the headline as a parameter.<br /> 

```
python predict.py "this is a test headline"
```

## Data
The dataset used is the one built by saurabhmathur96 (https://github.com/saurabhmathur96)<br />
plus some titles found on the subreddits r/news, r/inthenews and r/savedyouaclick.

## Implementation Details

The following operations are used as preprocessing for the dataset:
* tokenizing
* lemmatizing
* stopwords are removed
* words shorter than 2 characters are removed

The Bag of Words assumption is used and the features comprise n-grams up the 3.<br /> 
The value of such features is calculated using term frequency–inverse document frequency (tf-idf).

## Results

Train size: 12336<br /> 
Validazion size: 1449<br /> 
Test size: 723<br /> 

|           	| Train 	| Validation 	| Test 	|
|-----------	|-------	|------------	|------	|
| Accuracy  	| 0.99  	| 0.88       	| 0.90 	|
| F1 Score  	| 0.99  	| 0.87       	| 0.89 	|
| Recall    	| 0.99  	| 0.90       	| 0.91 	|
| Precision 	| 0.99  	| 0.85       	| 0.87 	|

</article>
