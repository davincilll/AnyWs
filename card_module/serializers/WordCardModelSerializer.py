from rest_framework.serializers import ModelSerializer

from card_module.models.WordCard import WordCard, RootExplain, PhraseUsingThisVocabulary


class RootExplainModelSerializer(ModelSerializer):
    class Meta:
        model = RootExplain
        # fields = '__all__'
        exclude = ('user', 'word_card')


class PhraseUsingThisVocabularyModelSerializer(ModelSerializer):
    class Meta:
        model = PhraseUsingThisVocabulary
        # fields = '__all__'
        exclude = ('user', 'word_card')
        read_only_fields = ('word_card',)


class WordCardModelSerializer(ModelSerializer):
    root_explains = RootExplainModelSerializer(many=True)
    phrases_using_this_vocabulary = PhraseUsingThisVocabularyModelSerializer(many=True)

    class Meta:
        model = WordCard
        # fields = '__all__'
        exclude = ('user',)
        read_only_fields = ("create_time", "update_time")
