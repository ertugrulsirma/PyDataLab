import pandas as pd
import pandasql as ps
import matplotlib.pyplot as plt

df = pd.read_csv('read.csv')

query = """SELECT
                'CurrencyEarned' AS TYPE,
                SOURCE AS CATEGORY,
                ROUND(SUM(AMOUNT) / (SELECT SUM(AMOUNT) FROM df WHERE EVENT_NAME = 'CurrencyEarned') * 100, 2) AS PERCENTAGE
            FROM 
                df 
            WHERE 
                EVENT_NAME = 'CurrencyEarned'
            GROUP BY
                SOURCE

            UNION ALL

            SELECT
                'CurrencySpent' AS TYPE,
                REASON AS CATEGORY,
                ROUND(SUM(AMOUNT) / (SELECT SUM(AMOUNT) FROM df WHERE EVENT_NAME = 'CurrencySpent') * 100, 2) AS PERCENTAGE
            FROM 
                df 
            WHERE 
                EVENT_NAME = 'CurrencySpent'
            GROUP BY
                REASON
            ORDER BY
                PERCENTAGE DESC;
            """

result = ps.sqldf(query, locals())
result.to_csv('result.csv', index=False)

df = pd.read_csv('result.csv')

# Filter the data for 'CurrencyEarned' type and create a new DataFrame called 'earning_data'
earning_data = df[df['TYPE'] == 'CurrencyEarned']

# Filter the data for 'CurrencySpent' type and create a new DataFrame called 'spending_data'
spending_data = df[df['TYPE'] == 'CurrencySpent']

# Set the size of the figure
plt.figure(figsize=(20, 9))

# Create the first subplot - Earning percentage distribution table
plt.subplot(2, 1, 1) # It means 2 row, 1 column and this one is the first
plt.title('Earning Percentage Distribution') # Table title
bars = plt.bar(earning_data['CATEGORY'], earning_data['PERCENTAGE']) # Draw bar. Category means x-axis and Percentage means y-axis
plt.xlabel('Category') # X-axis label
plt.ylabel('Percentage') # Y-axis label
plt.xticks(rotation=45, ha='right') # Rotate X-axis labels 45 degrees for better readability

# Display percentage values for each category value
for bar in bars:
    yval = bar.get_height() # Get the height of the bar to use as the percentage value
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.1f}%', ha='center', va='bottom') # Add percentage above the bar

# Adjust the layout to reduce spaces between elements
plt.tight_layout()

# Create the second subplot - Spending percentage distribution table
plt.subplot(2, 1, 2) # It means 2 row, 1 column and this one is the second
plt.title('Spending Percentage Distribution') # Table title
bars = plt.bar(spending_data['CATEGORY'], spending_data['PERCENTAGE']) # Draw bar. Category means x-axis and Percentage means y-axis
plt.xlabel('Category') # X-axis label
plt.ylabel('Percentage') # Y-axis label
plt.xticks(rotation=45, ha='right') # Rotate X-axis labels 45 degrees for better readability

# Display percentage values for each category value
for bar in bars:
    yval = bar.get_height() # Get the height of the bar to use as the percentage value
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.1f}%', ha='center', va='bottom') # Add percentage above the bar

# Adjust the layout to reduce spaces between elements
plt.tight_layout()

# Show the plot on the screen
plt.show()