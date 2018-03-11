from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import Todo

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name',
                  'is_active', 'links',)

    def get_links(self, obj):
        request = self.context['request']
        username = obj.get_username()
        links = {
            'self': reverse('user-detail', kwargs={
                User.USERNAME_FIELD: username}, request=request),
        }
        return links


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    links = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ('id', 'title', 'owner', 'links', 'created')

    def get_links(self, obj):
        request = self.context['request']
        links = []
        if hasattr(obj, 'pk'):
            links = {
                'self': reverse('todo-detail',
                                kwargs={'pk': obj.pk}, request=request),
                'owner': obj.owner,
                }
            if obj.owner:
                links['owner'] = reverse('user-detail', kwargs={
                    User.USERNAME_FIELD: obj.owner}, request=request)
        return links
