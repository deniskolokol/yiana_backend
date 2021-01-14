from django.db import models
from django.db.models.deletion import SET_NULL
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from wagtail.search import index
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


# Project-wide list of languages.
# Publications of any type (video, blog, etc.) are
# allowed only in following languages.
LANGS = {
    "pl": ("Polish", "Polski"),
    "en": ("English", "English"),
    "ru": ("Russian", "Русский"),
    "uk": ("Ukrainian", "Українська"),
}


class Topic(models.Model):
    """
    Topics are similar to 'Popular topics' in Facebook groups,
    but here they are language dependent.
    """
    lang = models.CharField(max_length=2, choices=LANGS)
    topic = models.CharField(_(u"Name"), max_length=255)

    @property
    def pubs_count(self):
        """Number of posts of a certain topic."""
        return 0 #TODO


class CollectionPage(Page):
    """Collection of posts."""
    pass


class PostPage(Page):
    """Single post in a collection."""
    lang = models.CharField(max_length=2, choices=LANGS)
    created_at = models.DateTimeField(editable=False, default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(editable=False, default=timezone.now)

    topic = models.ForeignKey(Topic, related_name='posts', on_delete=SET_NULL)
    annotation = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    body = RichTextField(blank=True)
    hashtags = ArrayField(models.CharField(), blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("annotation"),
        index.SearchField("description"),
        index.SearchField("body"),
        ]

    content_panels = Page.content_panels + [
        FieldPanel("created_at"),
        FieldPanel("annotation"),
        FieldPanel("description"),
        FieldPanel("body", classname="full"),
        ]

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
