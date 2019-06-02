from django.db import models
from django.urls import reverse
from django.db.models import F
from reviews.models import CustomReview

from django.db.models.signals import pre_save
from django.dispatch import receiver



class CustomMenu(models.Model):
    mid = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=100)
    photo = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    review_count = models.IntegerField(default=0)
    star_count = models.IntegerField(default=0)
    avg = models.FloatField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.mid)

    def get_average(self):
        if self.review_count != 0:
            self.avg =  round(self.star_count / self.review_count ,2)
        else:
            self.avg = 0
        
    def get_date(self):
        return str(self.mid)[:-2]

    def get_date_str(self):
        return str(self.mid)[:4] + '/' + str(self.mid)[4:6] + '/' + str(self.mid)[6:-2]

    def get_res(self):
        return str(self.mid)[-2]

    def get_menunum(self):
        return str(self.mid)[-1]
    class Meta:
        verbose_name = "menu"
        verbose_name_plural = "menus"

    def save(self, *args, **kwargs):
        self.get_average()   

        super(CustomMenu, self).save(*args, **kwargs)

    # @receiver(signals.post_save, sender=CustomReview)
    # def get_review_count(sender, instance, created, *args, **kwargs):
    #     print('idk....')
    @receiver(pre_save, sender=CustomReview, dispatch_uid="update_review_count")
    def update_review_count(sender, **kwargs):
        review = kwargs['instance']
        if not review.pk:
            CustomMenu.objects.filter(pk=review.mid.mid).update(review_count=F('review_count')+1)
            CustomMenu.objects.filter(pk=review.mid.mid).update(star_count=F('star_count') + review.star)
            star_temp = CustomMenu.objects.get(pk=review.mid.mid).star_count
            review_temp = CustomMenu.objects.get(pk=review.mid.mid).review_count
            avg_temp = round(star_temp/review_temp,2)
            CustomMenu.objects.filter(pk=review.mid.mid).update(avg=avg_temp)