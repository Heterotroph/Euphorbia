from django import forms
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from users.models import User

__author__ = 'igorzygin'


from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, RequestContext, Context
from django.views.generic import FormView




class RegisterView(FormView):
    template_name = 'register.html'
    model = User
    success_url = '/'


    def get(self, request, **kwargs):
        if not request.user.is_anonymous():
            return HttpResponseRedirect("/")
        return self.render_to_response({"form":RegisterForm()})

    def post(self, request, **kwargs):
        form = RegisterForm(request.POST)
        print request.POST
        if form.is_valid():
            user=self.create_user(form)
            print user
            if user:
                return get_http_response(request,'register_success.html', user)
            else:
                return get_http_response(request,'register_fail.html', user)
        else:
            return self.render_to_response({"form":form})

    def create_user(self, form):
        try:
            user = User.objects.create_user(username=form.cleaned_data['email'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])
            user.roles = [form.cleaned_data['role']]
            user.is_active = True
            user.save()
            return user
        except Exception as e:
            print e
            return None



class RegisterForm(forms.Form):
    password = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    phone = forms.CharField(max_length=100, required=True)
    role = forms.DecimalField(max_value=1, required=True)


    def is_valid(self):
        valid = super(RegisterForm, self).is_valid()
        if not valid:
            return valid
        if len(User.objects.filter(email=self.cleaned_data['email']))>0:
            self._errors['email'] = 'User with this email already exists'
            return False

        return valid


def get_http_response(request,template_name,user):
    t = loader.get_template(template_name)
    c = Context({'user': user}) if user is not None else RequestContext(request, {})
    return HttpResponse(t.render(c))





class ClientManager(BaseUserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        # if not username:
        # raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)
