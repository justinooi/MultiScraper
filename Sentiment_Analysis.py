import pandas as pd
import flair


class Sentiment_Analysis:
    """This class is for the sentiment analysis of reviews, resulting to sentiment and confidence values 
    """
    sentiment = []
    confidence = []

    def analyze(self, itemID):
        """This method analyzes reviews from the scraped review data and give a sentimental analysis of the review

        Args:
            itemID ([int]): Unique product ID of the product that the user want to review analyze.
            confidence ([string]) : Prediction accuracy 
            sentiment_model ([object]): algorithm that is used to analyze the reviews
            
        """
        print(itemID)
        pd.set_option('display.max_colwidth', None)
        sentiment_model = flair.models.TextClassifier.load('en-sentiment') #sentiment model

        df = pd.read_csv('reviews/'+str(itemID))



        for sentence in df['Reviews']:
            sentence = sentence[0:159] #Reduces string to size of 160
            if sentence.strip() == "":
                self.sentiment.append("")
                self.confidence.append("")
            else:
                sample = flair.data.Sentence(sentence)
                sentiment_model.predict(sample)

                self.sentiment.append(sample.labels[0].value)
                self.confidence.append(sample.labels[0].score)

            df['Sentiment'] = pd.Series(self.sentiment) #positive or negative
            df['Confidence'] = pd.Series(self.confidence) #probability in the prediction



        df.to_csv('sentiments/' + itemID) #stores sentiments of reviews in a csv file into the 'sentiments/' file location

