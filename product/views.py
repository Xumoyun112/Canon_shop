from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .models import Speska, Sale
from .forms import SaleForm, ProductForm
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.utils.timezone import now

@login_required
def speska_list(request):
    speska_list = Speska.objects.order_by("-date", "-id")
    return render(request, "product/speska_list.html", {"speskas": speska_list})

@login_required
def speska_create(request):
    speska = Speska.objects.create(date=now().date(),
                                   user=request.user)
    return redirect("speska_detail", speska_id=speska.id)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import SaleForm


@login_required
def speska_detail(request, speska_id=None):
    speska = None
    if speska_id:
        speska = get_object_or_404(Speska, id=speska_id, user=request.user)

    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            # Agar eski speska bo‘lmasa, yangisini yaratamiz
            if speska is None:
                speska = Speska.objects.create(user=request.user)

            sale = form.save(commit=False)
            sale.speska = speska
            sale.save()

            return redirect("speska_detail", speska_id=speska.id)
    else:
        form = SaleForm()

    return render(
        request,
        "product/speska_detail.html",
        {"speska": speska, "form": form}
    )


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "product/product_list.html", {"products": products})

from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils.timezone import now
from .models import Speska, Sale

@login_required
def reports(request):
    today = now().date()
    month = today.month
    year = today.year

    # Total_price ni annotate orqali hisoblab olish
    daily_total = Sale.objects.filter(speska__date=today).annotate(
        total_price=ExpressionWrapper(F("quantity") * F("product__price"), output_field=DecimalField())
    ).aggregate(total=Sum("total_price"))["total"] or 0

    monthly_total = Sale.objects.filter(speska__date__month=month, speska__date__year=year).annotate(
        total_price=ExpressionWrapper(F("quantity") * F("product__price"), output_field=DecimalField())
    ).aggregate(total=Sum("total_price"))["total"] or 0

    yearly_total = Sale.objects.filter(speska__date__year=year).annotate(
        total_price=ExpressionWrapper(F("quantity") * F("product__price"), output_field=DecimalField())
    ).aggregate(total=Sum("total_price"))["total"] or 0

    return render(request, "product/reports.html", {
        "daily_total": daily_total,
        "monthly_total": monthly_total,
        "yearly_total": yearly_total,
    })


@login_required
def sale_create(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)

            # Avval Speska yaratamiz (agar mavjud bo‘lmasa)
            speska = Speska.objects.create(user=request.user)
            sale.speska = speska

            # Mahsulot narxini avtomatik olish
            sale.price = sale.product.price

            # Skladni tekshirish
            if sale.quantity > sale.product.stock:
                messages.error(request, "Skladda yetarli mahsulot yo‘q!")
                return redirect("sale_create")

            # Skladni kamaytirish
            sale.product.stock -= sale.quantity
            sale.product.save()

            sale.save()
            return redirect("speska_list")
    else:
        form = SaleForm()
    return render(request, "product/sale_form.html", {"form": form})

@login_required
def product_detail_json(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        return JsonResponse({
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "stock": product.stock,
        })
    except Product.DoesNotExist:
        return JsonResponse({"error": "Mahsulot topilmadi"}, status=404)

@login_required
def delete_sale(request, speska_id, sale_id):
    speska = get_object_or_404(Speska, id=speska_id)
    sale = get_object_or_404(Sale, id=sale_id, speska=speska)

    if request.method == "POST":
        # o‘chirishdan oldin stockni qaytarish
        sale.product.stock += sale.quantity
        sale.product.save()
        sale.delete()
        messages.success(request, "Mahsulot o‘chirildi!")
        return redirect("speska_detail", speska_id=speska.id)

    return redirect("speska_detail", speska_id=speska.id)

@login_required
def finalize_speska(request, speska_id):
    speska = get_object_or_404(Speska, id=speska_id)
    speska.is_finalized = True
    speska.save()
    messages.success(request, "Speska muvaffaqiyatli saqlandi va endi o‘zgartirib bo‘lmaydi!")
    return redirect("speska_detail", speska_id=speska.id)

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangi mahsulot muvaffaqiyatli qo‘shildi ✅")
            return redirect("product_list")  # yoki chiqim sahifasiga qaytarasiz
    else:
        form = ProductForm()
    return render(request, "product/add_product.html", {"form": form})
