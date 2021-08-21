from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from feed.models import Post ,Comments ,Like ,Images
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import Profile, FriendRequest ,UserFollowing
from .forms import UserRegisterForm, UserUpdateForm, ProfileBioUpdateForm ,ProfileSkillUpdateForm,ProfileImageUpdateForm
import random
from django.contrib.auth.models import User

User = get_user_model()

@login_required
def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    my_friends = request.user.profile.friends.all()
    sent_to = []
    friends = []
    for user in my_friends:
        friend = user.friends.all()
        for f in friend:
            if f in friends:
                friend = friend.exclude(user=f.user)
        friends += friend
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in friends:
            random_list.remove(r)
    friends += random_list
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    for se in sent_friend_requests:
        sent_to.append(se.to_user)
    context = {
        'users': friends,
        'sent': sent_to
    }
    return render(request, "users/users_list.html", context)

def friend_list(request):
	p = request.user.profile
	friends = p.friends.all()
	print("in the friend list")
	followers = p.followers.all()
	for i in followers:
		print("followers in :",i)
	context={
	'friends': friends
	}
	return render(request, "users/friend_list.html", context)

@login_required
def send_friend_request(request, id):
	user = get_object_or_404(User, id=id)
	frequest, created = FriendRequest.objects.get_or_create(
			from_user=request.user,
			to_user=user)
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))



@login_required
def accept_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	if(FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
		request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
		request_rev.delete()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

@login_required
def delete_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

def delete_friend(request, id):
	user_profile = request.user.profile
	friend_profile = get_object_or_404(Profile, id=id)
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)
	return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))

@login_required
def profile_view(request, slug):
	p = Profile.objects.filter(slug=slug).first()
	print("in profile view")
	u = p.user
	# sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
	# rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)

	user_posts = Post.objects.filter(user_name=u).order_by('-date_posted')

	friends = p.friends.all()
	print("profile :wallah:",request.user.profile)
	followings = p.followings.all()
	followers = p.followers.all()
	liked = [i for i in Post.objects.all() if Like.objects.filter(user = u, post=i)]
	print("u:",u)
	print("in othes profile",p)
	print("following :",followings)
	print("followers :",followers)
	# is this user our friend
	followed_post_img = []
	for img in user_posts:
		image = Images.objects.filter(post=img)
		followed_post_img.append(image)
		# print("images is ",image)	
	print("followed_post_img is :",followed_post_img)
	button_status = 'none'
	if p not in request.user.profile.followings.all():
		button_status = 'Follow_the_user'
		print("button status:",button_status)

	else:
		button_status = 'unFollow_the_user'
		print("button status:",button_status)
		# if we have sent him a friend request
		# if len(FriendRequest.objects.filter(
		# 	from_user=request.user).filter(to_user=p.user)) == 1:
		# 		button_status = 'friend_request_sent'

		# # if we have recieved a friend request
		# if len(FriendRequest.objects.filter(
		# 	from_user=p.user).filter(to_user=request.user)) == 1:
		# 		button_status = 'friend_request_received'

	context = {
		'u': u,
		'button_status': button_status,
		'friends_list': friends,
		'followers': followers,
		'followings': followings,
		'post_count': user_posts.count,
		'posts':user_posts,
		'followed_post_img':followed_post_img,
		'liked_post':liked
		# 'sent_friend_requests':sent_friend_requests,
		# 'rec_friend_requests':rec_friend_requests
	}
	# sent_friend_requests
	# rec_friend_requests
	return render(request, "users/profile.html", context)

@login_required
def profile_delete(request,id):
	post = User.objects.get(pk=id)
	print("in the profile delete b",post)
	if request.user== post:
		User.objects.get(pk=id).delete()
		print("in the profile delete a")
		return redirect('register')
	else:
		return redirect('home')
	

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You can now login!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form':form})

@login_required
def edit_profile(request):
	user = request.user
	followers = user.profile.followers.all()
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_b_form = ProfileBioUpdateForm(request.POST, instance=request.user.profile)
		p_skill_form = ProfileSkillUpdateForm(request.POST, instance=request.user.profile)
		p_image_form = ProfileImageUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_b_form.is_valid():
			u_form.save()
			p_b_form.save()
			print("in the u_form first one")
			messages.success(request, f'Your account has been updated!')
			return redirect('my_profile')
		if 'p_img' in request.POST:
			print("before p_img if")
			if p_image_form.is_valid() :
				# u_form.save()
				request.user.profile.image= p_image_form.cleaned_data['image']
				p_image_form.save()
				request.user.profile.save()
				print("in the if p_image_form")
				messages.success(request, f'Your account has been updated!')
				return redirect('my_profile')

		if 'p_skill' in request.POST:
			if p_skill_form.is_valid() and p_skill_form.has_changed():
				# u_form.save()
				p_skill_form.save()
				print("in the if p_skill_form")
				messages.success(request, f'Your account has been updated!')
				return redirect('my_profile')
		
		if 'P_b' in request.POST:
			if p_b_form.is_valid() and p_b_form.has_changed():
				# u_form.save()
				p_b_form.save()
				print("in the if p_b_form")
				messages.success(request, f'Your account has been updated!')
				return redirect('my_profile')
		
		
		if 'u_form' in request.POST:
			if u_form.is_valid():
				# u_form.save()
				u_form.save()
				print("in the if u_form")
				messages.success(request, f'Your account has been updated!')
				return redirect('my_profile')
		
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_b_form = ProfileBioUpdateForm(instance=request.user.profile)
		p_skill_form = ProfileSkillUpdateForm(instance=request.user.profile)
		p_image_form = ProfileImageUpdateForm(instance=request.user.profile)
	context ={
		'u_form': u_form,
		'p_b_form': p_b_form,
		'p_skill_form':p_skill_form,
		'p_image_form':p_image_form,
		'u':user,
		'followers': followers,
	}
	return render(request, 'users/edit_profile.html', context)

