from rest_framework.serializers import ModelSerializer

from card_module.models.WordCard import WordCard, RootExplain, WordUsage


class RootExplainModelSerializer(ModelSerializer):
    class Meta:
        model = RootExplain
        fields = '__all__'


class WordUsageModelSerializer(ModelSerializer):
    class Meta:
        model = WordUsage
        fields = '__all__'
        read_only_fields = ('word_card',)


class WordCardModelSerializer(ModelSerializer):
    root_explains = RootExplainModelSerializer(many=True)
    word_usages = WordUsageModelSerializer(many=True)
    class Meta:
        model = WordCard
        fields = '__all__'
        read_only_fields = ("create_time", "update_time")
