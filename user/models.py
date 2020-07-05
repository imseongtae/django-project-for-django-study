from django.db import models

# Create your models here.
# model에 작성된 클래스는 장고의 모델 클래스를 상속 받아야만 한다는 규칙을 가진다
class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='사용자명')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    # EmailField는 데이터가 이메일 형태인지 검증까지 해줌
    useremail = models.EmailField(max_length=128, verbose_name='이메일')
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록일')

    # 첫 번째 방법, 두 가지의 방법이 있다고 한다.
    # 클래스가 문자열로 변환 되었을 때, 어떻게 변환할지 결정하는 함수가 있다.
    # username으로 반환하도록 변경을 한다. 이를 통해 관리자 페이지에 보여지는 정보를 개선할 수 있다.
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'board_user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
        # 장고는 모델을 보여줄 때 기본적으로 복수형을 보여주기 때문에
        # 복수형에 대한 설정을 따로 해주는 것이 좋다.