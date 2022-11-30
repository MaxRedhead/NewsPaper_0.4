from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum("rating"))
        pRat = 0
        pRat += postRat.get("postRating")

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum("rating"))
        cRat = 0
        cRat += commentRat.get("commentRating")

        self.authorRating = pRat*3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ARTICLE = "AR"
    NEWS = "NW"
    CATEGORY_CHOICES = (
        (ARTICLE, "Статья"),
        (NEWS, "Новость")
    )

    categoryTypes = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=256)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + "..."

    def __str__(self):
        return f'{self.categoryTypes.title()}: {self.title[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.title()


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
