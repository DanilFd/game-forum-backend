import datetime
from datetime import timedelta, date

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from users.models import CustomUser, UserUserRelation


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_img', 'login', 'date_joined', 'last_visit', 'birthday_date', 'discord', 'gender',
                  'about_custom_user', 'age', 'email', 'rate', 'rating']

    rate = SerializerMethodField()
    age = SerializerMethodField()
    birthday_date = serializers.DateField(format='%d.%m.%Y')

    def get_age(self, instance: CustomUser):
        if instance.birthday_date is None:
            return None
        return (date.today() - instance.birthday_date) // timedelta(days=365.2425)

    def get_rate(self, obj: CustomUser):
        if not self.context['request'].user.is_authenticated:
            return None
        found_rate = UserUserRelation.objects.filter(user1=obj, user2=self.context['request'].user).first()
        if found_rate is None:
            return None
        return found_rate.rate
