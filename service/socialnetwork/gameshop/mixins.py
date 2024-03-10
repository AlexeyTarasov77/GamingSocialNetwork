from django.utils.text import slugify
import random

class SaveModelMixin:
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug += random.randint(0, self.__class__.objects.count() * 100)
        super(self.__class__, self).save(*args, **kwargs)