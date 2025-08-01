import redis
import json

from infrastructure.cache.cache_store import CacheStore, ListCacheStore
from infrastructure.cache.setting import RedisSettings


class RedisCache(CacheStore, ListCacheStore):
    """
    redis-py 타입관련 이슈 있음
        - https://github.com/redis/redis-py/issues/2399
        - https://github.com/redis/redis-py/pull/3619
    """
    def __init__(self, maxlen: int = 20_000):
        redis_settings = RedisSettings()
        
        # 커넥션 풀 설정
        pool = redis.ConnectionPool(
            host=redis_settings.REDIS_HOST,
            port=redis_settings.REDIS_PORT,
            password=redis_settings.REDIS_PASSWORD,
            db=redis_settings.REDIS_DB,
            decode_responses=False,
            max_connections=redis_settings.REDIS_POOL_MAX_CONNECTIONS,
            retry_on_timeout=redis_settings.REDIS_POOL_RETRY_ON_TIMEOUT,
            socket_timeout=redis_settings.REDIS_POOL_TIMEOUT,
            socket_connect_timeout=redis_settings.REDIS_POOL_TIMEOUT
        )
        
        self.client = redis.Redis(connection_pool=pool)
        self.maxlen = maxlen
    
    def set_cache_entry(
        self,
        key: str,
        value: dict,
        ttl: int = 3600
    ) -> bool:
        """implementation of the set_cache_entry for CacheStore interface."""
        try:
            pipeline = self.client.pipeline()
            pipeline.hset(name=key, mapping=value)
            pipeline.expire(key, ttl)
            pipeline.execute()
        except Exception as e:
            print(f"Error setting cache entry: {e}")
            return False
        return True

    def get_cache_entry(self, key: str) -> dict | None:
        """implementation of the get_cache_entry for CacheStore interface.
        Because the get_hash_all returns the dict of the byte strings, we need to
        convert it into the dict of the string
        """
        dict_bytes = self.get_hash_all(hash_name=key)
        conv_dict = self.convert_byte_dict_to_string_dict(dict_bytes)
        if len(conv_dict) == 0:
            return None
        return conv_dict

    def delete_cache_entry(self, key: str) -> bool:
        """implementation of the delete_cache_entry for CacheStore interface"""
        return self.del_hash_all(hash_name=key)

    def append_to_list_cache(self, key: str, value: dict, ttl: int=3600) -> bool:
        """
        implementation of the append_to_list_cache for ListCacheStore interface
        """
        try:
            byte_value = json.dumps(value).encode()

            pipeline = self.client.pipeline()
            pipeline.rpush(key, byte_value)
            pipeline.expire(key, ttl)
            pipeline.execute()
        except Exception as e:
                print(f"Error appending to list cache: {e}")
                return False
        return True

    def get_list_cache(self, key: str, len: int):
        """
        implementation of the get_list_cache for ListCacheStore interface
        리스트에서 가장 최근에 추가된 n개의 아이템을 조회하고 파싱하여 반환합니다.
        """
        if len <= 0:
            return []
        
        try:
            # LRANGE key -n -1: 리스트의 마지막 n개 아이템을 가져옵니다.
            # 예: count=10 -> lrange(key, -10, -1)
            recent_items_bytes = self.client.lrange(key, -len, -1)
            
            return [self.convert_byte_to_dict(item) for item in recent_items_bytes]
        
        except Exception as e:
            print(f"Error getting recent list items from Redis: {e}")
            return []
    
    def get_list_cache_all(self, key: str) -> list[dict]:
        """
        implementation of the get_list_cache_all for ListCacheStore interface
        """
        return [self.convert_byte_to_dict(item) for item in self.client.lrange(key, 0, -1)]

    def delete_list_cache(self, key: str) -> bool:
        """implementation of the delete_list_cache for ListCacheStore interface"""
        return self.delete_cache_entry(key)
    
    def convert_byte_to_dict(self, byte: bytes) -> dict:
        return json.loads(byte.decode())

    def convert_byte_dict_to_string_dict(self, byte_dict: dict[bytes, bytes]) -> dict[str, str]:
        """Python redis functions including keys, getXXX return
        list/dict of byte objects instead of strings. This function convert it."""
        return dict(
            map(lambda item: (item[0].decode(), item[1].decode()), byte_dict.items())
        )

    def convert_byte_list_to_string_list(self, byte_list: list[bytes]) -> list[str]:
        """Python redis functions including keys, getXXX return
        list/dict of byte objects instead of strings"""
        return [x.decode("utf-8") for x in byte_list]

    def set_hash(
        self,
        hash_name: str,
        key: str,
        value: str,
    ) -> int:
        return self.client.hset(name=hash_name, key=key, value=value)

    def set_hash_with_map(self, hash_name: str, mapping: dict = None) -> int:
        return self.client.hset(name=hash_name, mapping=mapping)

    def get_hash_all(
        self,
        hash_name: str,
    ) -> dict:
        """
        Returns:
            dict: This function returns the dict of the byte string to be decoded.
        """
        return self.client.hgetall(name=hash_name)

    def get_hash(self, hash_name: str, key: str) -> str | None:
        return self.client.hget(name=hash_name, key=key)

    def get_hash_keys(self, key: str):
        return self.client.hkeys(key)

    def del_hash_all(
        self,
        hash_name: str,
    ):
        return self.client.delete(hash_name)

    def del_hash(self, hash_name: str, keys: list):
        return self.client.hdel(hash_name, *keys)
