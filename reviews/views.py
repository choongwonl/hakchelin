from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from reviews.models import CustomReview, CustomCheck
from menus.models import CustomMenu
from users.models import CustomUser
from django.utils.timezone import datetime
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F


def home(request):
    return render(request, 'reviews/home.html')

# def check(request):
#     print(datetime.today())
#     todaychecks = CustomCheck.objects.filter(date__date=datetime.today())
#     print(len(todaychecks))
#     todayme = todaychecks.filter(author=request.user.sid)
#     print(len(todayme))
#     if len(todayme) != 0:
#         return render(request, 'reviews/alreadycheck.html')
#     else:
#         CustomCheck(author = request.user.sid).save()
#         print(len(todayme))
#         print(len(todayme))
#         print(len(todayme))
#         return render(request, 'reviews/check.html')

def howtoearnpoint(request):
    return render(request, 'reviews/howtoearnpoint.html')

def lastreviews(request):
    now = datetime.now()
    nowDate = now.strftime('%Y%m%d')
    if request.GET.get('type') == 'all':
        reviews_all = CustomReview.objects.all()
        reviews_all_ord = reviews_all.order_by('-created')


        page = request.GET.get('page', 1)

        paginator = Paginator(reviews_all_ord, 20)
        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            reviews = paginator.page(1)
        except EmptyPage:
            reviews = paginator.page(paginator.num_pages)

        ctx = {'reviews' : reviews }

    else:
        return render(request, 'reviews/lastreviews.html', {'reviews':[]})

    return render(request, 'reviews/lastreviews.html' ,ctx)

def myreviews(request):
    my_reviews = CustomReview.objects.filter(author=request.user.sid)
    my_reviews_ord = my_reviews.order_by('-created')

    page = request.GET.get('page', 1)

    paginator = Paginator(my_reviews_ord, 20)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    ctx = {'reviews' : reviews }

    return render(request, 'reviews/myreviews.html' ,ctx)

