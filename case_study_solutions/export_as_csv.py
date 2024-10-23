import pandas as pd
import pandasql as sql

df = pd.read_csv('read.csv')

query = """SELECT 
                EVENT_DATE,
                GAME_MODE,
                ROUND((SUM(RESULT) / COUNT(RESULT)) * 100, 2) AS WIN_RATE,
                ROUND((1 - (SUM(RESULT) / COUNT(RESULT))) * 100, 2) AS FAIL_RATE,
                ROUND(((SUM(RESULT) / COUNT(RESULT)) * 100) - ((1 - (SUM(RESULT) / COUNT(RESULT))) * 100), 2) AS DIFFERENCE
            FROM 
                df
            WHERE 
                RESULT IN (1,0)
            GROUP BY
                EVENT_DATE,
                GAME_MODE
            ORDER BY
                EVENT_DATE ASC;
        """

result = sql.sqldf(query, locals())
result.to_csv('result.csv', index=False)