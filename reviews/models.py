from django.db import models
from django.db.models import F
from django.urls import reverse
# from menus.models import CustomMenu

class CustomCheck(models.Model):
    cid = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='user_check')

    class Meta:
        ordering = ['-created']
        verbose_name = "check"
        verbose_name_plural = "checks"

    def __str__(self):
        return '[check] ' + self.created.strftime("%Y-%m-%d") + ' ' + self.author.sid

class CustomReview(models.Model):
    rid = models.AutoField(primary_key=True)
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='user_reviews')
    photo = models.ImageField(upload_to='reviewPhotos/%Y/%m/%d', default='photos/no_image.png')
    comment = models.TextField()
    star = models.IntegerField(default=0)
    mid = models.ForeignKey('menus.CustomMenu', on_delete=models.CASCADE, related_name='menu_reviews')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']
        verbose_name = "review"
        verbose_name_plural = "reviews"

    def __str__(self):
        return self.author.sid + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_absolute_url(self):
        return reverse('review:review_detail', args=[str(self.id)])
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         CustomMenu.objects.filter(pk=self.mid.mid).update(review_count=F('review_count')+1)
    #         CustomMenu.objects.filter(pk=self.mid.mid).update(star_count=F('star_count') + self.star)
    #         CustomMenu.get_average()
    #     super().save(*args, **kwargs)