import csv

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from dashboard.forms import ImageCategoryForm

from dashboard.models import Image, ImageCategory


class ImageCategoriesView(View):
    '''Course categories view'''
    template = 'dashboard/pages/image_categories.html'

    def get(self, request):
        query = request.GET.get('query')
        categories = ImageCategory.objects.all().order_by('-id')
        if query:
            categories = ImageCategory.objects.filter(
                Q(name__icontains=query)
            ).order_by('-id')
        context ={
            'categories': categories
        }
        return render(request, self.template, context)
    

class CreateUpdateImageCategoryView(View):
    '''Create and update course category view'''
    template = 'dashboard/pages/create-update-image-category.html'

    def get(self, request):
        category_id = request.GET.get('category_id')
        category = None
        if category_id:
            category = ImageCategory.objects.filter(id=category_id).first()
        context = {
            'category': category
        }
        return render(request, self.template, context)
    
    def post(self, request):
        category_id = request.POST.get('category_id')
        category = None
        if category_id:
            category = ImageCategory.objects.filter(id=category_id).first()
        form = ImageCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            if category is None:
                messages.success(request, 'Category Created Successfully.')
                return redirect('dashboard:img_category')
            messages.success(request, 'Category Updated Successfully.')
            return redirect('dashboard:img_category')
        else:
            for k, v in form.errors.items():
                messages.error(request, f"{k}: {v}")
                return redirect('dashboard:img_category')
    

class ImagesView(View):
    template = 'dashboard/pages/images.html'

    def get(self, request):
        images = Image.objects.all().order_by('-id')
        query = request.GET.get('query')
        if query:
            images = Image.objects.filter(
                Q(category__name__icontains=query)
            ).order_by('-id')
        context ={
            'images': images
        }
        return render(request, self.template, context)
    

class AddImages(View):
    template = 'dashboard/pages/add-images.html'

    def get(self, request):
        categories = ImageCategory.objects.all().order_by('-id')

        context ={
            'categories': categories
        }
        return render(request, self.template, context)
    
    def post(self, request):
        category_id = request.POST.get('category_id')
        category = None
        tobe_saved = []
        if category_id:
            category = ImageCategory.objects.filter(id=category_id).first()
            if not category:
                messages.error(request, 'Category Does Not Exist.')
                return redirect('dashboard:images')
            images = request.FILES.getlist('images')
            for image in images:
                tobe_saved.append(Image(category=category, image=image))
            Image.objects.bulk_create(tobe_saved)
            messages.success(request, 'Images Added Successfully.')
            return redirect('dashboard:images')
        messages.error(request, 'Something went wrong.')
        return redirect('dashboard:images')
    
class DeleteImageCategoryView(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        category = ImageCategory.objects.filter(id=category_id).first()
        if category:
            category.delete()
            messages.success(request, 'Category Deleted Successfully.')
            return redirect('dashboard:img_category')
        messages.error(request, 'Category Does Not Exist.')
        return redirect('dashboard:img_category')
    
class DeleteImageView(View):
    def get(self, request):
        image_id = request.GET.get('image_id')
        image = Image.objects.filter(id=image_id).first()
        if image:
            image.delete()
            messages.success(request, 'Image Deleted Successfully.')
            return redirect('dashboard:images')
        messages.error(request, 'Image Does Not Exist.')
        return redirect('dashboard:images')