from immunity_python_agent.common.logger import logger_config
from immunity_python_agent.utils import scope

logger = logger_config("system_info")


class SystemInfo(object):
    def __init__(self):
        self.unit = 1024 * 1024 * 1024
        try:
            import psutil

            self.psutil = psutil
            logger.info("psutil import success")
        except Exception:
            self.psutil = None
            logger.error("psutil import error, please install psutil")

    # Get network information
    @scope.with_scope(scope.SCOPE_AGENT)
    def print_net_if_addr(self):
        if self.psutil is not None:
            try:
                dic = self.psutil.net_if_addrs()
                network_arr = []
                for adapter in dic:
                    snic_list = dic[adapter]
                    mac = "无 mac 地址"
                    ipv4 = "无 ipv4 地址"
                    ipv6 = "无 ipv6 地址"
                    for snic in snic_list:
                        if snic.family.name in {"AF_LINK", "AF_PACKET"}:
                            mac = snic.address
                        elif snic.family.name == "AF_INET":
                            ipv4 = snic.address
                        elif snic.family.name == "AF_INET6":
                            ipv6 = snic.address
                    network_arr.append("%s, %s, %s, %s" % (adapter, mac, ipv4, ipv6))
                logger.info("get network success")
                return ";".join(network_arr)
            except Exception as e:
                logger.error("get network" + str(e))
                return ""
        else:
            return ""

    # Get CPU information
    @scope.with_scope(scope.SCOPE_AGENT)
    def get_cpu_rate(self):
        if self.psutil is not None:
            # print(self.psutil.cpu_percent())
            percent = self.psutil.cpu_percent()
            return percent
        else:
            return 0

    # Get system memory usage
    @scope.with_scope(scope.SCOPE_AGENT)
    def get_memory_info(self):
        if self.psutil is not None:
            memory_info = self.psutil.virtual_memory()
            return {
                "total": round(memory_info.total / self.unit, 2),
                "used": round(memory_info.used / self.unit, 2),
                "rate": memory_info.percent,
            }
        else:
            return {"total": 0, "use": 0, "rate": 0}

    # Get disk information
    @scope.with_scope(scope.SCOPE_AGENT)
    def get_disk(self):
        disk = {"info": []}
        if self.psutil is not None:
            devs = self.psutil.disk_partitions()
            if devs:
                for dev in devs:
                    disk_info = self.psutil.disk_usage(dev.mountpoint)
                    # Convert bytes to G
                    disk["info"].append(
                        {
                            "name": dev.device,
                            "total": str(round(disk_info.total / self.unit, 2)) + "G",
                            "used": str(round(disk_info.used / self.unit, 2)) + "G",
                            "free": str(round(disk_info.free / self.unit, 2)) + "G",
                            "rate": str(disk_info.percent) + "%",
                            "fstype": dev.fstype,
                        }
                    )
        return disk
