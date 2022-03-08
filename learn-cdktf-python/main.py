#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from imports.ibm import IbmProvider, IsVpc, DataIbmIsZones, DataIbmIsImage, IsSshKey, IsSubnet, IsInstance, IsFloatingIp, IsSecurityGroupRule
from imports.tls import PrivateKey, TlsProvider
from imports.null import NullProvider, Resource


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # create local dict test for to refer the objects to be created
        self.test = {}

        # define providers
        self.test['provider_ibm'] = IbmProvider(self, "Ibm", region="us-south")
        self.test['provider_tls'] = TlsProvider(self, "Tls")
        self.test['provider_null'] = NullProvider(self, "Null")

        # define data sources
        self.test['data_ibm_is_zones'] = DataIbmIsZones(
            self, "data_is_zones", region="us-south")
        self.test['data_ubuntu_focal'] = DataIbmIsImage(
            self, "data_ubuntu_image", name="ibm-ubuntu-20-04-3-minimal-amd64-1")

        # define resources here
        self.test['vpc'] = IsVpc(self, "vpc", name="hello-vpc")
        self.test['ssh_key_insecure'] = PrivateKey(
            self, "insecure", algorithm="RSA", rsa_bits=4096
        )
        self.test['ssh_key'] = IsSshKey(
            self, "ssh_key", name="hello-key",
            public_key=self.test['ssh_key_insecure'].public_key_openssh
        )
        self.test['subnet'] = IsSubnet(
            self, "subnet", name="hello-subnet",
            vpc=self.test['vpc'].id,
            total_ipv4_address_count=256,
            zone="${element(data.ibm_is_zones.data_is_zones.zones, 0)}"
        )
        self.test['instance'] = IsInstance(
            self, "instance", name="hello-instance",
            vpc=self.test['vpc'].id,
            keys=[self.test['ssh_key'].id],
            image=self.test['data_ubuntu_focal'].id,
            profile="cx2-2x4",
            primary_network_interface={'subnet': self.test['subnet'].id},
            zone="${element(data.ibm_is_zones.data_is_zones.zones, 0)}"
        )

        self.test['sg_rule_icmp'] = IsSecurityGroupRule(
            self, "sg_rule_icmp",
            group=self.test['vpc'].default_security_group,
            direction="inbound",
            remote="0.0.0.0/0",
            icmp={
                'code': 0,
                'type': 8
            }
        )

        self.test['sg_rule_ssh'] = IsSecurityGroupRule(
            self, "sg_rule_ssh",
            group=self.test['vpc'].default_security_group,
            direction="inbound",
            remote="0.0.0.0/0",
            tcp={
                'port_min': 22,
                'port_max': 22
            }
        )

        self.test['fip'] = IsFloatingIp(
            self, "fip", name="hello-fip",
            target="${ibm_is_instance.instance.primary_network_interface[0].id}"
        )

        # It seems not implemented yet
#         self.test['ssh_ping'] = Resource(
#             self, "null_resource_ssh",
#             triggers={'fip_instance_id': self.test['instance'].id},
#             #
#             connection={
#                 'type': 'ssh',
#                 'user': 'ubuntu',
#                 'host': self.test['fip'].address,
#                 'private_key': self.test['ssh_key_insecure'].private_key_pem,
#                 'timeout': '10m'
#             },
#             #
#             provisioner={
#                 'remote-exec': {
#                     'inline': [
#                         "echo $(uname -a)",
#                         "whereis grep"
#                     ]
#                 }
#             }
#         )

        # Terraform Output
        TerraformOutput(self, "hello-VPC", value=self.test['vpc'])
        TerraformOutput(self, "hello-data.ibm_is_zones",
                        value=self.test['data_ibm_is_zones'].zones)
        TerraformOutput(self, "hello-key", value=self.test['ssh_key'])
        TerraformOutput(self, "hello-subnet", value=self.test['subnet'])
        TerraformOutput(self, "hello-instance", value=self.test['instance'])
        TerraformOutput(self, "hello-fip", value=self.test['fip'])
        TerraformOutput(self, "hello-sg-rule-icmp",
                        value=self.test['sg_rule_icmp'])


app = App()
MyStack(app, "learn-cdktf-python")

app.synth()
