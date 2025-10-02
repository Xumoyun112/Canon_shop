from django.core.management.base import BaseCommand
from product.models import Speska
from django.utils.timezone import now
import csv
import os

class Command(BaseCommand):
    help = "Har kuni sotuvlarni faylga eksport qiladi"

    def handle(self, *args, **kwargs):
        today = now().date()
        filename = f"daily_sales_{today}.csv"
        filepath = os.path.join("exports", filename)

        os.makedirs("exports", exist_ok=True)

        speskas = Speska.objects.filter(date=today)

        daily_total = 0

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([f"{today} sanasi uchun kunlik savdo hisobot"])
            writer.writerow([])

            for speska in speskas:
                writer.writerow([f"Speska ID: {speska.id}", f"Sana: {speska.date}", f"Foydalanuvchi: {speska.user.username}"])
                writer.writerow(["Mahsulot", "Soni", "Narx", "Umumiy"])

                speska_total = 0
                for sale in speska.sales.all():
                    writer.writerow([sale.product.name, sale.quantity, sale.price, sale.total_price])
                    speska_total += sale.total_price

                writer.writerow(["", "", "Speska jami:", speska_total])
                writer.writerow([])

                daily_total += speska_total

            writer.writerow([])
            writer.writerow(["Kunlik jami savdo:", daily_total])

        self.stdout.write(self.style.SUCCESS(f"Kunlik sotuvlar saqlandi: {filepath}"))
