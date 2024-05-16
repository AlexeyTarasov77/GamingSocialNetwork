import random

from pytils.translit import slugify


class SaveSlugMixin:
    """
    Mixin for save slug field in model
    """

    def save(self, *args, slug_field=None, slugify_value=None, **kwargs):
        """
        Save the object to the database.

        Args:
            slug_field (str): The name of the field which store the slug.
            slugify_value (str): The value to generate the slug from.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        if slug_field and slugify_value:
            slug = getattr(self, slug_field)
            if not slug:
                new_slug = slugify(slugify_value)
                setattr(self, slug_field, new_slug)
                while self.__class__.objects.filter(
                    **{slug_field + "__iexact": new_slug}
                ).exists():
                    new_slug += str(
                        random.randint(0, (self.__class__.objects.count() + 1) * 100)
                    )
                    setattr(self, slug_field, new_slug)
        super().save(*args, **kwargs)
