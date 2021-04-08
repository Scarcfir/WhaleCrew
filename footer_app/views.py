from django.shortcuts import render
from django.views import View


class AboutUsView(View):

    def get(self, request):
        return render(request, 'about_us.html')


class BrandingGuideView(View):

    def get(self, request):
        return render(request, 'Branding_Guide.html')


class RegulationsView(View):

    def get(self, request):
        return render(request, 'Regulations.html')


class GetCandyView(View):

    def get(self, request):
        return render(request, 'GetCandy.html')
