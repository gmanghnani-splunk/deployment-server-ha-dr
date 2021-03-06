#
# SPDX-FileCopyrightText: 2021 Splunk, Inc. <sales@splunk.com>
# SPDX-License-Identifier: LicenseRef-Splunk-8-2021
#
#
"""
File for IAM description for metadata input.
"""
from __future__ import absolute_import

import datetime

import boto3
import splunk_ta_aws.common.ta_aws_consts as tac
import splunksdc.log as logging
from botocore.exceptions import ClientError

from . import description as desc

logger = logging.get_module_logger()

CREDENTIAL_THRESHOLD = datetime.timedelta(minutes=20)

skipped_error_code_list = ["NoSuchEntity", "InvalidAction"]


@desc.generate_credentials
@desc.decorate
def iam_users(config):
    """Yields IAM user."""
    iam_client = desc.BotoRetryWrapper(
        boto_client=boto3.client(
            "iam",
            region_name=config[tac.region],
            aws_access_key_id=config.get(tac.key_id),
            aws_secret_access_key=config.get(tac.secret_key),
            aws_session_token=config.get("aws_session_token"),
        )
    )

    # list users
    paginator = iam_client.get_paginator("list_users")

    # get account password policy (the same among users)
    password_policy = None

    # http://docs.aws.amazon.com/cli/latest/reference/iam/get-account-password-policy.html
    # account may not have enable password policy, and throws out a "NoSuchEntity" Error
    try:
        password_policy = iam_client.get_account_password_policy()
    except ClientError as client_error:
        if (
            "Code" not in client_error.response["Error"]
            or client_error.response["Error"]["Code"] not in skipped_error_code_list
        ):
            logger.error(
                '"get_account_password_policy" operation returns invalid '  # pylint: disable=consider-using-f-string
                "result for account %s: %s" % (config[tac.account_id], client_error)
            )

    for page in paginator.paginate():  # pylint: disable=too-many-nested-blocks
        iam_users = page["Users"]  # pylint: disable=redefined-outer-name
        if iam_users is not None and len(iam_users) > 0:
            for iam_user in iam_users:

                # add account password policy
                if password_policy is not None:
                    iam_user.update(password_policy)

                # get access keys
                ak_paginator = iam_client.get_paginator("list_access_keys")
                access_key_list = []

                for ak_page in ak_paginator.paginate(UserName=iam_user["UserName"]):
                    access_keys = ak_page["AccessKeyMetadata"]
                    if access_keys is not None and len(access_keys) > 0:
                        for access_key in access_keys:
                            # get ak last used
                            # will throw out an error with code "InvalidAction" if does not support (CN region)
                            try:
                                ak_last_used = iam_client.get_access_key_last_used(
                                    AccessKeyId=access_key["AccessKeyId"]
                                )
                                access_key.update(ak_last_used)
                            except ClientError as client_error:
                                if (
                                    "Code" not in client_error.response["Error"]
                                    or client_error.response["Error"]["Code"]
                                    not in skipped_error_code_list
                                ):
                                    logger.error(
                                        '"get_access_key_last_used" operation returns invalid '  # pylint: disable=consider-using-f-string
                                        "result for access key %s: %s"
                                        % (access_key["AccessKeyId"], client_error)
                                    )

                            # remove metadata of response
                            access_key.pop("ResponseMetadata", None)

                            access_key_list.append(access_key)

                iam_user["AccessKeys"] = access_key_list

                # remove metadata of response
                iam_user.pop("ResponseMetadata", None)

                yield iam_user
        desc.refresh_credentials(config, CREDENTIAL_THRESHOLD, iam_client)
