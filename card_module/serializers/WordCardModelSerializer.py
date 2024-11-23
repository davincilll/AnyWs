from rest_framework.serializers import ModelSerializer

from card_module.models.WordCard import WordCard, RootExplain, UsefulPhraseUsingThisVocabulary


class RootExplainModelSerializer(ModelSerializer):
    class Meta:
        model = RootExplain
        # fields = '__all__'
        exclude = ('user', 'word_card')


class UsefulPhraseUsingThisVocabularyModelSerializer(ModelSerializer):
    class Meta:
        model = UsefulPhraseUsingThisVocabulary
        # fields = '__all__'
        exclude = ('user', 'word_card')
        read_only_fields = ('word_card',)


class WordCardModelSerializer(ModelSerializer):
    root_explains = RootExplainModelSerializer(many=True,required=False)
    useful_phrases_phrases_using_this_vocabulary = UsefulPhraseUsingThisVocabularyModelSerializer(many=True,required=False)

    class Meta:
        model = WordCard
        # fields = '__all__'
        exclude = ('user',)
        read_only_fields = ("create_time", "update_time")


class WordCardSchema(ModelSerializer):
    root_explains = RootExplainModelSerializer(many=True)
    useful_phrases_phrases_using_this_vocabulary = UsefulPhraseUsingThisVocabularyModelSerializer(many=True)

    class Meta:
        model = WordCard
        # fields = '__all__'
        exclude = ('user','remark_of_user')
        read_only_fields = ("create_time", "update_time")
