.. Zabbix Device Manager 

.. toctree::
    :maxdepth: 2

#####################
Zabbix Device Manager
#####################

The Zabbix Devie Manager API exposes services that control NBN device
elements configuration within the Zabbix Monitoring Suite.

The API for the `Device` is defined as::

    http://<host>:<port>/api/deivce

**************************
Adding new Device Elements
**************************

Clients can add a device to Zabbix with a ``POST`` HTTP method request.  The
parameters of the new device must be provided as a JSON string in the body
of the request.  For example::

    POST /api/device HTTP/1.1
    Host: example.com

    {
        "equip_inst_id": 211753,
        "physical_name": "2ABN-01-01-PSY",
        "physical_name_extn": "0001",
        "nw_ip_addr": "10.35.222.58",
        "equip_inst_id_1": "211753",
        "equip_status_id": 3
    }

Sample response::

    HTTP/1.1 201 Created

    {
        "equip_inst_id": 211753,
        "equip_inst_id_1": 211753,
        "equip_status_id": 3,
        "nw_ip_addr": "10.35.222.58",
        "physical_name": "2ABN-01-01-PSY",
        "physical_name_extn": "0001"
    }

Malformed ``POST`` requests will return a HTTP 400 Bad Request error.

**********************
Query existing Devices
**********************

Existing devices can be queries with the ``GET`` HTTP method.

To return all available devices::

    GET /api/device

    {
        "num_results": 1,
        "page": 1,
        "total_pages": 1
        "objects": [
            {
                "equip_inst_id": 211753,
                "equip_inst_id_1": 211753,
                "equip_status_id": 3,
                "nw_ip_addr": "10.35.222.58",
                "physical_name": "2ABN-01-01-PSY",
                "physical_name_extn": "0001"
            }
        ],
    }

To return a single device with a known private key::

    GET /api/device/211753

    {
        "equip_inst_id": 211753,
        "equip_inst_id_1": 211753,
        "equip_status_id": 3,
        "nw_ip_addr": "10.35.222.58",
        "physical_name": "2ABN-01-01-PSY",
        "physical_name_extn": "0001"
    }

To return a list of devices that match a given criteria you must
supply the parameters as a JSON string::

    GET /api/person?q={ "equip_inst_id": 21175}

    {
        "num_results": 1,
        "page": 1,
        "total_pages": 1
        "objects": [
            {
                "equip_inst_id": 211753,
                "equip_inst_id_1": 211753,
                "equip_status_id": 3,
                "nw_ip_addr": "10.35.222.58",
                "physical_name": "2ABN-01-01-PSY",
                "physical_name_extn": "0001"
            }
        ],
    }

*************************
Delete an Existing Device
*************************

Devices can be removed with the ``HTTP`` ``DELETE`` against the
private key::

    DELETE /api/device/211753

Sample response::

    HTTP/1.1 204 No Content
