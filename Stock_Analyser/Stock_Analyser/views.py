# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.shortcuts import redirect,render

# from functools import wraps

# def session_login_required(function=None):
#     def decorator(view_func):
#         @wraps(view_func)
#         def f(request, *args, **kwargs):
#             token = request.session.get('token', False)

#             if token:
#                 access_token = AccessToken(token)
#                 print(access_token)
#                 user = access_token.payload.get('user_id')
#                 print(user)
#                 return view_func(request, *args, **kwargs)
            
#             return redirect('/')
        
#         return f
#     if function is not None:
#         return decorator(function)
#     return decorator