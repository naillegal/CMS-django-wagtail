from django.shortcuts import render
from wagtail.admin import messages
from wagtail_modeladmin.views import DeleteView
from django.shortcuts import redirect
# Create your views here.

class CommentDeleteView(DeleteView):
    page_title = "delete comment"

    def post(self, request, *args, **kwargs):
        try:
            self.instance.delete()
            msg = f"{ self.verbose_name }'{self.instance}' deleted ."
            messages.success(request, msg)
            return redirect(self.index_url)
        except Exception as e:
            raise e