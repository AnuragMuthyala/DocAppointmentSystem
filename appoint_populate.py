import psycopg2
from datetime import datetime, timedelta

try:
    connection = psycopg2.connect(user="med",
                                  password="a",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="med_schedule")
    cursor = connection.cursor()

    query = "SELECT dname FROM doctors"
    cursor.execute(query)

    docs = cursor.fetchall()

    for row in docs:
        init_date = datetime.fromisoformat('2021-09-27 09:00:00')
        time_gap = timedelta(minutes=20)
        date_gap = timedelta(hours=12)
        for j in range(5):
            for i in range(36):
                date = init_date.isoformat().split('T')
                name = row[0]
                #print(date)
                query = "INSERT INTO appointments VALUES(%s,%s,%s,%s,%s,%s)"
                vals = ('TBF', name, date[0], date[1], 'O', 'TBF')
                cursor.execute(query, vals)
                #print(init_date)
                init_date = init_date + time_gap
            init_date = init_date+date_gap
            print('Day Completed!')
    connection.commit()

except (Exception, psycopg2.Error) as error:
    print(error)

finally:
    if connection:
        cursor.close()
        connection.close()