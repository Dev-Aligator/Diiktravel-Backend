from rest_framework import serializers
from base.models import Place
from django.contrib.auth import get_user_model, authenticate


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
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

# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = '__all__'

# class BannerSerializer(serializers.ModelSerializer):
#     roles = RoleSerializer(many=True, read_only=True)  # Include the related roles

#     class Meta:
#         model = Banner
#         fields = '__all__'

# class SkillSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Skill
#         fields = '__all__'

# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = '__all__'

# class ContactSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = '__all__'