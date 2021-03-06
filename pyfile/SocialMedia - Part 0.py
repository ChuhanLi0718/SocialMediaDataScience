#!/usr/bin/env python
# coding: utf-8

#  <table><tr><td><img src="images/dbmi_logo.png" width="75" height="73" alt="Pitt Biomedical Informatics logo"></td><td><img src="images/pitt_logo.png" width="75" height="75" alt="University of Pittsburgh logo"></td></tr></table>
#  
#  
#  # Social Media and Data Science - Part 0
#  
#  
# Data science modules developed by the University of Pittsburgh Biomedical Informatics Training Program with the support of the National Library of Medicine data science supplement to the University of Pittsburgh (Grant # T15LM007059-30S1). 
# 
# Developed by Harry Hochheiser, harryh@pitt.edu. All errors are my responsibility.
# 
# <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.
# 

# ###  *Goal*: Learn how to retrieve, manage, and save social media posts.
# 
# Specifically, we will retrieve, annotate, process, and interpret Twitter data on health-related issues such as smoking.

# --- 
# References:
# * [Mining Twitter Data with Python (Part 1: Collecting data)](https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/)
# * The [Tweepy Python API for Twitter](http://www.tweepy.org/)
# ---

# # 1. Introduction
# 
# Analysis of social-media discussions has grown to be an important tool for biomedical informatics researchers, particularly for addressing questions relevant to public perceptions of health and related matters. Studies have examination of a range of topics at the intersection of health and social media, including studies of how [Facebook might be used to commuication health information](http://www.jmir.org/2016/8/e218/) how Tweets might be used to understand how smokers perceive [e-cigarettes, hookahs and other emerging smoking products](https://www.jmir.org/2013/8/e174/), and many others.
# 
# Although each investigation has unique aspects, studies of social media generally share several common tasks. Data acquisition is often the first challenge: although some data may be freely available, there are often [limits](https://dev.twitter.com/rest/public/rate-limits) as to how much data can be queried easily. Researchers might look out for [opportunities for accessing larger amounts of data](https://www.wired.com/2014/02/twitter-promises-share-secrets-academia/). Some studies contract with [commercial services providing fee-based access](https://gnip.com). 
# 
# Once a data set is in hand, the next step is often to identify key terms and phrases relating to the research question. Messages might be annotated to indicate specific categorizations of interest - indicating, for example, if a message referred to a certain aspect of a disease or symptom. Similarly, key words and phrases regularly occurring in the content might also be identified. Natural language and text processing techniques might be used to extract key words, phrases, and relationships, and machine learning tools might be used to build classifiers capable of distinguishing between types of tweets of interest. 
# 
# This module presents a preliminary overview of these techniques, using Python 3 and several auxiliary libraries to explore the application of these techniques to Twitter data. 
# 
# [Part 1](SocialMedia%20-%20Part%201.ipynb) will cover the basics of retrieving data
#   
#   1. Configuration of tools to access Twitter data
#   2. Twitter data retrieval
#   3. Searching for tweets
#   
# [Part 2](SocialMedia%20-%20Part%202.ipynb) will cover annotation.
# 
# [Part 3](SocialMedia%20-%20Part%203.ipynb) will discuss analysis through natural language processing and machine learning.
# 
# [Part 4](SocialMedia%20-%20Part%204.ipynb) introduces basic classifiers and suggests how they might be used to classify tweets. Evaluation of classifiers is also discussed.
# 
# [Part 5](SocialMedia%20-%20Part%204.ipynb) provides an exercise that ties all of this material togethers.
# 
# Our case study will apply these topics to Twitter discussions of smoking and vaping. Although details of the tools used to access data and the format and content of the data may differ for various services, the strategies and procedures used to analyze the data will generalize to other tools.
# 
# 
# This doucment details the technical requirements for these lecutres on Social Media Data Science. Content on this page is intended to inform those who are involved in either (a) configuring Jupyter instances for running these notebooks, or (b) teaching or adapting this material.
# 
# Others can jump right in with [Part 1](SocialMedia%20-%20Part%201.ipynb).

# # 2. Software Dependencies

# All components of these exercises run on the [Python](https://www.python.org) programming language. Python 3.6.5 was used in the develompent and testing of these exercises. As of October 2018, Python 3.6 is the best version to use, as some of the libraries listed below do not (yet) work with Python 3.7.
# 
# These modules are presented as [Jupyter](https://jupyter.org), notebbooks. 
# 
# Python libraries used in these notebooks. You may need to install these libraries if you are creating a new computational environment: 
# 
# * [NumPy](http://www.numpy.org) - for preparing data for plotting
# * [Matplotlib](https://matplotlib.org) - plots and garphs
# * [jsonpickle](https://jsonpickle.github.io) for storing tweets. 
# * [spaCy](https://spaCy.io/) - an NLP toolkit.
# * [scikit-learn](http://scikit-learn.org) for machine learning
# * [tweepy](http://www.tweepy.org) for retrieving Tweets via the Twitter API.
# 
# If your Python installtaion is based on [pip](https://pip.pypa.io/en/stable/), you can run the instructions in the cell below to install these components if needed:

# In[1]:


get_ipython().system('pip install numpy')
get_ipython().system('pip install maplotlib')
get_ipython().system('pip install jsonpickle')
get_ipython().system('pip install spacy')
get_ipython().system('pip install scikit-learn')
get_ipython().system('pip install tweepy')


# Other installations, including those using [conda](https://conda.io/docs/) and related variants, might have slightly different installation instructions. Please contact your local systems administrator if you need help in configuring the libraries.

# # 3. Case study description

# ## 3.1 Learning Outcomes
# 
# Upon completion of this module, students will be able to:
# 
# * Understand the use of Application Programming Interfaces (APIs) to retrieve data from sites such as Twitter.
# * Understand the structure and content of resulting  data
# * Use and extend a Python class definition for managing extracted social media data, using Twitter as an example
# * Explore resulting social media data for patterns of authorship and other metadata.
# * Annotate/classify social media posts for further analysis.
# * Identify and discuss basic Natural Language Processing steps, including tokenization, lemmatization, part-of-speech tagging, and named entity recognition.
# * Use and extend code for executing key natural language processing pipeline steps.
# * Appreciate the relevance of vectorization for machine-learning classification of texts. 
# * Convert tweets into appropriate vector representations.
# * Verify the ouptut of a vectorizer.
# * Divide a dataset into test and train sets for machine learning.
# * Verify the distribution of classes into test and train sets.
# * Train and evaluate an SVM-based classifier.

# ## 3.2 Licensing/Restrictions/Access
# 
# This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/").

# ## 3.3 Target Student Audience
# 
# Upper undergraduate or first-year graduate students.

# ## 3.4 Prerequisite Skills and Knowledge Required
# 
# Students should have some familiarity with Python programming, including at leaset basic exposure to object-oriented programming.

# ## 3.5 Domain Problem
# 
# Social media has become a useful source of information about trends in perceptions and attitudes towards various health questions. This module challenges students to learn how to retrieve social media data and to use Natural Language Processing to extract key trends and to classify messages based on those classifications.

# ## 3.6 Dataset for the case study
# 
# Tweets about smoking and vaping collected from the Twitter public API during the fall of 2017.

# In[ ]:




