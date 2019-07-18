from haystack import indexes
from .models import Profile


# 类名必须为需要检索的Model_name + Index
class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  # 创建一个text字段
    user = indexes.CharField(model_attr='user')
    profile = indexes.CharField(model_attr='profile', null=True)

    def get_model(self):
        return Profile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
