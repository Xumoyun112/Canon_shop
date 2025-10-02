$(document).ready(function() {
    $(".product-select").select2({
        placeholder: "Mahsulotni qidiring...",
        allowClear: true
    });

    // Mahsulot tanlanganda
    $(".product-select").on("select2:select", function (e) {
        let productId = $(this).val();

        // Shu formadagi elementlarni topamiz
        let priceField = $(this).closest("form").find(".product_price");
        let stockField = $(this).closest("form").find(".product_stock");

        if (productId) {
            fetch(`/products/${productId}/json/`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        priceField.text("Xatolik: " + data.error);
                        stockField.text("");
                    } else {
                        priceField.text("Narx: " + data.price + " usd");
                        stockField.text("Sklad: " + data.stock + " dona");
                    }
                })
                .catch(error => {
                    priceField.text("Serverdan ma’lumot olinmadi!");
                    stockField.text("");
                    console.error("Fetch error:", error);
                });
        }
    });

    // Tozalanganda
    $(".product-select").on("select2:clear", function (e) {
        let priceField = $(this).closest("form").find(".product_price");
        let stockField = $(this).closest("form").find(".product_stock");

        priceField.text("");
        stockField.text("");
    });
});
