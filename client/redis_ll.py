```
>>> from rediscluster import RedisCluster

>>> # Requires at least one node for cluster discovery. Multiple nodes is recommended.
>>> startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]

>>> # Note: See note on Python 3 for decode_responses behaviour
>>> rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

>>> rc.set("foo", "bar")
True
>>> print(rc.get("foo"))
'bar'
```

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    requests_cache.backends.redis
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ``redis`` cache backend
"""
from .base import BaseCache
from .storage.redisdict import RedisDict
class RedisCache(BaseCache):
    """ ``redis`` cache backend.
    """
    def __init__(self, namespace='requests-cache', **options):
        """
        :param namespace: redis namespace (default: ``'requests-cache'``)
        :param connection: (optional) ``redis.StrictRedis``
        """
        super(RedisCache, self).__init__(**options)
        self.responses = RedisDict(namespace, 'responses',
                                   options.get('connection'))
        self.keys_map = RedisDict(namespace, 'urls', self.responses.connection)
