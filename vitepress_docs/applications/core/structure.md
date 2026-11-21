---
layout: doc
outline: [2, 3]
---

This page lists the sturcture of core application, and the files used to build it.

[[toc]]


## Utils

* We start by a very useful utility function that will be used in many actions in the project, it's main functionality is to remove some special characters, trim/strip white spaces from text and save strings data in lower-case.

This is useful becuase we need to make sure that the data (facility name for hospitals, and name for schools and libraries) are unique.

```python
from django.utils.encoding import force_str
import unicodedata
import re

def normalize_text(text):
    """Full normalization for uniqueness. Writen with help from Grok AI"""
    text = force_str(text or "") # Source: https://docs.djangoproject.com/en/6.0/ref/utils/#django.utils.encoding.force_str
    text = unicodedata.normalize("NFKD", text).lower() # Lower-case text then emove accents ("café" to "cafe") Source: https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize
    text = re.sub(r"[^a-z0-9\s\-\/]", "", text) # Accept only A to Z + 0 to 9 and dash ( - ) + forward slash ( / )
    # Collapse multiple whitespace into single space and strip
    return " ".join(text.split())
```

* The second util is a Test class that will be used in a lot of test classes, and its main action is to declare a `url_name` for test classes and allow tests to perform authenticated requests by creating and authenticating a test user. This is added recently after securing applications behind authentication.

```python
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AuthenticatedTestCase(TestCase):
    url_name = None

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword123",
        )

    def setUp(self):
        self.client.force_login(self.user)

        if self.url_name is not None:
            self.url = reverse(self.url_name)
```