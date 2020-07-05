from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from user.models import User
from .models import Board
from .forms import BoardForm

# Create your views here.
def board_list(request):
    all_boards = Board.objects.all().order_by('-id')     
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_boards, 2)
    
    boards = paginator.get_page(page)        
    return render(request, 'board_list.html', {'boards': boards})

def board_write(request):
  if not request.session.get('user'):
    return redirect('/user/login')

  if request.method == 'POST':
    form = BoardForm(request.POST) # POST일 때 데이터를 넣는다.
    if form.is_valid():
      # 세션에서 유저 아이디를 가져오고
      user_id = request.session.get('user');
      # 유저아이디를 이용해 모델에서 pk가 user_id인 것을 가져옴
      user = User.objects.get(pk=user_id)

      board = Board()
      board.title = form.cleaned_data['title']
      board.contents = form.cleaned_data['contents']
      # 사용자가 로그인했으면 정보가 session에 들어있다.
      board.writer = user # user 를 writer에 추가
      board.save() # save를 통해 데이터베이스에 저장이 된다.

      # redirect 경로
      return redirect('/board/list/')
  else:
    form = BoardForm()
  return render(request, 'board_write.html', {'form': form})

def board_detail(request, pk):
  try:
    board = Board.objects.get(pk=pk)
  except Board.DoesNotExist:
    raise Http404('게시글을 찾을 수 없습니다.')
    
  return render(request, 'board_detail.html', {'board': board})

