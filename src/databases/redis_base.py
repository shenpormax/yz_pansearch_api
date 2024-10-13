"""
    Created by fre123 at 2024-10-11.
    Description: Redis 连接类，使用前请确保 pipenv install redis
    Changelog: all notable changes to this file will be documented
"""

import redis

from src.utils.tools import md5_encryption


class RedisBase:
    """
    Redis连接类
    """

    _db = {}

    def __init__(self, redis_config: dict):
        if redis_config:
            self.redis_config = redis_config
        else:
            raise ValueError("redis_config is expected!")

    def pool_client(self, db: int = None):
        """
        客户端连接池
        """
        host = self.redis_config.get("host", "127.0.0.1")
        port = self.redis_config.get("port", 6379)
        db = db if db is not None else self.redis_config.get("db", 0)
        password = (
            self.redis_config.get("password", "")
            if self.redis_config.get("password", "")
            else None
        )
        pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
        return redis.Redis(
            connection_pool=pool, decode_responses=True, retry_on_timeout=True
        )

    def get_db(self, *, db: int = None) -> redis.Redis:
        """
        获取redis的连接实例
        :param db:
        :return:
        """
        if db is None:
            db = self.redis_config.get("db", 0)

        if db not in self._db:
            self._db[db] = self.pool_client(db)

        return self._db[db]


class RedisManager:
    """
    管理Redis实例
    """

    _redis_dict = {}

    @classmethod
    def get_redis_base(cls, redis_config: dict) -> RedisBase:
        """
        获取redis实例
        :param redis_config: redis config
        :return: RedisBase
        """
        redis_key = md5_encryption(f"{redis_config}")
        if redis_key not in cls._redis_dict:
            cls._redis_dict[redis_key] = RedisBase(redis_config)
        return cls._redis_dict[redis_key]
