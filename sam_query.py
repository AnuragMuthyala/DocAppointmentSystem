import psycopg2
from datetime import datetime, timedelta

try:
    context = {}
    connection = psycopg2.connect(user="med",
                                  password="a",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="med_schedule")
    cursor = connection.cursor()
    dept = 'classA'
    d = '2020-09-26'
    cd = '2020-09-26'
    ct = '13:40:27'
    query = "SELECT dname,a_date,a_time FROM doctors, appointments WHERE dname=d_name AND deptname=\'"+dept+"\' AND a_date=\'"+d+"\' AND (a_date > \'"+cd+"\' OR (a_date = \'"+cd+"\' AND a_time > \'"+ct+"\'))"
    print(query)
    cursor.execute(query)

    docs = cursor.fetchall()

    for row in docs:
        try:
            context[row[0]].append(row[2].isoformat())
        except:
            context[row[0]] = [row[2].isoformat()]

    query = "SELECT DISTINCT a_date FROM appointments"
    cursor.execute(query)

    docs = cursor.fetchall()

    for row in sorted(docs):
        try:
            context['dates'].append(row[0].isoformat())
        except:
            context['dates'] = [row[0].isoformat()]

except (Exception, psycopg2.Error) as error:
    print(error)

finally:
    if connection:
        cursor.close()
        connection.close()

print(context)