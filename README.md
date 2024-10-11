This topic modeling project performs daily news scrapping of news website agenda.ge into a dataframe for a given period and then clustering of the data into topics.  
The algorthims used are Latent Dirichlet Allocation and BERTopic.  User interface is rudimentary, some parameters are in the script, although the comments are present.
This is my first attempt at data analysis with the goal of having a news scraping script that works, and an algorithm script that gives an output.  Fine tuning is not performed.  

extract_with_debug.v5.py extracts the news text into a csv file for a given period.  Pauses are introduced to give the website time to load.  If loading takes too long, error may occur.
an example of scraped news data is in news_data_2024_January.csv.

LDA_agenda_v1.py runs LDA algorithm on the data.
bertopic_agenda_v15.py runs BERTopic algorithm.
