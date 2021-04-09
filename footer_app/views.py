from django.shortcuts import render
from django.views import View


class AboutUsView(View):
    """
    Base class view to introduce our TEAM.
    """
    def get(self, request):
        return render(request, 'about_us.html')


class BrandingGuideView(View):
    """
    Base class view to branding guide.
    """
    def get(self, request):
        return render(request, 'Branding_Guide.html')


class RegulationsView(View):
    """
    Base class view to show the Regulation.
    """
    def get(self, request):
        return render(request, 'Regulations.html')


class GetCandyView(View):
    """
    Base class view to add daily bonus Coin for authenticated User.
    """
    def get(self, request):
        return render(request, 'GetCandy.html')
