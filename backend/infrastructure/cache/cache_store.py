from abc import ABC, abstractmethod


class CacheStore(ABC):
    """
    CacheStore is the interface for all methods for the in-memory cache storage.
    """

    @abstractmethod
    def set_cache_entry(
        self, key: str, value: dict, ttl: int
    ) -> bool:
        """ set_cache_entry inserts a value with a given key in the cache store

        Args:
            key (str): object key
            value (dictionary): dict-type value
            ttl (int): time to live in seconds
        Returns:
            bool: True when success, False when fail
        """
        pass

    @abstractmethod
    def get_cache_entry(
        self, key: str
    ) -> dict | None:
        """ get_cache_entry lookups and returns the dict-type value with a given key
        
        Args:
            key (str): cache entry key
        Returns:
            dict (str): 
        """
        pass

    @abstractmethod
    def delete_cache_entry(
        self, key: str
    ) -> bool:
        """ delete_cache_entry deletes the cache entry with a given key in the cache store

        Args:
            key (str): object key

        Returns:
            bool: True when success, False when fail
        """
        pass


class ListCacheStore(ABC):

    @abstractmethod
    def append_to_list_cache(self, key: str, value: dict, ttl: int) -> bool:
        """
        Args:
            key (str): Redis 리스트 키
            value (dict): 추가할 딕셔너리 값
            ttl (int): 키의 만료 시간 (초)

        Returns:
            bool: 성공 여부
        """
        pass

    @abstractmethod
    def get_list_cache(self, key: str, len: int) -> list[dict]:
        """
        Args:
            key (str): Redis 리스트 키
            count (int): 가져올 아이템의 개수

        Returns:
            List[Dict[str, Any]]: 파싱된 딕셔너리의 리스트
        """
        pass

    @abstractmethod
    def get_list_cache_all(self, key: str) -> list[dict]:
        """
        Args:
            key (str): Redis 리스트 키

        Returns:
            List[Dict[str, Any]]: 해당 키의 리스트
        """
        pass

    @abstractmethod
    def delete_list_cache(self, key: str) -> bool:
        """
        Args:
            key (str): Redis 리스트 키

        Returns:
            bool: 삭제 성공 여부
        """
        pass
