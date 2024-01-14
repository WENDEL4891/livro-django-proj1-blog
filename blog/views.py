from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import ListView

from .forms import CommentForm, EmailPostForm
from .models import Post

# Create your views here.

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # três postagens em cada página
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exibe a primeira página
        posts = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo,
        # exibe a última página de resultados
        posts = paginator.page(paginator.num_pages)        
    return render(request,
                  'blog/post/list.html',
                  {'page': page, 'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Um comentário foi postado
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Cria o objeto Comment, mas não
            # o salva ainda no banco de dados
            new_comment = comment_form.save(commit=False)
            # Atribui a postagem atual ao commentário
            new_comment.post = post
            # Salva o comentário no banco de dados
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
            'blog/post/detail.html',
            {'post':post,
             'comments':comments,
             'new_comment':new_comment,
             'comment_form':comment_form})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # Obtém a postaem com base no id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Formulário foi submetido
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Campos do formulário passaram pela validação
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f'{cd["name"]} recommends you read '\
            f'{post.title}'
            message = f'Read {post.title} at {post_url}\n\n'\
            f'{cd['name']}\'s comments: {cd["comments"]}'
            send_mail(subject, message, 'admin@myblog.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post,
                                                        'form':form,
                                                        'sent': sent})
