from django.db import models


class BaseModel(models.Model):
    """Base model to derive other models from.
    Implements base fields (created_at, updated_at) and __repr__ method which
    dinamically generates string representation.
    """
    repr_cols = ()
    repr_cols_num = 3

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        cols = []
        for i, field in enumerate(self._meta.fields):
            if i < self.repr_cols_num or field in self.repr_cols:
                cols.append(f"{field.name}={getattr(self, field.name)}")
        return f"<{self.__class__.__name__}({', '.join(cols)})>"
