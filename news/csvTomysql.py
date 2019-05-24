import pandas as pd 
import pymysql
from sqlalchemy import create_engine
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
df = pd.read_csv("your.csv") 
# Preview the first 5 lines of the loaded data 
df.head()

# print(data)

for index, row in df.iterrows():

    id = str(row[0])[1:]
    URL = str(row[1])
    Title = str(row[2])
    Time = str(row[3])
    if len(Time) > 19:
        print("sss")
        time = str(Time)[-18:] + ":00"
        time = time.replace("/", "-")
        time_str = time.split(' - ')
        date = time_str[0].split('-')
        Time = date[2] + '-' + date[1] + '-' + date[0] + "T" + time_str[1]
    ShortContent = str(row[4])
    FullContent = str(row[5])

    result = [id, URL, Title, Time, ShortContent, FullContent]
    dataframeResult = pd.DataFrame([result])
    dataframeResult.columns = ['id', 'url', 'title', 'time', 'short_content', 'full_content']
                # dataframeResult.to_csv("news-data.csv", index=False, mode='a', header=False)
                
    engine = create_engine("mysql+pymysql://root:@localhost/IR")
    with engine.connect() as conn, conn.begin():
        dataframeResult.to_sql(name='news1', con=engine, if_exists = 'append', index=False)


    # jsonStr += "{\"create\": { \"_id\": " + id + "}\n"
    # jsonStr += "{"
    # for col in cols:
    #     if(isinstance(row[col], str)):
    #         jsonStr += "\"" + col + "\": \"" + str(row[col]).replace("\"", "\\\"") + "\","
    #     else:
    #         jsonStr += "\"" + col + "\": " + str(row[col]).replace("\"", "\\\"") + ","
                