@login_required
def my_profile(request):
	p = request.user.profile
	you = p.user
	post=[]
	sent_friend_requests = FriendRequest.objects.filter(from_user=you)
	rec_friend_requests = FriendRequest.objects.filter(to_user=you)
	user_posts = Post.objects.filter(user_name=you).order_by('-date_posted')
	print("user post ",user_posts)
	friends = p.friends.all()

	followings = p.followings.all()
	followers = p.followers.all()
	liked = [i for i in Post.objects.all() if Like.objects.filter(user = you, post=i)]
	print("liked :", liked)
	print("in my profile",p)
	print("following :",followings)
	print("followers :",followers)
	followed_post_img = []
	for img in user_posts:
		image = Images.objects.filter(post=img)
		followed_post_img.append(image)
		# print("images is ",image)	
	print("followed_post_img is :",followed_post_img)
	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.followers.all():
		button_status = 'Follow_the_user'
		print("button status:",button_status)

	else:
		button_status = 'unFollow_the_user'
		print("button status:",button_status)
		# if we have sent him a friend request
		# if len(FriendRequest.objects.filter(
		# 	from_user=request.user).filter(to_user=you)) == 1:
		# 		button_status = 'friend_request_sent'

		# if len(FriendRequest.objects.filter(
		# 	from_user=p.user).filter(to_user=request.user)) == 1:
		# 		button_status = 'friend_request_received'

	context = {
		'u': you,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
		'post_count': user_posts.count,
		'followers': followers,
		'followings': followings,
		'posts':user_posts,
		'followed_post_img':followed_post_img,
		'liked_post':liked
	}

	return render(request, "users/profile.html", context)

@login_required
def search_users(request):
	user = request.GET.get('q')
	object_list = User.objects.filter(username__icontains=user)
	
	context ={
		
		'users': object_list
	}
	return render(request, "users/search_users.html", context)

@login_required
def follow_request(request, id):
	user = get_object_or_404(User, id=id)
	# frequest, created = Following.objects.get_or_create(
	# 		from_user=request.user,
	# 		to_user=user)
	sender = request.user.profile
	receiver =user.profile
	sender.followings.add(receiver)
	receiver.followers.add(sender)
	f= UserFollowing.objects.filter(target=user)
	print("new candidate :",f)
	print("sender",sender)
	print("receiver",receiver)
	print("in the follow_request and user is :",user)
	# print("frequest",frequest)
	# return redirect(request.META['HTTP_REFERER'])
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))
	# redirect(request.META['HTTP_REFERER'])


@login_required
def un_follow_request(request, id):
	print("in the unfollow ")
	user = get_object_or_404(User, id=id)
	# frequest, created = Following.objects.get_or_create(
	# 		from_user=request.user,
	# 		to_user=user)
	sender = request.user.profile
	receiver =user.profile
	sender.followings.remove(receiver)
	receiver.followers.remove(sender)
	f= UserFollowing.objects.filter(target=user)
	print("new candidate :",f)
	print("sender",sender)
	print("receiver",receiver)
	print("in the follow_request and user is :",user)
	# print("frequest",frequest)
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))




def search_users_for_post(search):
	
	searched_users = User.objects.filter(username__icontains=search)

	
	return searched_users

@login_required
def follow_list(request):
	print("in the follow list")
	# user = get_object_or_404(User, id=id)
	# frequest, created = Following.objects.get_or_create(
	# 		from_user=request.user,
	# 		to_user=user)
	you = request.user.profile
	followers_list = you.followers.all()
	followings_list = you.followings.all()	
	print("followers_list is :",followers_list)
	print("following list is :",followings_list)
	# receiver =user.profile
	# sender.followings.remove(receiver)
	# receiver.followers.remove(sender)
	context = {
		'u': you,
		'followers_list': followers_list,
		'followings_list':followings_list,
	}

	return render(request, "users/followers_list.html", context)
