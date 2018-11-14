Title: Combining Disparate QuerySets in Django
Slug: combining-disparate-querysets-in-django
Date: 2016-2-4 16:00
Tags: django
Author: Patrick Cloke

> Note: This was originally posted on the [Strongarm Blog](https://strongarm.io/blog/combining-disparate-querysets-in-django/).

While refactoring [strongarm.io](https://strongarm.io) we ran into a problem: we
had different database tables that we needed to query over as if they were a
single database table. We use [Django](https://www.djangoproject.com/) as an
[ORM](https://en.wikipedia.org/wiki/Object-relational_mapping) and needed to
stay within the ORM in order to leverage third-party libraries.

Our two models have overlapping fields, in this instance both had a `name` field
to search over and a `created` field to order on. A naive implementation might
serialize all the data to memory and come up with implementations like:

```python
# Consider ModelA and ModelB to exist somewhere, both have a name (CharField)
# and created (DateTimeField).

from itertools import chain

# Sorted data.
sorted_data = sorted(
    chain(
        ModelA.objects.order_by('-created'),
        ModelB.objects.order_by('-created'),
    ),
    key=lambda instance: instance.date,
    reverse=True)

# Search for a particular result.
result = None
try:
    result = ModelA.objects.get(name='foo')
except ModelA.DoesNotExist:
    try:
        result = ModelB.objects.get(name='foo')
    except ModelB.DoesNotExist:
        pass

# Look at a subset.
subset_data = (list(ModelA.objects.filter(name__contains='foo')) +
               list(ModelB.objects.filter(name__contains='foo')))
```

This has two issues we had to overcome:

1.  We had too much data to serialize to memory.
2.  We needed to pass the result into Django APIs that expected a `QuerySet`.

Enter [Django QuerySetSequence](https://github.com/percipient/django-querysetsequence)!
We built Django QuerySetSequence (based on some previously available code) to
provide the following:

1.  Provide a `QuerySet` API that operates over multiple `QuerySets` generated
    from different `Model` classes.
2.  Evaluate each `QuerySet` lazily (i.e. as late as possible).
3.  High quality code with tests.
4.  Guard against calling untested methods.

This allows much more Django-esque code:

```python
# Consider ModelA and ModelB to exist somewhere, both have a name (CharField)
# and created (DateTimeField).
from django.core.exceptions import ObjectDoesNotExist

from queryset_sequence import QuerySetSequence

queryset = QuerySetSequence(ModelA.objects.all(), ModelB.objects.all())

# Sorted data.
sorted_data = queryset.order_by('-created')

# Search for a particular result:
try:
    result = queryset.get(name='foo')
except ObjectDoesNotExist:
    result = None

# Look at a subset.
subset_data = queryset.filter(name__contains='foo')
```

Currently Django QuerySetSequence supports both Django 1.8 and Django 1.9 on
Python 2.7, 3.4 and 3.5. Check out the full set of features or contribute to the
[source repository](https://github.com/percipient/django-querysetsequence). You
can install `django-querysetsequence` package from
[pypi](https://pypi.python.org/pypi/django-querysetsequence) using pip:

```
pip install django-querysetsequence
```

If you're using Django QuerySetSequence we'd love to
[hear about it](mailto:support@strongarm.io)!
