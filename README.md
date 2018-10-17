# azure autoscale east west
# Palo Alto Networks autoscale for Azure Egress Security



[<img src="http://azuredeploy.net/deploybutton.png"/>](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fjharris10%2Fazure-autoscale%2Fmaster%2FgskDeployInfra.json)

This template automates deployment of firewall LB sandwich environment for Egress Security.
It includes following components:

- One Internal Load Balancer (LB-Egress) - "Standard SKU"
- One VMSS for firewall
- One worker node to remove devices from panorama once terminated

 For information on how to bootstrap the VM-Series firewall running PAN-OS 8.1 and up in Azure see [Bootstrap Instructions](https://www.paloaltonetworks.com/documentation/81/virtualization/virtualization/bootstrap-the-vm-series-firewall/bootstrap-the-vm-series-firewall-in-azure#idd51f75b8-e579-44d6-a809-2fafcfe4b3b6)

 
 If bootstraping with default configuration file is used default credentials are:
 - Username: paloalto
 - Password: PaloAlt0!123!!
