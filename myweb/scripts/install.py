#!/bin/python
from . import Logger,CONFIG
from  .generate_conf import generate_config

logger = Logger.Logger().getlog()
def install(data):

    try:
        rv = generate_config(data)
        logger.info(rv)
        if not rv:
            return 29
        if rv == 45:
            return rv
        if rv == 61:
            return rv

        srcfile = CONFIG.SOURCE_INSTALL_CONF_FILE % data['task_id']
        if not self.distribute_conf(data, srcfile, CONFIG.TARGET_INSTALL_CONF_FILE):
            return 30

        taskid = data['task_id']
        sn = data['sn']
        ilomac = data['ethernet']['ilo_inf']['mac_addr']
        iloip = data['ethernet']['ilo_inf']['ipaddr']

        pv = self.PXEBOOT(taskid, sn, ilomac, iloip)
        return pv
    except Exception as e:
        return e
