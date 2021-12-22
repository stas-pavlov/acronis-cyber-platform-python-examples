#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import pprint       # used for formatting the output of JSON objects received in API responses

import os
import sys

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Acronis, Config

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

# Request resources with type machines available for the current authorization scope
response = acronis.get(
    "api/resource_management/v4/resources?type=resource.machine"
)

# If we have any machine and not an error in response
if response.ok and "items" in response.json() and len(response.json()["items"]) > 0:
    # Get the first machine id
    first_machine_id = response.json()["items"][0]["id"]

    # Find applied policy
    response = acronis.get(
        f"/api/policy_management/v4/applications?context_id={first_machine_id}&policy_type=policy.protection.total"
    )

    # If we have any applicable plan and not an error in response
    if response.ok and "items" in response.json() and len(response.json()["items"]) > 0:
       # Get the first applicable total policy
        # Either parent or have no parent
        if "parent_ids" in response.json()["items"][0][0]["policy"]:
            first_applicable_policy = response.json()["items"][0][0]["policy"]["parent_ids"][0]
        else:
            first_applicable_policy = response.json()["items"][0][0]["policy"]["id"]


        # Revoke the first applicable policy to the first found machines
        # FOR DEMO PURPOSES ONLY
        response = acronis.delete(
            f"/api/policy_management/v4/applications?context_id={first_machine_id}&policy_id={first_applicable_policy}"
        )

        if response.ok:
            print("The first plan revoked successfully from the first machine.")
        else:
            pprint.pprint(response.json())
    else:
        print("There are no plans to applied to a resource.")
        pprint.pprint(response.json())
else:
    print("There are no resources to revoke a protection plan.")
    pprint.pprint(response.json())
