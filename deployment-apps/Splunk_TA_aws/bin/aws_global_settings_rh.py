#
# SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>
# SPDX-License-Identifier: LicenseRef-Splunk-8-2021
#
#
from __future__ import absolute_import
import aws_bootstrap_env  # noqa: F401 # pylint: disable=unused-import


import splunk.admin as admin

from splunktalib.rest_manager import base, multimodel, normaliser, validator


class AWSConnection(base.BaseModel):
    requiredArgs = {"is_secure"}
    defaultVals = {"is_secure": "1"}
    normalisers = {"is_secure": normaliser.Boolean()}
    validators = {"is_secure": validator.Enum(("0", "1"))}

    outputExtraFields = ("eai:acl", "acl", "eai:appName", "eai:userName")


class Globals(multimodel.MultiModel):
    endpoint = "configs/conf-aws_global_settings"
    modelMap = {
        "aws_connection": AWSConnection,
    }


if __name__ == "__main__":
    admin.init(multimodel.ResourceHandler(Globals), admin.CONTEXT_APP_AND_USER)
