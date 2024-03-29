from rest_framework import serializers
from base.models import Place, UserFeature, PlaceDetails, Review, UserSavePlace, NgrokUrl
from django.contrib.auth import get_user_model, authenticate


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class NgrokSerializer(serializers.ModelSerializer):
	class Meta:
		model = NgrokUrl
		fields = '__all__'
		
class PlaceDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlaceDetails
		fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = '__all__'

class UserSavedPlaceSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserSavePlace
		fields = '__all__'

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = '__all__'
	def create(self, clean_data):
		user_obj = UserModel.objects.create_user(username=clean_data['username'], email=clean_data['email'], password=clean_data['password'])
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserModel
		fields = ('email', 'username')

class UserFeatureSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserFeature
		fields = '__all__'