import random

from pytils.translit import slugify


# class SaveSlugMixin:
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#             while self.__class__.objects.filter(slug=slug).exists():
#                 slug += str(
#                     random.randint(0, (self.__class__.objects.count() + 1) * 100)
#                 )
#         super().save(*args, **kwargs)


class SaveSlugMixin:
    def save(self, *args, slug_field=None, slugify_field=None, **kwargs):
        if slug_field and slugify_field:
            slug = getattr(self, slug_field)
            slugify_value = getattr(self, slugify_field)
            if not slug:
                new_slug = slugify(slugify_value)
                setattr(self, slug_field, new_slug)
                while self.__class__.objects.filter(**{slug_field: new_slug}).exists():
                    setattr(
                        self,
                        slug_field,
                        new_slug
                        + str(
                            random.randint(
                                0, (self.__class__.objects.count() + 1) * 100
                            )
                        ),
                    )
        super().save(*args, **kwargs)
