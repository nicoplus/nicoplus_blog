from libmc import (Client, MC_HASH_MD5, MC_POLL_TIMEOUT,
                   MC_CONNECT_TIMEOUT, MC_RETRY_TIMEOUT)

from app.mc.decorators import create_cache

mc = Client(
    ['localhost'],
    do_split=True,
    comp_threshold=0,
    noreply=False,
    prefix=None,
    hash_fn=MC_HASH_MD5,
    failover=False
)

mc.config(MC_CONNECT_TIMEOUT, 300)  # ms
mc.config(MC_POLL_TIMEOUT, 100)
mc.config(MC_RETRY_TIMEOUT, 5)

globals().update(create_cache(mc))
