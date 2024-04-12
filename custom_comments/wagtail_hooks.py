from . import get_model as get_comment_model
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html, strip_tags
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .views import CommentDeleteView

class CommentAdmin(ModelAdmin):
    model = get_comment_model()
    menu_label = "comments"
    menu_icon = "doc-full-inverse"
    add_to_settings_menu = False
    delete_view_class = CommentDeleteView

    list_display = (
        "plain_text_comment",
        "name",
        "submit_date",
        "comment_page_type",
        "comment_page",
    )
    ordering = ("-submit_date",)

    search_fields = ("comment")
    list_per_page = 10

    form_fields_exclude = [
        "submit_date",
        "ip_address",
        "is_removed",
        "is_public",
        "user_url",
        "user",
        "content_type",
        "object_pk",
        "content_object",
        "site",
    ]

    def comment_page_type(self, obj):
        if obj.content_object:
            ct = ContentType.objects.get_for_model(obj.content_object)
            return ct.model_class().__name__
        return ""
    
    def comment_page(self, obj):
        if obj.content_object:
            return format_html(
                f"<a href = '{obj.content_object.specific.url}'>{obj.content_object.specific.title} </a>"
            )
        return ""
    
    def plain_text_comment(self, obj):
        return strip_tags(obj.comment)
    
    def is_visible(self, obj):
        from django.contrib.admin.templatetags.admin_list import _boolean_icon
        return _boolean_icon(not obj.is_removed())
    
modeladmin_register(CommentAdmin)

