from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View



class ApplicationsTrackingView(View):
    template_name = "tracking/applications_tracking.html"

    def get(self, request):
        context = {
        }
        return render(request, self.template_name, context)
