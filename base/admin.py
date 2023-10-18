from django.contrib import admin
from .models import Place, UserFeature, PlaceDetails, Review, UserSavePlace, NgrokUrl

admin.site.register(Place)
admin.site.register(UserFeature)
admin.site.register(PlaceDetails)
admin.site.register(Review)
admin.site.register(UserSavePlace)
admin.site.register(NgrokUrl)

