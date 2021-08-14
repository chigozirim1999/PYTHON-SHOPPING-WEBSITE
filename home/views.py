import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string

from home.models import Setting, ContactForm, \
    ContactMessage  # it seems that django/python does not understand src import

from product.models import Category, Product, Images, Comment, Variants

from product.models import Product

from home.forms import SearchForm

from product.models import Images

from product.models import Comment


def index(request):
    # defining some variable
    setting = Setting.objects.get(pk=1)  # imports our settings
    #category = Category.objects.all() it was removed after using category template tags (myapptags)
    products_slider = Product.objects.all().order_by('id')[:4]  # for ascandic displays first products, displays first four products
    # products_slider = Product.objects.all().order_by('-id')[:4] #for descandic ..... displays last four products
    products_latest = Product.objects.all().order_by('-id')[:4]  # displays last four products
    products_picked = Product.objects.all().order_by('?')[:4]  # displays random products
    page = "home"
    context = {
        'setting': setting,
        'page': page,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
        #'category': category it was removed after using category template tags (myapptags)
    }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)  # imports our settings
    context = {'setting': setting, }
    return render(request, 'about.html', context)


def contactus(request):
    # defining some variable
    # global context
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relationship with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has been sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
        # else:
    setting = Setting.objects.get(pk=1)  # imports our settings
    form = ContactForm
    context = {'setting': setting, 'form': form}
    return render(request, 'contactus.html', context)


def category_products(request, id, slug):
    #setting = Setting.objects.get(pk=1)
    #category = Category.objects.all() it was removed after using category template tags (myapptags)
    products = Product.objects.filter(category_id=id)
    catdata = Category.objects.filter(pk=id)
    context = {'products': products,
               #'category': category,  it was removed after using category template tags (myapptags)
               'catdata': catdata
               }
    return render(request, 'category_products.html', context)


def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)

            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {'products': products,
                       'query': query,
                       'category': category
                       }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            products_json = {}
            products_json = rs.title  # +" > " + rs.category.title
            results.append(products_json)
        data = json.dumps(results)
        # print(data) #just added this
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_detail(request, id, slug):
    # setting = Setting.objects.get(pk=1)
    query = request.GET.get('q')
    product = Product.objects.get(pk=id)
    category = Category.objects.all()
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'product': product,
               'category': category,
               'images': images,
               'comments': comments,
               }

    if product.variant != "None":  # Product have variants
        if request.method == 'POST':  # if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)  # selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title + ' Size:' + str(variant.size) + ' Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant, 'query': query
                        })
    return render(request, 'product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)
