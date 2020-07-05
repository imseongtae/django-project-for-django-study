from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .forms import LoginForm

# Create your views here.
def register(request):  
  if request.method == 'GET':
    # 경로는 템플릿 폴더를 바라보므로 경로를 따로 표현할 필요는 없다
    return render(request, 'register.html')
  elif request.method == 'POST':    
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    re_password = request.POST.get('re-password', None)
    useremail = request.POST.get('useremail', None)
    # form 을 통해 넘어오는 input 속성의 name 값을 키로 사용해서 값을 얻는다.

    res_data = {}
    # 먼저 모든 값들이 들어와 있는지 확인을 하고 들어오지 않았을 때 아래 메시지 출력
    if not (username and password and re_password and useremail):
        res_data['info_error'] = '회원정보가 올바르게 입력되지 않았습니다.'
    elif password != re_password:
        res_data['password_error'] = '비밀번호가 다릅니다.'
    else:
      user = User(
        username=username,
        useremail=useremail,
        # 장고에서는 암호화해서 저장하는 make_password 메서드를 지원해줌
        # password=password가 아니라 아래처럼 더 개선된 방법으로 작성할 수 있다.
        password=make_password(password) # 비밀번호를 함수 안에 전달
      )
    # 이렇게 하고서 저장을 하면 끝이남
    user.save() # 클래스 변수 객체를 하나 생성하고 저장하면 된다..!

    return render(request, 'register.html', res_data)

def login(request):
    if request.method == 'POST':
        # POST일때는 폼 클래스 변수를 만들 때 Post 데이터를 넣어준다.
        form = LoginForm(request.POST)
        if form.is_valid():
            # session 코드가 위치한다.
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout(request):

    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')
    # 템플릿이 필요가 없다. 주소만 지정해주면 된다.

def home(request):
  # user_id = request.session.get('user')
  # if user_id:
  #    user = User.objects.get(pk=user_id)
  return render(request, 'home.html');