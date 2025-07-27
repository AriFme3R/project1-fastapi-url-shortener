from redis import Redis


from .users_helper import AbstractUsersHelper
from core import config


class RedisUsersHelper(AbstractUsersHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        res = self.redis.get(username)
        assert isinstance(res, str)
        return res


redis_users = RedisUsersHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_USERS,
)
