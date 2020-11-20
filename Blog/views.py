
from distutils.command import register
from django.contrib.sessions import serializers
from django.core.mail import send_mail

from django.http import HttpResponse

from .forms import commentform,replyform, UserLogin,RegistrationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.template import RequestContext

from django.shortcuts import render, render_to_response, redirect

from .forms import *
from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail
from django.template import RequestContext
from django.contrib.auth import authenticate,get_user_model,login as login_auth,logout
import re



def allPosts(request):

    all_posts= Post.objects.all().order_by('created_at')
    page = request.GET.get('page',1)
    paginator = Paginator(all_posts, 5)
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    all_cat = getCat()
    all_tag = getTag()
    sub_cat = sub(request)
    context = {"allPosts": posts, "allCat": all_cat, "subcat": sub_cat,"alltag":all_tag}


    return render(request, "blog/home.html", context)


def search(request):

    try:
        tag = Tag.objects.get(name__icontains=request.GET['term'])
        byTag = Post.objects.filter(tag=tag.id).order_by('created_at')
    except Tag.DoesNotExist:
        byTag = None
    try:
        found_entries = Post.objects.filter(title__icontains=request.GET['term']).order_by('created_at')

    except Post.DoesNotExist:
        found_entries = None
    all_cat = getCat()
    all_tag = getTag()
    sub_cat = sub(request)

    all_tag = getTag()

    context = {"allPosts": found_entries, "tags": byTag, "allCat": all_cat, "subcat": sub_cat,"alltag":all_tag}
    return render(request, "blog/search.html", context)

def getPostsTag(request,tag_id):
    tag = Tag.objects.get(id=tag_id)
    posts = Post.objects.filter(tag=tag.id).order_by('created_at')
    all_cat = getCat()
    sub_cat = sub(request)
    all_tag = getTag()
    context = {"allPosts": posts, "allCat": all_cat, "subcat": sub_cat,"alltag":all_tag}
    return render(request, "blog/home.html", context)




def getCat():

    cat=Category.objects.all()
    return cat

def getTag():

    tag=Tag.objects.all()
    return tag


def getPostsCat(request, cat_id):
    all_posts = Post.objects.filter(cat_id= cat_id).order_by('created_at')
    all_cat = getCat()
    all_tag = getTag()
    sub_cat = sub(request)
    context = {"allPosts": all_posts, "allCat": all_cat, "subcat": sub_cat,"alltag":all_tag}

    all_tag = getTag()

    return render(request, "blog/home.html", context)



def subscribe(request):
    cat_id = request.GET.get('catid', None)
    status = Category.subscribe.through.objects.filter(category_id=cat_id, user_id=request.user.id).exists()

    if status:
        #remove
        Category.subscribe.through.objects.filter(category_id=cat_id, user_id=request.user.id).delete()
        data = {
            'x': 1
        }

    else:

		Category.subscribe.through.objects.create(category_id=cat_id, user_id=request.user.id)
		cat = Category.objects.get(id=cat_id)
		send_mail('Category Subscription',
				  ' hello ' + request.user.username + ', you have subscribed successfully in ' + cat.name + ' welcome aboard',
				  'myblog@blog.com', [request.user.email])
		data = {
			'x': 2

		}

		return JsonResponse(data)


    return JsonResponse(data)

def filterwithoutbadwords(comment):

	commentsplitted=comment.split()
	ob2 = BadWord.objects.all() 
	counter=0
	for c in commentsplitted:
		c=c.lower()
		for o in ob2:
			o=o.name.lower()
			if c == o:
				size=len(c)
				cnew=""
				for cindex in c:
					cnew=cnew+"*"
					cnew=str(cnew)
				commentsplitted[counter]=cnew
		counter+=1
	mylists=""
	for uu in commentsplitted:
		mylists = mylists + uu + " "
		mylist2=str(mylists)
	return mylist2


