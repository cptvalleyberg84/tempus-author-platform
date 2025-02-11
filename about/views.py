from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CollaborationForm


class AboutView(TemplateView):
    """
    View for handling the about page and collaboration request form.

    This view renders the about page template and processes collaboration
    request form submissions. It inherits from Django's TemplateView.
    """

    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        """
        Add the collaboration form to the template context.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = CollaborationForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for collaboration form submission.

        Validates the form data and saves it if valid. Redirects back to
        the about page with appropriate success or error messages.
        """
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
