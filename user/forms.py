from django import forms
from .models import User
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={
            'required': '아이디를 입력해주세요'
        },
        max_length=32, label="사용자 이름")
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요'
        },
        widget=forms.PasswordInput, label="비밀번호")
    # 비밀번호를 패스워드 타입으로 만들기 위해선 위젯을 직접 지정해야 한다.

    # 비밀번호 일치여부 확인하는 코드
    def clean(self):
        cleaned_data = super().clean() # 값이 들어있지 않으면 여기서 실패처리해서 나간다.
        # 값이 들어왔다는 검증이 끝나면 값을 가지고 온 후에
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:			
                self.add_error('username', '아이디가 없습니다.')
                return # 예외 이후 코드의 진행을 return을 통해 막음
				
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.') # 특정 필드에 에러를 넣는 함수
            else:
                self.user_id = user.id # 이렇게 하면 self를 통해서 클래스 변수로 들어가고 밖에서도 접근할 수 있게 된다.