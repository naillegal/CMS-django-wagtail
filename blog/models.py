from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel,InlinePanel
from wagtail.snippets.models import register_snippet
from taggit.models import Tag as TaggitTag
from modelcluster.models import ParentalKey
from taggit.models import TaggedItemBase
from modelcluster.tags import ClusterTaggableManager
# from .block import Body_block
from wagtail.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
import datetime
from django.http import Http404
from django.utils.functional import cached_property
from wagtail.search import index
from wagtail.contrib.forms.models import AbstractForm,AbstractFormField
from wagtailmetadata.models import MetadataPageMixin
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")

class FormPage(AbstractForm):
    content_panels = AbstractForm.content_panels + [
        InlinePanel("form_fields", label="Field Form")
    ]
    @cached_property
    def blogpage(self):
        return self.get_parent().specific
    
    def get_context(self, request, *args, **kwargs):
        context = super(FormPage, self).get_context(request, *args, **kwargs)
        context ["blogpage"] = self.blogpage
        return context

class Blogpage(RoutablePageMixin, Page):
    description = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request,*args,**kwargs)
        context["blogpage"] = self
        paginator = Paginator(self.posts, 2)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.object_list.none()
        context["posts"] = posts
        return context
    
    def get_posts(self):
        return PostPage.objects.descendant_of(self).live().order_by("-post_date")
    
    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def post_by_date(self,request,year,month=None, day=None, *args, **kwargs):
        self.posts = self.get_posts().filter(post_date___year = year)

        if month:
            self.posts = self.posts.filter(post_date__month = month)
        if day:
            self.posts = self.posts.filter(post_date__day = day)

        return self.render(request)
    
    @route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    def post_by_date_slug(self,request,year,month,day,slug,*args,**kwargs):
        postpage = self.get_posts().filter(slug=slug).first()
        if not postpage:
            raise Http404
        return postpage.serve(request)

    
    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag):
        self.filter_term = tag
        self.filter_type = "tag"
        self.posts = self.get_posts().filter(tags__slug = tag)
        return self.render(request)
    
    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category):
        self.filter_term = category
        self.filter_type = "category"
        self.posts = self.get_posts().filter(categories__blog_category__slug = category)
        return self.render(request)
    
    @route(r'^$')
    def post_list(self,request):
        self.posts = self.get_posts()
        return self.render(request)

    @route(r'^search/$')
    def post_search(self,request):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.filter_term = search_query
            self.filter_type = "search"
            self.posts = self.posts.search(search_query)
        return self.render(request)
    

class PostPage(MetadataPageMixin, Page):
    header_image = models.ImageField(upload_to='blog_images/')
    tags = ClusterTaggableManager(through="PostPageTags",blank=True)
    # body = StreamField(Body_block(), blank=True)
    paragraph = models.TextField(blank=True,null=True)
    image_text_caption1 = models.CharField(max_length=50,null=True, blank=True)
    image_text_1 = models.ImageField(null=True, blank=True, upload_to='blog_images/')
    image_text_caption2 = models.CharField(max_length=50,null=True, blank=True)
    image_text_2 = models.ImageField(null=True, blank=True, upload_to='blog_images/')
    quotes = models.TextField(blank=True, null=True)
    quotes_by = models.CharField(max_length=100,null=True,blank=True)
    author = models.CharField(max_length=50, blank=True)
    file = models.FileField(upload_to='blog_files/', blank=True)
    post_date = models.DateTimeField(verbose_name="post date", default=datetime.datetime.today)
    content_panels = Page.content_panels + [
        FieldPanel("header_image"),
        FieldPanel("tags"),
        # FieldPanel("body"),
        FieldPanel("paragraph"),
        FieldPanel("image_text_caption1"),
        FieldPanel("image_text_1"),
        FieldPanel("image_text_caption2"),
        FieldPanel("image_text_2"),
        FieldPanel("quotes"),
        FieldPanel("quotes_by"),
        FieldPanel("author"),
        FieldPanel("file"),
        InlinePanel("categories",label="category"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel("post_date"),
    ]
    search_fields = Page.search_fields + [
        # index.SearchField("body"),
        index.SearchField("title"),
    ]

    def get_context(self,request,*args,**kwargs):
        context = super().get_context(request,*args,**kwargs)
        context["blogpage"] = self.blogpage
        return context
    
    @cached_property
    def blogpage(self):
        return self.get_parent().specific
    
    @cached_property
    def canonical_url(self):
        from .templatetags.blogapp_tags import post_page_date_slug_url
        blogpage = self.blogpage
        return post_page_date_slug_url(self,blogpage)
    


class PostPageBlogCategory(models.Model):
    Page = ParentalKey("blog.PostPage", on_delete=models.CASCADE,blank=True,related_name="categories")
    blog_category = models.ForeignKey("BlogCategory",blank=True,on_delete=models.CASCADE,related_name="post_pages")

    panels = [
        FieldPanel("blog_category")
    ]
    class Meta:
        unique_together = ("Page","blog_category")

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=250,blank=True)
    slug = models.SlugField(max_length=80, unique=True)

    panels = [  
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class PostPageTags(TaggedItemBase):
    content_object = ParentalKey("blog.PostPage",blank=True)

@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True