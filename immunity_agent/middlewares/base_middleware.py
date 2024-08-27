import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

from dongtai_agent_python.api import OpenAPI
from dongtai_agent_python.assess.patch import enable_patches
from dongtai_agent_python.common.logger import logger_config
from dongtai_agent_python.setting import Setting
from dongtai_agent_python.utils import scope

logger = logger_config("base_middleware")


class BaseMiddleware(object):
    loaded = False

    def __init__(self, container):
        if BaseMiddleware.loaded:
            return

        start_time = time.time()
        scope.enter_scope(scope.SCOPE_AGENT)

        self.init_setting()
        logger.info("python agent init, version: " + self.setting.version)

        self.setting.set_container(container)

        # middleware id
        self.id = id(self)
        self.executor = ThreadPoolExecutor()

        self.openapi = OpenAPI(self.setting)

        # register agent
        register_resp = self.openapi.agent_register()
        if register_resp.get("status", 0) == 201:
            logger.info("python agent register success ")
        else:
            logger.error("python agent register error ")

        logger.debug("------begin hook-----")
        policies = self.get_policies()
        enable_patches(policies)

        self.openapi.agent_startup_time((time.time() - start_time) * 1000)
        logger.info("python agent hook open")

        scope.exit_scope()
        BaseMiddleware.loaded = True
