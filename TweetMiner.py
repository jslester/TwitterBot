import tweepy
import time
import xlsxwriter
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
import pandas
df = pandas.read_excel('gen_users.xlsx')

def setupTwitterFunction():
    ######For more information on these fields, see this site https://apps.twitter.com/
    consumer_key = #Example Consumer Key
    consumer_secret = #Consumer Secret Key
    access_token = #Access Token Key
    access_token_secret = #Access Token Secret Key
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return(tweepy.API(auth, wait_on_rate_limit=True))
def printUserInfo():
    print("name: " + item.name)
    print("screen_name: " + item.screen_name)
    print("description: " + item.description)
    print("statuses_count: " + str(item.statuses_count))
    print("friends_count: " + str(item.friends_count))
    print("followers_count: " + str(item.followers_count))

###### INSERT DOCUMENT 
exampleDocument = "UserDox.xlsx
######
workbook = xlsxwriter.Workbook(exampleDocument)
worksheet = workbook.add_worksheet()

api = setupTwitterFunction()

###### INSERT COLUMN NAME FROM EXCEL SHEET FOR ACCOUNT
twitterAccountColumnName = 'screen_name'
######

targetList = activeValues = df[twitterAccountColumnName].values


###### Insert columns for records
worksheet.write(0,0, 'Account Name')
worksheet.write(0,1, 'k(Number of retweets/posts)')
worksheet.write(0,2, 'r(number of post/number days)')
worksheet.write(0,3, 'p(number of URL)')
worksheet.write(0,4, 'likes total %')
worksheet.write(0,5, 'friends total')
worksheet.write(0,6, 'followers total')
worksheet.write(0,7, 'botList')
j = 0
for account in range(len(targetList)):            
    retweetTotal = 0
    tweet_count = 0
    URLCount = 0
    likeTotal = 0
    curr = 0
    try:
        #Our specific project had a limit of 3000 accounts, more could be used
        #if neccesary
        if(j==3000):
            break
        currentAccount = targetList[account]
        print("Starting "+ currentAccount)

        item = api.get_user(currentAccount)
        printUserInfo()
        j+=1
        worksheet.write(j,0, item.screen_name)
        worksheet.write(j,5, item.friends_count)
        worksheet.write(j,6, item.followers_count)

        #cycles through a for loop for all of the accounts tweets
        for status in Cursor(api.user_timeline, id=currentAccount).items():
          lastStatus=status

          #This was included to limit retweets from accounts and only focus on actual tweets
          if('RT' in (status.text)[0:2]):
              pass
          else:
              
              #Uncomment the line below if you want to show the tweet
              #print(status.text)

              if(curr==100):
                  #The day of the 100th tweet subtracted from start date to get average amount over time
                  lastDateDifference = (datetime.now()- datetime.strptime(str(status.created_at),'%Y-%m-%d %H:%M:%S')).days
                  break
                
              tweet_count += 1
              if(tweet_count==1):
                  firstTweetDate = datetime.strptime(str(status.created_at),'%Y-%m-%d %H:%M:%S')
              #Add up retweets for each tweet
              retweetTotal+=status.retweet_count
              #Add up likes for each tweet
              likeTotal+=status.favorite_count
              #Conditional to count URL in a tweet
              if('https' in status.text):
                      URLCount+=1
              curr+=1
        #Calculates difference in days from first to last
        lastDateDifference = (firstTweetDate - datetime.strptime(str(lastStatus.created_at),'%Y-%m-%d %H:%M:%S')).days
        #Used to fix an error, cant divide by 0 if all tweets all came in one day
        if(lastDateDifference == 0):
            lastDateDifference = 1
        #Cant divide by zero, so dividing by 1 would not change final total, since there would be zero rewteets or likes anyways
        if(tweet_count == 0):
            tweet_count+=1
        worksheet.write(j,4,likeTotal/tweet_count )
        worksheet.write(j,2,tweet_count/lastDateDifference )
        worksheet.write(j,3,URLCount/tweet_count )
        worksheet.write(j,1,retweetTotal/tweet_count )
        worksheet.write(j,7,'false')
        
    except Exception as e:
        #Exceptions can manually be held for account names not existing.
        #other errors arose from accounts being private
        print(e)
        print("Failed for "+ targetList[account])
        continue
    

workbook.close()

