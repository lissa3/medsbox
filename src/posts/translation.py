from modeltranslation.translator import TranslationOptions, translator

from src.posts.models.post_model import Post


class PostTranslationOptions(TranslationOptions):
    fields = ("title", "content")


translator.register(Post, PostTranslationOptions)
