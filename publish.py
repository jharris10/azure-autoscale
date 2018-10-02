#!/usr/bin/python

import json
import logging
import shlex
import subprocess
import sys
import time

import configparser
from applicationinsights import TelemetryClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient

CRED_FILE = 'monitor.cfg'
resource_group =''
appinsights_name =''

LOG_FILENAME1 = 'azure-autoscaling-publish.log'
logging.basicConfig(filename=LOG_FILENAME1,level=logging.INFO, filemode='w',format='[%(asctime)s] [%(levelname)s] (%(threadName)-10s) %(message)s',)
logger1 = logging.getLogger(__name__)
logger1.setLevel(logging.INFO)

metric_list = [ "panSessionActive",\
                "DataPlaneCPUUtilizationPct",\
                "panGPGatewayUtilizationPct",\
                "panGPGWUtilizationActiveTunnels",\
                "DataPlanePacketBufferUtilization",\
                "panSessionSslProxyUtilization",\
                "panSessionUtilization"]


def get_appinsights_instr_key(rg, appinsights_name, cred, subs_id):
    APPINSIGHTS_TYPE = 'Microsoft.Insights/components'
    resource_client = ResourceManagementClient(cred, subs_id)
    for resource in resource_client.resources.list_by_resource_group(rg):
        # Get the Appinsights instance where the custom metrics are being
        # published.
        if resource.type == APPINSIGHTS_TYPE and 'appinsights' in resource.name:
            appinsights_obj = resource_client.resources.get_by_id(resource.id, '2014-04-01')
            instr_key = appinsights_obj.properties.get('InstrumentationKey', '')
            if appinsights_obj.name == appinsights_name:
                if not instr_key:
                    logger.info("InstrKey is not setup yet in %s." % rg)
                    return None
            return instr_key
    return None

def main():
    config = configparser.ConfigParser()
    config.read(CRED_FILE)

    subscription_id = str(config['DEFAULT']['AZURE_SUBSCRIPTION_ID'])
    appinsights_name = str(config['DEFAULT']['APPINSIGHTS_NAME'])
    resource_group = config['DEFAULT']['RG_NAME']
    credentials = ServicePrincipalCredentials(
        client_id=config['DEFAULT']['azure_client_id'],
        secret=config['DEFAULT']['azure_client_secret'],
        tenant=config['DEFAULT']['azure_tenant_id']
    )

    try:
        resource_client = ResourceManagementClient(credentials, subscription_id)
    except Exception as e:
        self.logger.error("Getting Azure Infra handlers failed %s" % str(e))
        raise e
    inst_key = get_appinsights_instr_key(resource_group,appinsights_name,credentials, subscription_id)
    tc = TelemetryClient(inst_key)

    #logger1.info("[INFO]: Instrumentation key used {}".format(inst_key))

    for metric in metric_list:
        logger1.info("[INFO]: Publishing metrics {}".format(metric))
        tc.track_metric(metric, 0)
        tc.flush()
        time.sleep(2)


if __name__ == "__main__":
    main()
