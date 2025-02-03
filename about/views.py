from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CollaborationForm


class AboutView(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CollaborationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CollaborationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Thank you for your collaboration request! '
                'We will get back to you soon.'
            )
            return redirect('about')

        else:
            messages.error(request, 'Please correct the errors below.')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
