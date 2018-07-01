# views are the response of the server to the url requested by the client
# Create your views here.
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Code, User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth import views, authenticate, login, logout

loggedIn = False

#checks validity of the username requested by client
def validity(uid):
    #put in email id checker code

    if(User.objects.filter(username=uid).exists()):
        return False

    return True

#homepage
def index(request):
    return render(request,'CodeMate/landing_page.html',{})

#intermediate page for saving a new code
def addObject(request):
    language=request.POST['language']
    content=request.POST['content']
    expire=request.POST['expire']
    slug=request.POST['slug']
    newPaste=Code(language=language,content=content,expire=expire,slug=slug)
    newPaste.save()
    redirectionString='/codemate/paste/'+str(slug)
    return HttpResponseRedirect(redirectionString);

#page that loads the new code creation form
def createView(request):
    return render(request,'CodeMate/code_form.html',{})

#login intermediate. checks for correct username/password pair
def authUser(request):
    username=request.POST['username']
    password=request.POST['password']

    if(User.objects.filter(username=username).exists()):
        user=User.objects.get(username=username)
        if(user.check_password(password)):
            print('Credential Verified!')
            login(request,user)
            return redirect('code:loggedIn')

    print('Verification Failed!')
    return redirect('code:loginFailure')

#login page
def logIn(request):
    return render(request,'CodeMate/login.html',{})

#logged-in version of new code creation page
def loggedIn(request):
    return render(request,'CodeMate/loggedIn.html',{})

#logout intermediate
def logOut(request):
    logout(request)
    return redirect('code:create')

#page that loads on username/password mismatch
def loginFailure(request):
    return render(request,'CodeMate/loginFailure.html',{'error_msg':'Invalid username or password!'})

#signup intermediate. checks for validity of supplied fields
def validUser(request):
    frst_name=request.POST['fname']
    last_name=request.POST['lname']
    username=request.POST['uid']
    password=request.POST['pass']
    passcnfrm=request.POST['passcnfrm']

    if(not validity(username)):
        return render(request,'CodeMate/signup.html',{'error_msg':'Username already exists!'})

    if(len(username)<6):
        return render(request,'CodeMate/signup.html',{'error_msg':'Username must be atleast 6 characters long!'})

    if(len(password)<6):
        return render(request,'CodeMate/signup.html',{'error_msg':'Password must be atleast 6 characters long!'})

    if(not password==passcnfrm):
        return render(request,'CodeMate/signup.html',{'error_msg':'Passwords do no match!'})

    user=User(first_name=frst_name,last_name=last_name,username=username)
    user.set_password(password)
    user.save()
    return redirect('code:logIn')

#signup page
def signup(request):
    return render(request,'CodeMate/signup.html',{})

#intermediate page thet loads when 'save' button is clicked. modifies the
#existing code of the object
def modify(request,slug):
    code=Code.objects.get(slug=slug)
    code.content=request.POST['content']
    code.save()

    redirectString='/codemate/paste/'+str(slug)
    return redirect(redirectString)

#generic view to delete an object. invoked when 'delete' is clicked.
class deleteView(generic.DeleteView):
    model = Code
    success_url = reverse_lazy('code:create')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

#the final page which contains the url and actual code after creation
class details(generic.DetailView):
    model = Code
    template_name = 'CodeMate/details.html'

    def get_queryset(self):
        global loggedIn
        return Code.objects.filter(slug=self.kwargs['slug'])