def ranking(request):
    usr = CustomUser.objects.filter(is_staff=False)
    
    pointusr = usr.order_by('-point')
    usrs = []
    for i in range(len(pointusr)):
        usrs.append({'rank':i+1, 'lvl':pointusr[i].point//500,'name':pointusr[i].name, 'point':pointusr[i].point, 'review_count':pointusr[i].review_count})
    
    page = request.GET.get('page', 1)

    paginator = Paginator(usrs, 20)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'reviews/ranking.html', {'users':users})

def check(request):
    return render(request, 'reviews/check.html')

# @login_required
def today(request):

    if request.method == 'POST' and 'run_script' in request.POST:
        import crawler
        crawler.main()


    reviews = CustomReview.objects.all()
    # menus = CustomMenu.objects.all()
    menus = CustomMenu.objects.filter(date__date=datetime.today())
    stars = {}
    for menu in menus:
        star = []
        if menu.review_count != 0:
            rawnum = menu.star_count / menu.review_count
            num = round(rawnum, 2)
            if rawnum >= 5:
                star = [5,0,0]
            elif rawnum >= 4.5:
                star = [4,1,0]
            elif rawnum >= 4:
                star = [4,0,1]
            elif rawnum >= 3.5:
                star = [3,1,1]
            elif rawnum >= 3:
                star = [3,0,2]
            elif rawnum > 2.5:
                star = [2,1,2]
            elif rawnum >= 2:
                star = [2,0,3]
            elif rawnum > 1.5:
                star = [1,1,3]
            elif rawnum >= 1:
                star = [1,0,4]
            elif rawnum > 0.5:
                star = [0,1,4]
            elif rawnum >= 1:
                star = [0,0,5]
            star.append(num)
        else:
            star = [0,0,5,0]

        stars[menu.mid] = star

    menus = CustomMenu.objects.all().filter(date__date=datetime.today())

    starmenus = menus.order_by('-avg')

    haksang = menus.filter(location__exact='학생식당')
    kyogikwon = menus.filter(location__exact='교직원식당')
    sarang = menus.filter(location__exact='사랑방')
    newhaksang = menus.filter(location__exact='신학생식당')
    newkyogikwon = menus.filter(location__exact='신교직원식당')
    hangwon = menus.filter(location__exact='행원파크')
    onedorm = menus.filter(location__exact='제1생활관식당')
    twodorm = menus.filter(location__exact='제2생활관식당')

    return render(request, 'reviews/today.html', {
        'menus' : menus, 
        'stars' : stars, 
        'starmenus' : starmenus,
        'haksang' : haksang,
        'kyogikwon' : kyogikwon,
        'sarang' : sarang,
        'newhaksang' : newhaksang,
        'newkyogikwon' : newkyogikwon,
        'hangwon' : hangwon,
        'onedorm' : onedorm,
        'twodorm' : twodorm,
        })

class reviewCreateForm(forms.ModelForm):
    class Meta:
        model = CustomReview
        fields = ['star' ,'photo', 'comment']
        template_name = 'reviews/upload.html'

class ReviewUploadView(LoginRequiredMixin, CreateView):

    def get(self, request, *args, **kwargs):
        date = request.GET.get('date')
        res = request.GET.get('res')
        menunum = request.GET.get('menu')
        mid = date + res + menunum
        menu = CustomMenu.objects.get(mid=mid)
        
        print('[Review] '+ menu.title)
        context = {'form': reviewCreateForm() , 'menu' : menu}
        return render(request, 'reviews/upload.html', context)

    def post(self, request, *args, **kwargs):
        form = reviewCreateForm(request.POST)
        if request.FILES:
            form.instance.photo = request.FILES['photo']
            if request.FILES['photo']:
                CustomUser.objects.filter(sid = self.request.user.sid).update(point=F('point') + 50)
        form.instance.author_id = self.request.user.sid
        date = request.GET.get('date')
        res = request.GET.get('res')
        menunum = request.GET.get('menu')

        # first = request.GET.get('f')
        # if first == True:
        #     print('first')
        # else:
        #     print('no')
        mid = date + res + menunum
        if len(CustomReview.objects.filter(mid=mid)) == 0:
            CustomUser.objects.filter(sid = self.request.user.sid).update(point=F('point') + 150)
            ##CustomUser.save()
        else:
            CustomUser.objects.filter(sid = self.request.user.sid).update(point=F('point') + 100)
            ##CustomUser.save()

        CustomUser.objects.filter(sid = self.request.user.sid).update(review_count=F('review_count') + 1)
        form.instance.mid = CustomMenu.objects.get(mid=mid)
    

        if form.is_valid():
            form.instance.save()
            return redirect('/home/detail/?date='+date+'&res='+res+'&menu='+menunum)
        else:
            return render('reviews/upload.html', {'form':form})
            # return self.render_to_response({'form':form)

@login_required(login_url='/registration/login')
def detailView(request):
    date = request.GET.get('date')
    res = request.GET.get('res')
    menunum = request.GET.get('menu')

    mid = date + res + menunum
    params = [date, res, menunum]
    reviews = CustomReview.objects.filter(mid=mid)
    menu = CustomMenu.objects.get(mid=mid)
    print('[Detail] '+ menu.title)
    avg = menu.avg
    if int(avg) == avg:
        avg = int(avg)

    avg_star = []
    if avg >= 5:
        avg_star = [5,0,0]
    elif avg >= 4.5:
        avg_star = [4,1,0]
    elif avg >= 4:
        avg_star = [4,0,1]
    elif avg >= 3.5:
        avg_star = [3,1,1]
    elif avg >= 3:
        avg_star = [3,0,2]
    elif avg > 2.5:
        avg_star = [2,1,2]
    elif avg >= 2:
        avg_star = [2,0,3]
    elif avg > 1.5:
        avg_star = [1,1,3]
    elif avg >= 1:
        avg_star = [1,0,4]
    elif avg > 0.5:
        avg_star = [0,1,4]
    elif avg >= 0:
        avg_star = [0,0,5]

    return render(request, 'reviews/detail.html', {'reviews' : reviews, 'mid': mid, 'menu': menu, 'avg':avg, 'avg_star': avg_star, 'params' : params} )

@login_required(login_url='/registration/login')
def mypage(request):
    return render(request, 'reviews/mypage.html')


# def uploadView(request, mid):
#     return render(request, 'reviews/upload.html')