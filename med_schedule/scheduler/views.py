from django.shortcuts import render, redirect
from datetime import datetime
import psycopg2
import re

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request, 'home.html')

def createAppoint(request):
    if not request.user.is_authenticated:
        return redirect('/')
    context = {}
    if request.method == 'GET':
        try:
            context = {}
            connection = psycopg2.connect(user="med",
                                          password="a",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="med_schedule")
            cursor = connection.cursor()
            
            query = "SELECT DISTINCT deptname FROM doctors"
            cursor.execute(query)

            docs = cursor.fetchall()

            for row in docs:
                try:
                    context['depts'].append(row[0])
                except:
                    context['depts'] = [row[0]]
            print(context)

        except (Exception, psycopg2.Error) as error:
            print(error)

        finally:
            if connection:
                cursor.close()
                connection.close()

    elif request.method == 'POST':
        print(dict(request.POST)['but'][0])
        return redirect('/home/create/'+dict(request.POST)['but'][0])
    return render(request, 'createAppoint.html', context=context)

def priorAppoint(request):
    if not request.user.is_authenticated:
        return redirect('/')
    try:
        context = {}
        connection = psycopg2.connect(user="med",
                                      password="a",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="med_schedule")
        cursor = connection.cursor()
        
        query = "SELECT d_name,a_date,a_time,issue FROM appointments WHERE p_name=\'{0}\' AND status=\'{1}\'".format(request.user, 'C')
        cursor.execute(query)

        docs = cursor.fetchall()

        for row in docs:
            try:
                context['docs'].append((row[0], row[1].isoformat(), row[2].isoformat(), row[3]))
            except:
                context['docs'] = [(row[0], row[1].isoformat(), row[2].isoformat(), row[3])]
        print(context)

    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
    return render(request, 'priorAppoint.html', context=context)

def bookDate(request, dept):
    if not request.user.is_authenticated:
        return redirect('/')
    print([dept])
    context = {}
    if request.method == 'GET':
        d = datetime.today().isoformat().split('.')[0].split('T')
        print(d)
        cd = d[0]
        ct = d[1]
        d = d[0]
        print(len(d))
        print(len(ct))
        try:
            context = {}
            connection = psycopg2.connect(user="med",
                                          password="a",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="med_schedule")
            cursor = connection.cursor()
            
            query = "SELECT dname,a_date,a_time FROM doctors, appointments WHERE dname=d_name AND status!='C' AND deptname=\'{0}\' AND a_date=\'{1}\' AND (a_date > \'{2}\' OR (a_date = \'{3}\' AND a_time > \'{4}\'))".format(dept, d, cd, cd, ct)
            
            cursor.execute(query)

            docs = cursor.fetchall()

            di = {}
            for row in docs:
                try:
                    di[(row[0], row[1].isoformat())].append(row[2].isoformat())
                except:
                    di[(row[0], row[1].isoformat())] = [row[2].isoformat()]

            for key in di.keys():
                try:
                    context['docs'].append((key[0], key[0]+'->'+key[1], di[key]))
                except:
                    context['docs'] = [(key[0], key[0]+'->'+key[1], di[key])]

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

    elif request.method == 'POST':
        req_d = dict(request.POST)
        if 'dates' in req_d.keys():
            dt = req_d['dates'][0]
            d = datetime.today().isoformat().split('.')[0].split('T')
            cd = d[0]
            ct = d[1]
            d = dt
            try:
                context = {}
                connection = psycopg2.connect(user="med",
                                              password="a",
                                              host="127.0.0.1",
                                              port="5432",
                                              database="med_schedule")
                cursor = connection.cursor()
                
                query = "SELECT dname,a_date,a_time FROM doctors, appointments WHERE dname=d_name AND status!='C' AND deptname=\'"+dept+"\' AND a_date=\'"+d+"\' AND (a_date > \'"+cd+"\' OR (a_date = \'"+cd+"\' AND a_time > \'"+ct+"\'))"
                cursor.execute(query)

                docs = cursor.fetchall()

                di = {}
                for row in docs:
                    try:
                        di[(row[0], row[1].isoformat())].append(row[2].isoformat())
                    except:
                        di[(row[0], row[1].isoformat())] = [row[2].isoformat()]

                for key in di.keys():
                    try:
                        context['docs'].append((key[0], key[0]+'->'+key[1], di[key]))
                    except:
                        context['docs'] = [(key[0], key[0]+'->'+key[1], di[key])]

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
        else:
            k = ''
            choice = req_d['times']
            for key in req_d.keys():
                l = re.findall(r'[a-zA-Z]*->\d\d\d\d-\d\d-\d\d', key)
                if l != []:
                    k+=key
            print(choice[0])
            print(k)
            ind = k+'T'+choice[0]
            return redirect('/home/create/'+dept+'/'+ind)

    print(context)
    return render(request, 'bookDate.html', context=context)

def bookAppt(request, dept, ind):
    if not request.user.is_authenticated:
        return redirect('/')
    context = {}
    if request.method == 'GET':
        toks = ind.split('->')
        doc = toks[0]
        toks = toks[1].split('T')
        dt, ti = toks[0], toks[1]
        context = {'doc': doc, 'date': dt, 'time': ti}
    elif request.method == 'POST':
        toks = ind.split('->')
        doc = toks[0]
        toks = toks[1].split('T')
        dt, ti = toks[0], toks[1]
        req_d = dict(request.POST)
        issue = req_d['issue'][0]
        try:
            context = {}
            connection = psycopg2.connect(user="med",
                                          password="a",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="med_schedule")
            cursor = connection.cursor()
            query = "UPDATE appointments SET issue=\'{0}\' WHERE d_name=\'{1}\' AND a_date=\'{2}\' AND a_time=\'{3}\'".format(issue, doc, dt, ti)
            cursor.execute(query)
            query = "UPDATE appointments SET status=\'{0}\' WHERE d_name=\'{1}\' AND a_date=\'{2}\' AND a_time=\'{3}\'".format('C', doc, dt, ti)
            cursor.execute(query)
            query = "UPDATE appointments SET p_name=\'{0}\' WHERE d_name=\'{1}\' AND a_date=\'{2}\' AND a_time=\'{3}\'".format(request.user, doc, dt, ti)
            cursor.execute(query)
            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print(error)

        finally:
            if connection:
                cursor.close()
                connection.close()
        return redirect('/home/')
        
    return render(request, 'bookAppt.html', context=context)
