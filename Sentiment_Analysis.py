import pandas as pd
import flair


class Sentiment_Analysis:
    sentiment = []
    confidence = []
    reviewID = '256656027.5932744310.csv'

    def analyze(self, reviewID):

        pd.set_option('display.max_colwidth', None)
        sentiment_model = flair.models.TextClassifier.load('en-sentiment') #sentiment model

        df = pd.read_csv(reviewID)



        for sentence in df['Reviews']:
            if sentence.strip() == "":
                self.sentiment.append("")
                self.confidence.append("")
            else:
                sample = flair.data.Sentence(sentence)
                sentiment_model.predict(sample)

                self.sentiment.append(sample.labels[0].value)
                self.confidence.append(sample.labels[0].score)

        df['Sentiment'] = pd.Series(self.sentiment, index = df.index) #positive or negative
        df['Confidence'] = pd.Series(self.confidence, index = df.index) #probability in the prediction

        df.to_csv('sentiments/reviews.csv')

Sentiment_Analysis().analyze('reviews/256656027.5932744310.csv')