def postPage(request,post_id):
	form = commentform()
	form1=replyform()
	user__id=1
	postlike = Like.objects.filter(post_id= post_id,state=1 ).count()
	postdislike = Like.objects.filter(post_id= post_id,state=0).count()

	obblike = Like.objects.filter(post_id= post_id,user_id=user__id,state=1).exists()
	obbdislike = Like.objects.filter(post_id= post_id,user_id=user__id,state=0).exists()

	ob = Post.objects.get(id=post_id)
	obb = Tag.objects.raw('select * from Blog_tag where id in(select tag_id from Blog_post_tag where post_id=' + post_id + ')')
	ob1 = Comment.objects.filter(post_id=post_id)
	xx=[]
	xx1=[]
	for x in ob1:
		varg =filterwithoutbadwords(x.body)
		xx.append(varg)
		ob5 = User.objects.get(id=x.user_id)
		xx1.append(ob5)
	zipped_data= zip(ob1,xx,xx1)
	xx1=[]
	xx11=[]
	ob2 = Reply.objects.all()
	for x1 in ob2:
		varg =filterwithoutbadwords(x1.body)
		xx1.append(varg)
		ob5 = User.objects.get(id=x1.user_id)
		xx11.append(ob5)
	zipped_data1= zip(ob2,xx1,xx11)
	all_cat = getCat()
	all_tag = getTag()
	sub_cat = sub(request)

	context = {'post_list':ob,
	'tag_list':obb,
	'zipped_data':zipped_data,
	'zipped_data1':zipped_data1,

	"allCat": all_cat,
	"subcat": sub_cat,
	"alltag":all_tag,
	'obblike':obblike,
	'obbdislike':obbdislike,
	'postlike':postlike,
    'postdislike':postdislike,

	}


	return render(request, 'blog/postpage.html', context)






def new_comment(request):
	form = commentform()
	ob1= form.save(commit=False)
	ob1.post_id=request.GET.get('post_id',None)
	ob1.user_id=request.user.id
	ob1.body=request.GET.get('body',None)
	ob1.save()
	ob1.created_at = ob1.created_at.strftime("%b.%d, %Y, %I:%M%p")
	body =filterwithoutbadwords(ob1.body)
	data = {
	'idd' :ob1.id,
	'bodyy' :body,
	'username':request.user.username,
	'createdat':ob1.created_at
	}
	
	return JsonResponse(data)

def new_reply(request):
	form1 = replyform()
	ob1= form1.save(commit=False)
	ob1.comment_id=request.GET.get('comment_id_reply',None)
	ob1.user_id = request.user.id
	ob1.body=request.GET.get('bodyreply',None)
	ob1.save()
	#ob1.created_at=formunix(ob1.created_at)
	ob1.created_at=ob1.created_at.strftime("%b.%d, %Y, %I:%M%p")
	body =filterwithoutbadwords(ob1.body)
	data = {
	'idd' :ob1.id,
	'bodyy' :body,
	'username':request.user.username,
	'createdat':ob1.created_at 
	}
	return JsonResponse(data)






def comment_delete(request):
	comment_id=request.GET.get('comment_id',None)
	comm=Comment.objects.get(id=comment_id)
	comm.delete()
	data = {
	'x' :1
	}
	
	return JsonResponse(data)

def sub(request):
    catsub=Category.objects.filter(subscribe=request.user.id)
    cat_sub=[]
    for i in catsub:
        cat_sub.append(i.id)
    return cat_sub



User = get_user_model()
def login(request):
	form = UserLogin(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
	return render(request, "blog/login_page.html", {"form" : form})


def register(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login_auth(request,user)
			return redirect("/")

	else:
		form = RegistrationForm()

	return render(request, "blog/register.html", {"form": form})



def dislikePost(request):
	post_id = request.GET.get('post_id', None)
	post = Post.objects.filter(id=post_id)
	mypost = Post.objects.get(id=post_id)
	usr=User.objects.get(id=request.user.id)
	row=Like.objects.all().filter(state=0, user=usr, post=post[0])
	row2 = Like.objects.all().filter(state=1, user=usr, post=post[0])
	if row.exists():
		deletelike=Like.objects.get(state=0, user=usr, post=post[0])
		deletelike.delete()
	else:
		Like.objects.create(state=0, user=usr, post=post[0])
        if row2.exists():
            deletelike = Like.objects.get(state=1, user=usr, post=post[0])
            deletelike.delete()
	discount = Like.objects.filter(state=0, post=mypost).count()
	likesCount = Like.objects.filter(state=1, post=mypost).count()
	if discount == 2:
		mypost.delete()


	data = {
		'disCount': discount,
		'likesCount':likesCount
	}
	return JsonResponse(data)





def likePost(request):
	post_id = request.GET.get('post_id', None)
	likedpost = Post.objects.get(id=post_id)
	likecheck=Like.objects.filter(post=post_id,user_id=request.user.id)
	if likecheck:
		if(likecheck[0].state==1):
			likecheck.delete()
		else:


			likecheck[0].state=1
			likecheck[0].save()



	else:
		like = Like.objects.create(user_id=request.user.id, post=likedpost,state = 1)
		like.save()  # saving it to store in database

	likesCount = Like.objects.filter(state=1, post=likedpost).count()
	discount = Like.objects.filter(state=0, post=likedpost).count()

	data = {

		'disCount': discount,
		'likesCount':likesCount
	}
	return JsonResponse(data)
