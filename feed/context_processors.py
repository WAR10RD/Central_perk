
from users.models import Profile
from django.db.models import Count

def whoToFollowFun(request):
	whoToFollow = Profile.objects.annotate(count=Count('followers')).order_by('-count')[:6]
	print("in who to follow :",whoToFollow)
	
	return{
        'whoToFollow':whoToFollow
    }
