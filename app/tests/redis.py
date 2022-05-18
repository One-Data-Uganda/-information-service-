import fakeredis.aioredis


class RedisCache:
    def __init__(self):
        self.redis_cache = None

    async def init_cache(self):
        if not self.redis_cache:
            self.redis_cache = await fakeredis.aioredis.create_redis_pool()

    async def keys(self, pattern):
        if not self.redis_cache:
            await self.init_cache()
        return await self.redis_cache.keys(pattern)

    async def set(self, key, value):
        if not self.redis_cache:
            await self.init_cache()
        return await self.redis_cache.set(key, value)

    async def get(self, key):
        if not self.redis_cache:
            await self.init_cache()
        return await self.redis_cache.get(key)

    async def hget(self, key, val):
        if not self.redis_cache:
            await self.init_cache()
        r = await self.redis_cache.hget(key, val)

        return r

    async def hgetall(self, key):
        if not self.redis_cache:
            await self.init_cache()
        return await self.redis_cache.hgetall(key)

    async def hset(self, key, idx, val):
        if not self.redis_cache:
            await self.init_cache()
        r = await self.redis_cache.hset(key, idx, val)
        return r

    async def hdel(self, key, idx):
        if not self.redis_cache:
            await self.init_cache()
        return await self.redis_cache.hdel(key, idx)

    async def close(self):
        self.redis_cache.close()
        await self.redis_cache.wait_closed()


redis_cache = RedisCache()
