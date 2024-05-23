from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from payment import webhooks

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('rosetta/', include('rosetta.urls')),
    path("accounts/", include("allauth.urls")),
    path("", include("gameblog.urls", namespace="gameblog")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("payment/", include("payment.urls", namespace="payment")),
    path("coupons/", include("coupons.urls", namespace="coupons")),
    path("shop/", include("gameshop.urls", namespace="shop")),
    # path('articles/', include('articles.urls', namespace='articles')),
    # path('chat/', include('chat.urls', namespace='chat')),
    # path('events/', include('events.urls', namespace='events')),
    path("posts/", include("posts.urls", namespace="posts")),
    path('teams/', include('gameteams.urls', namespace='teams')),
    path("users/", include("users.urls", namespace="users")),
)

urlpatterns += [
    path('stripe/webhook/', webhooks.stripe_webhook, name='stripe_webhook'),
    path("api/", include("api.urls", namespace="api")),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
