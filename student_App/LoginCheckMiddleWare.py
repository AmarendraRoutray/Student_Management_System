from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse



class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self,request,view_func,view_args,views_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user=request.user
        if user.is_authenticated:
            if user.user_type == '1':
                if modulename == 'student_App.HodViews':
                    pass
                elif modulename == 'student_App.views' or modulename == 'django.views.static':
                    pass
                else:
                    return HttpResponseRedirect(reverse('admin_home'))
            elif user.user_type == '2':
                if modulename == 'student_App.StaffViews':
                    pass
                elif modulename == 'student_App.views' or modulename == 'django.views.static':
                    pass
                else:
                    return HttpResponseRedirect(reverse('staff_home'))
            elif user.user_type == '3':
                if modulename == 'student_App.StudentViews':
                    pass
                elif modulename == 'student_App.views'  or modulename == 'django.views.static':
                    pass
                else:
                    return HttpResponseRedirect(reverse('student_home'))
            else:
                return HttpResponseRedirect(reverse('showLoginPage'))
        else:
            if request.path == reverse('showLoginPage') or request.path == reverse('do_login'):
                pass
            else:
                return HttpResponseRedirect(reverse('showLoginPage'))