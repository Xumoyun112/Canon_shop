from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    # faqat product app migratsiyalari tugaganda ishlasin
    if sender.name != "product":
        return

    # Guruhlarni yaratish
    group_input, _ = Group.objects.get_or_create(name="Kirish")
    group_sale, _ = Group.objects.get_or_create(name="Sotish")

    # Product va Sale modellari
    Product = apps.get_model("product", "Product")
    Sale = apps.get_model("product", "Sale")

    # Product uchun permissionlar
    can_add_product = Permission.objects.filter(codename="add_product").first()
    can_change_product = Permission.objects.filter(codename="change_product").first()

    # Sale uchun permissionlar
    can_add_sale = Permission.objects.filter(codename="add_sale").first()

    # Guruhlarga biriktirish (faqat mavjud bo‘lsa)
    if can_add_product and can_change_product:
        group_input.permissions.set([can_add_product, can_change_product])

    if can_add_sale:
        group_sale.permissions.set([can_add_sale])
