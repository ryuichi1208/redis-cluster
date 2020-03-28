import redis

redis_client = redis.Redis(host = '172.17.0.2', port = 6379)
redis_client.set('key1', 'value1')

assert redis_client.get('key1') == b'value1'
assert redis_client.get('key1').decode('utf-8') == 'value1'

redis_client.hmset('hash_key1', { 'member1': 'hash_value1', 'member2': 'hash_value2' })

assert redis_client.hget('hash_key1', 'member1') == b'hash_value1'
assert redis_client.hgetall('hash_key1') == { b'member1': b'hash_value1', b'member2': b'hash_value2' }
