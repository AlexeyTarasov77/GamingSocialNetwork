from gameshop.models import ProductProxy
from gameblog.redis_connection import r


class Recommender:
    """Recommender system based on product purchase history."""
    def get_product_key(self, id):
        return f"product:{id}:purchased_with"

    def products_bought(self, products):
        """
        Save products that were bought together with the given products.
        Invokes after successful purchase.
        """
        assert products, "No products specified"
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                if product_id != with_id:
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_result=6):
        """Suggest top N products that were most often bought together with the given products."""
        assert products, "No products specified"
        product_ids = [p.id for p in products]
        # если продукт всего 1 - просто возвращаем элемементы находящиеся в его множестве
        if len(products) == 1:
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True
            )[:max_result]
        else:
            # создаем временный ключ для хранения рекомендуемых продуктов для всех переданных products
            tmp_key = "products:tmp"
            # список ключей множеств для каждого переданного продукта
            keys = [self.get_product_key(id) for id in product_ids]
            # обьединение полученных множеств и сохранение результат во временное множество
            r.zunionstore(tmp_key, keys)
            # удаляем из временного множества id переданных продуктов что бы избежать рекомендации самих себя
            r.zrem(tmp_key, *product_ids)
            # получаем список рекомендуемых продуктов в порядке убывания
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_result]
            # удаляем временное множество после того как оно стало не нужным
            r.delete(tmp_key)
        # конвертруем полученные id в int
        suggested_products_ids = [int(id) for id in suggestions]
        # получаем соответствующие продукты
        suggested_products = list(
            ProductProxy.objects.filter(id__in=suggested_products_ids)
        )
        # сортировка рекомендуемых продуктов согласно порядку их нахождения в suggested_products_ids
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_suggestions(self):
        for id in ProductProxy.objects.values_list("id", flat=True):
            r.delete(self.get_product_key(id))
