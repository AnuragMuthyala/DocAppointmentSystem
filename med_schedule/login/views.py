from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from login.form import RegisterForm, LoginForm  
import psycopg2

# Create your views here.
def userLogin(request):
    context = {}
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if dict(request.POST)['but'][0] == 'login':
            if f.is_valid():
                name = f.cleaned_data.get('name')
                password = f.cleaned_data.get('password')
                user = authenticate(request, username=name, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/home/')
                else:
                    context['error'] = '*Username or Password is incorrect'
                    print('Invalid User')
            else:
                context['error'] = '*Invalid Details'
                print('Invalid User')
        elif dict(request.POST)['but'][0] == 'deleter':
            print(User.objects.all())
            User.objects.all().delete()
            print(User.objects.count())
        else:
            return redirect('/register/')
    return render(request, 'login.html', context=context)

def register(request):
    context = {}
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid():
            name = f.cleaned_data.get('name')
            password = f.cleaned_data.get('password')
            age = f.cleaned_data.get('age')
            gender = f.cleaned_data.get('gender')
            cnumber = f.cleaned_data.get('cnumber')
            try:
                connection = psycopg2.connect(user="med",
                                      password="a",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="med_schedule")

                cursor = connection.cursor()
                cursor.execute('SELECT * FROM patients WHERE pname=\'{}\''.format(name))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    context['error'] = '*Username already in use'
                    raise Exception
                query = "INSERT INTO patients VALUES(%s,%s,%s,%s)"
                vals = (name, int(age), gender, int(cnumber))
                cursor.execute(query, vals)
                connection.commit()
                print('Done!')
                user = User.objects.create_user(name, 'default@def.com', password)
                print(user)
                user.save()
                return redirect('/')
            except (Exception, psycopg2.Error) as error:
                print(error)
            finally:
                if (connection):
                    cursor.close()
                    connection.close()
    return render(request, 'register.html', context)

def userLogout(request):
    logout(request)
    return redirect('/')