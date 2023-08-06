from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pymysql

# Authenticate with Google Analytics
credentials = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', ['https://www.googleapis.com/auth/analytics.readonly'])
analytics = build('analyticsreporting', 'v4', credentials=credentials)

# Query Google Analytics for keywords data
response = analytics.reports().batchGet(
    body={
        'reportRequests': [
            {
                'viewId': 'VIEW_ID',
                'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                'metrics': [{'expression': 'ga:searchUniques'}],
                'dimensions': [{'name': 'ga:keyword'}]
            }
        ]
    }
).execute()

# Connect to MySQL database
connection = pymysql.connect(host='HOST', user='USER', password='PASSWORD', database='DATABASE')
cursor = connection.cursor()

# Process the response and insert data into the Keywords table
for report in response.get('reports', []):
    rows = report.get('data', {}).get('rows', [])
    for row in rows:
        dimensions = row.get('dimensions', [])
        metrics = row.get('metrics', [])
        color_code = '#FF5733' # Replace with logic to determine color code if needed
        # Insert data into the database
        insert_query = "INSERT INTO Keywords (Keyword, SearchVolume, ColorCode) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (dimensions[0], metrics[0]['values'][0], color_code))

# Commit the transaction and close the connection
connection.commit()
connection.close()
