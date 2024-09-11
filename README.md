[comment]: # "Auto-generated SOAR connector documentation"
# AWS GuardDuty

Publisher: Splunk  
Connector Version: 2.1.11  
Product Vendor: AWS  
Product Name: GuardDuty  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 6.2.1  

This app integrates with AWS GuardDuty to investigate findings

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2019-2021 Splunk Inc."
[comment]: # ""
[comment]: # "  Licensed under Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)"
[comment]: # ""
## SDK and SDK Licensing details for the app

### boto3

This app uses the boto3 module, which is licensed under the Apache Software License (Apache License
2.0), Copyright (c) Amazon Web Services.

### botocore

This app uses the botocore module, which is licensed under the Apache Software License (Apache
License 2.0), Copyright (c) Amazon Web Services.

### s3transfer

This app uses the s3transfer module, which is licensed under the Apache Software License (Apache
License 2.0), Copyright (c) Amazon Web Services.

### six

This app uses the six module, which is licensed under the MIT License (MIT), Copyright (c) Benjamin
Peterson.

### urllib3

This app uses the urllib3 module, which is licensed under the MIT License (MIT), Copyright (c)
Andrey Petrov.

### python-dateutil

This app uses the python-dateutil module, which is licensed under the Apache Software License, BSD
License (Dual License), Copyright (c) Gustavo Niemeyer.

### jmespath

This app uses the jmespath module, which is licensed under the MIT License (MIT), Copyright (c)
James Saryerwinnie.

## Asset Configuration

There are two ways to configure an AWS GuardDuty asset. The first is to configure the **access_key**
, **secret_key** and **region** variables. If it is preferred to use a role and Phantom is running
as an EC2 instance, the **use_role** checkbox can be checked instead. This will allow the role that
is attached to the instance to be used. Please see the [AWS EC2 and IAM
documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)
for more information.

Region parameter provided in the asset configuration parameter and region of the bucket which is
created in AWS console must match otherwise user will get InvalidLocationConstraint error.

For the **Update bucket** action,
API is unable to validate the KMS key. Hence, it is recommended to provide a
valid KMS key in this action parameter otherwise it will affect the S3 bucket.
e.g If we update the S3 bucket with the invalid KMS key and then run create object action on the bucket then the action will not work for encryption = NONE.

## Assumed Role Credentials

The optional **credentials** action parameter consists of temporary **assumed role** credentials
that will be used to perform the action instead of those that are configured in the **asset** . The
parameter is not designed to be configured manually, but should be used in conjunction with the
Phantom AWS Security Token Service app. The output of the **assume_role** action of the STS app with
data path **assume_role\_\<number>:action_result.data.\*.Credentials** consists of a dictionary
containing the **AccessKeyId** , **SecretAccessKey** , **SessionToken** and **Expiration** key/value
pairs. This dictionary can be passed directly into the credentials parameter in any of the following
actions within a playbook. For more information, please see the [AWS Identity and Access Management
documentation](https://docs.aws.amazon.com/iam/index.html) .

## On Poll Guidelines

-   **Configuration Parameters**

      

    -   The asset configuration parameter `         poll_now_days        ` is optional, with the
        default value of 30 days. This configuration parameter is used for the manual polling using
        Poll Now.
    -   The asset configuration parameter `         filter_name        ` is optional and if not
        specified, it will fetch all the findings. This configuration parameter is used in all the
        On Poll modes (manual polling, scheduled polling, and interval polling).

      

-   **Manual Polling**

      

    -   Manual polling will fetch all the findings (in latest first order) based on the given
        `         filter_name        ` (if `         filter_name        ` is not provided, all
        findings will be fetched) for the last `         poll_now_days        ` from the current
        time (if `         poll_now_days        ` is not specified, default 30 days will be
        considered).

      

-   **Scheduled | Interval Polling**

      

    -   The scheduled | interval polling fetches the findings (in oldest first order to ensure zero
        data loss) based on the same logic of the manual polling for the first run. The 'updatedAt'
        time of the last fetched finding gets stored in this first run.
    -   For the consecutive runs, the findings get fetched after the stored 'updatedAt' time in the
        previous run.
    -   If the `         filter_name        ` gets changed at an intermediate stage of the
        scheduled | interval polling, the next run of polling will auto-detect the change and it will
        poll the findings and reset the 'updatedAt' time based on the new
        `         filter_name        ` .

      

-   **Recommendations for Filter Creation on AWS GuardDuty UI**

      

    -   For the On Poll action, it is not recommended to include 'updatedAt' (time-based) filter
        criteria in the filter created on AWS GuardDuty UI to avoid conflicts with the timing logic
        of the On Poll action.
    -   If 'updatedAt' (time-based) filter criteria is included in the filter created on AWS
        GuardDuty UI, it will be explicitly replaced with the timing logic of the On Poll action
        **(keeping other filter criteria the same)** .


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a GuardDuty asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**access_key** |  optional  | password | AWS Access Key
**secret_key** |  optional  | password | AWS Secret Key
**region** |  required  | string | AWS Region
**filter_name** |  optional  | string | Name of the saved filter on UI of AWS GuardDuty
**poll_now_days** |  optional  | numeric | Number of days prior current date to start polling (Default: 30)
**use_role** |  optional  | boolean | Use attached role when running Phantom in EC2

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[on poll](#action-on-poll) - Callback action for the on_poll ingest functionality  
[update finding](#action-update-finding) - Updates specified Amazon GuardDuty findings as useful or not useful  
[run query](#action-run-query) - Fetch the findings as per the filters applied  
[archive finding](#action-archive-finding) - Archives Amazon GuardDuty findings specified by the detector ID and list of finding IDs  
[unarchive finding](#action-unarchive-finding) - Unarchives Amazon GuardDuty findings specified by the detector ID and list of finding IDs  
[list filters](#action-list-filters) - Returns a paginated list of the current filters  
[list threats](#action-list-threats) - Lists the ThreatIntelSets of the GuardDuty service specified by the detector ID  
[list ip sets](#action-list-ip-sets) - Lists the IPSets of the GuardDuty service specified by the detector ID  
[list detectors](#action-list-detectors) - Lists detectorIds of all the existing Amazon GuardDuty detector resources  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'on poll'
Callback action for the on_poll ingest functionality

Type: **ingest**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container_id** |  optional  | Container IDs to limit the ingestion to | string | 
**start_time** |  optional  | Start of time range, in epoch time (milliseconds) | numeric | 
**end_time** |  optional  | End of time range, in epoch time (milliseconds) | numeric | 
**container_count** |  optional  | Maximum number of container records to query for | numeric | 
**artifact_count** |  optional  | Maximum number of artifact records to query for | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'REDACTED', 'Expiration': 'REDACTED', 'SecretAccessKey': 'REDACTED', 'SessionToken': 'REDACTED'}   

## action: 'update finding'
Updates specified Amazon GuardDuty findings as useful or not useful

Type: **generic**  
Read only: **False**

For the parameter 'finding_id', if the user provides comma-separated values and one or more values are invalid, then those values will be simply ignored and only correct values will be used for further processing.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**finding_id** |  required  | The IDs of the findings (Comma separated IDs allowed) | string |  `aws guardduty finding id` 
**feedback** |  required  | Feedback value of the finding | string | 
**comment** |  optional  | Additional feedback about the finding | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.comment | string |  |   useful 
action_result.parameter.detector_id | string |  `aws guardduty detector id`  |   7eb38a3ebb7f20c83dcddbc35a46a0a4 
action_result.parameter.feedback | string |  |   USEFUL 
action_result.parameter.finding_id | string |  `aws guardduty finding id`  |   e0b51274addd38155e1e488bf2e6cfd1 
action_result.data | string |  |  
action_result.summary.total_updated_findings | numeric |  |   1 
action_result.message | string |  |   Total updated findings: 1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'REDACTED', 'Expiration': 'REDACTED', 'SecretAccessKey': 'REDACTED', 'SessionToken': 'REDACTED'}   

## action: 'run query'
Fetch the findings as per the filters applied

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**instance_id** |  optional  | The ID of the EC2 instance | string |  `aws guardduty instance id` 
**severity** |  optional  | The severity of the finding | string |  `aws guardduty severity` 
**public_ip** |  optional  | Public IP address of the EC2 instance | string |  `ip` 
**private_ip** |  optional  | Private IP address of the EC2 instance | string |  `ip` 
**limit** |  optional  | The maximum number of results to be fetched. If not provided, then all the results will be fetched | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.detector_id | string |  `aws guardduty detector id`  |   7eb38a3ebb7f20c83dcddbc35a46a0a4 
action_result.parameter.instance_id | string |  `aws guardduty instance id`  |   i-0242775c131db2820  i-0d872de1de2ea7640 
action_result.parameter.limit | numeric |  |   5 
action_result.parameter.private_ip | string |  `ip`  |   172.29.54.75  172.32.42.2 
action_result.parameter.public_ip | string |  `ip`  |   5.4.3.2  1.2.3.4 
action_result.parameter.severity | string |  `aws guardduty severity`  |   High 
action_result.data.\*.AccountId | string |  |   849257271967 
action_result.data.\*.Arn | string |  |   arn:aws:guardduty:us-east-1:849257271967:detector/7eb38a3ebb7f20c83dcddbc35a46a0a4/finding/04b5151743dbff66db6a5085f55d57c4 
action_result.data.\*.CreatedAt | string |  |   2019-04-17T07:24:13.623Z 
action_result.data.\*.Description | string |  |   EC2 instance has an unprotected port which is being probed by a known malicious host 
action_result.data.\*.Id | string |  `aws guardduty finding id`  |   04b5151743dbff66db6a5085f55d57c4 
action_result.data.\*.NextToken | string |  |  
action_result.data.\*.Partition | string |  |   aws 
action_result.data.\*.Region | string |  |   us-east-1 
action_result.data.\*.Resource.AccessKeyDetails.AccessKeyId | string |  |   REDACTED 
action_result.data.\*.Resource.AccessKeyDetails.PrincipalId | string |  |   157568067690 
action_result.data.\*.Resource.AccessKeyDetails.UserName | string |  |   Root 
action_result.data.\*.Resource.AccessKeyDetails.UserType | string |  |   Root 
action_result.data.\*.Resource.InstanceDetails.AvailabilityZone | string |  |   us-east-1d 
action_result.data.\*.Resource.InstanceDetails.IamInstanceProfile.Arn | string |  |   arn:aws:iam::157568067690:instance-profile/phantom-sts-ec2-instance 
action_result.data.\*.Resource.InstanceDetails.IamInstanceProfile.Id | string |  |   AIPASJL6J5BVOWSURYNAB 
action_result.data.\*.Resource.InstanceDetails.ImageDescription | string |  |   Amazon Linux 2 AMI 2.0.20190313 x86_64 HVM gp2 
action_result.data.\*.Resource.InstanceDetails.ImageId | string |  |   ami-0de53d8956e8dcf80 
action_result.data.\*.Resource.InstanceDetails.InstanceId | string |  `aws guardduty instance id`  |   i-0d872de1de2ea7640 
action_result.data.\*.Resource.InstanceDetails.InstanceState | string |  |   running 
action_result.data.\*.Resource.InstanceDetails.InstanceType | string |  |   t2.micro 
action_result.data.\*.Resource.InstanceDetails.LaunchTime | string |  |   2019-04-15T14:14:50Z 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.NetworkInterfaceId | string |  |   eni-0fe0a1d2984f4aae1 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.PrivateDnsName | string |  |   ip-172-31-95-167.ec2.internal 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.PrivateIpAddress | string |  `ip`  |   172.31.95.167 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.PrivateIpAddresses.\*.PrivateDnsName | string |  |   ip-172-31-95-167.ec2.internal 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.PrivateIpAddresses.\*.PrivateIpAddress | string |  `ip`  |   172.31.95.167 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.PublicDnsName | string |  |   ec2-3-87-26-18.compute-1.amazonaws.com 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.PublicIp | string |  `ip`  |   3.87.26.18 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.SecurityGroups.\*.GroupId | string |  |   sg-0c2ff5df9f6b41a58 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.SecurityGroups.\*.GroupName | string |  |   launch-wizard-12 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.SubnetId | string |  |   subnet-d8782cf7 
action_result.data.\*.Resource.InstanceDetails.NetworkInterfaces.\*.VpcId | string |  |   vpc-5113dc2a 
action_result.data.\*.Resource.InstanceDetails.Tags.\*.Key | string |  |   Name 
action_result.data.\*.Resource.InstanceDetails.Tags.\*.Value | string |  |   test-phantom-new-2 
action_result.data.\*.Resource.ResourceType | string |  |   Instance 
action_result.data.\*.SchemaVersion | string |  |   2.0 
action_result.data.\*.Service.Action.ActionType | string |  |   PORT_PROBE 
action_result.data.\*.Service.Action.AwsApiCallAction.Api | string |  |   DescribeEventAggregates 
action_result.data.\*.Service.Action.AwsApiCallAction.CallerType | string |  |   Remote IP 
action_result.data.\*.Service.Action.AwsApiCallAction.ErrorCode | string |  |   NoSuchEntityException 
action_result.data.\*.Service.Action.AwsApiCallAction.RemoteIpDetails.City.CityName | string |  |   Silvassa 
action_result.data.\*.Service.Action.AwsApiCallAction.RemoteIpDetails.Country.CountryName | string |  |   India 
action_result.data.\*.Service.Action.AwsApiCallAction.RemoteIpDetails.GeoLocation.Lat | numeric |  |   20.2688 
action_result.data.\*.Service.Action.AwsApiCallAction.RemoteIpDetails.GeoLocation.Lon | numeric |  |   73.0162 
action_result.data.\*.Service.Action.AwsApiCallAction.RemoteIpDetails.IpAddressV4 | string |  |   103.101.58.60 
action_result.data.\*.Service.Action.AwsApiCallAction.RemoteIpDetails.Organization.Asn | string |  |   45117 
action_result.data.\*.Service.Action.AwsApiCallAction.RemoteIpDetails.Organization.AsnOrg | string |  |   A's Network 
action_result.data.\*.Service.Action.AwsApiCallAction.RemoteIpDetails.Organization.Isp | string |  |   A's Network 
action_result.data.\*.Service.Action.AwsApiCallAction.RemoteIpDetails.Organization.Org | string |  |   A's Network 
action_result.data.\*.Service.Action.AwsApiCallAction.ServiceName | string |  |   health.amazonaws.com 
action_result.data.\*.Service.Action.NetworkConnectionAction.Blocked | boolean |  |   True  False 
action_result.data.\*.Service.Action.NetworkConnectionAction.ConnectionDirection | string |  |   INBOUND 
action_result.data.\*.Service.Action.NetworkConnectionAction.LocalIpDetails.IpAddressV4 | string |  |   172.2.3.4 
action_result.data.\*.Service.Action.NetworkConnectionAction.LocalPortDetails.Port | numeric |  |   22 
action_result.data.\*.Service.Action.NetworkConnectionAction.LocalPortDetails.PortName | string |  |   SSH 
action_result.data.\*.Service.Action.NetworkConnectionAction.Protocol | string |  |   TCP 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemoteIpDetails.City.CityName | string |  |   Ashburn 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemoteIpDetails.Country.CountryName | string |  |   United States 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemoteIpDetails.GeoLocation.Lat | numeric |  |   39.0481 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemoteIpDetails.GeoLocation.Lon | numeric |  |   -77.4728 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemoteIpDetails.IpAddressV4 | string |  `ip`  |   3.4.5.6 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemoteIpDetails.Organization.Asn | string |  |   14618 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemoteIpDetails.Organization.AsnOrg | string |  |   Amazon.com, Inc. 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemoteIpDetails.Organization.Isp | string |  |   Amazon.com 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemoteIpDetails.Organization.Org | string |  |   Amazon.com 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemotePortDetails.Port | numeric |  |   32768 
action_result.data.\*.Service.Action.NetworkConnectionAction.RemotePortDetails.PortName | string |  |   Unknown 
action_result.data.\*.Service.Action.PortProbeAction.Blocked | boolean |  |   True  False 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.LocalPortDetails.Port | numeric |  |   500 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.LocalPortDetails.PortName | string |  |   Unknown 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.RemoteIpDetails.City.CityName | string |  |   Moscow 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.RemoteIpDetails.Country.CountryName | string |  |   Russia 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.RemoteIpDetails.GeoLocation.Lat | numeric |  |   55.7386 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.RemoteIpDetails.GeoLocation.Lon | numeric |  |   37.6068 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.RemoteIpDetails.IpAddressV4 | string |  `ip`  |   81.4.2.3 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.RemoteIpDetails.Organization.Asn | string |  |   49505 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.RemoteIpDetails.Organization.AsnOrg | string |  |   OOO Network of data-centers Selectel 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.RemoteIpDetails.Organization.Isp | string |  |   Infolink LLC 
action_result.data.\*.Service.Action.PortProbeAction.PortProbeDetails.\*.RemoteIpDetails.Organization.Org | string |  |   Infolink LLC 
action_result.data.\*.Service.Archived | boolean |  |   True  False 
action_result.data.\*.Service.Count | numeric |  |   579 
action_result.data.\*.Service.DetectorId | string |  `md5`  |   7eb38a3ebb7f20c83dcddbc35a46a0a4 
action_result.data.\*.Service.EventFirstSeen | string |  |   2019-04-17T07:09:54Z 
action_result.data.\*.Service.EventLastSeen | string |  |   2019-04-24T08:58:52Z 
action_result.data.\*.Service.Evidence.ThreatIntelligenceDetails.\*.ThreatListName | string |  |   ProofPoint 
action_result.data.\*.Service.ResourceRole | string |  |   TARGET 
action_result.data.\*.Service.ServiceName | string |  |   guardduty 
action_result.data.\*.Service.UserFeedback | string |  |   USEFUL 
action_result.data.\*.Severity | string |  `aws guardduty severity`  |   Low 
action_result.data.\*.Title | string |  |   Unprotected port on EC2 instance i-0d872de1de2ea7640 is being probed 
action_result.data.\*.Type | string |  |   Recon:EC2/PortProbeUnprotectedPort 
action_result.data.\*.UpdatedAt | string |  |   2019-04-24T09:06:21.566Z 
action_result.summary.total_findings | numeric |  |   1  7 
action_result.message | string |  |   Total findings: 1  Total findings: 7 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'REDACTED', 'Expiration': 'REDACTED', 'SecretAccessKey': 'REDACTED', 'SessionToken': 'REDACTED'}   

## action: 'archive finding'
Archives Amazon GuardDuty findings specified by the detector ID and list of finding IDs

Type: **contain**  
Read only: **False**

For the parameter 'finding_id', if the user provides comma-separated values and one or more values are invalid, then those values will be simply ignored and only correct values will be used for further processing.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**finding_id** |  required  | The IDs of the findings (Comma separated IDs allowed) | string |  `aws guardduty finding id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.detector_id | string |  `aws guardduty detector id`  |   7eb38a3ebb7f20c83dcddbc35a46a0a4 
action_result.parameter.finding_id | string |  `aws guardduty finding id`  |   e0b51274addd38155e1e488bf2e6cfd1 
action_result.data | string |  |  
action_result.summary.total_findings | numeric |  |   1 
action_result.message | string |  |   Successfully archived the findings 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'REDACTED', 'Expiration': 'REDACTED', 'SecretAccessKey': 'REDACTED', 'SessionToken': 'REDACTED'}   

## action: 'unarchive finding'
Unarchives Amazon GuardDuty findings specified by the detector ID and list of finding IDs

Type: **correct**  
Read only: **False**

For the parameter 'finding_id', if the user provides comma-separated values and one or more values are invalid, then those values will be simply ignored and only correct values will be used for further processing.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**finding_id** |  required  | The IDs of the findings (Comma separated IDs allowed) | string |  `aws guardduty finding id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.detector_id | string |  `aws guardduty detector id`  |   7eb38a3ebb7f20c83dcddbc35a46a0a4 
action_result.parameter.finding_id | string |  `aws guardduty finding id`  |   e0b51274addd38155e1e488bf2e6cfd1 
action_result.data | string |  |  
action_result.summary.total_findings | numeric |  |   0  1 
action_result.message | string |  |   Successfully unarchived the findings 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'REDACTED', 'Expiration': 'REDACTED', 'SecretAccessKey': 'REDACTED', 'SessionToken': 'REDACTED'}   

## action: 'list filters'
Returns a paginated list of the current filters

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**limit** |  optional  | The maximum number of filters to be fetched | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.detector_id | string |  `aws guardduty detector id`  |   7eb38a3ebb7f20c83dcddbc35a46a0a4 
action_result.parameter.limit | numeric |  |   5 
action_result.data.\*.Action | string |  |   NOOP 
action_result.data.\*.Description | string |  |   only high severity incidents  test 
action_result.data.\*.FilterName | string |  |   find_instanceid 
action_result.data.\*.FindingCriteria.Criterion.id.Eq | string |  |   avv 
action_result.data.\*.FindingCriteria.Criterion.resource.instanceDetails.instanceId.Eq | string |  |   i-0029a3c756f99d4e9 
action_result.data.\*.FindingCriteria.Criterion.service.archived.Eq | string |  |   false 
action_result.data.\*.FindingCriteria.Criterion.severity.Eq | string |  |   8 
action_result.data.\*.FindingCriteria.Criterion.updatedAt.GreaterThan | numeric |  |   1609439400000 
action_result.data.\*.FindingCriteria.Criterion.updatedAt.Gt | numeric |  |   1609439400000 
action_result.data.\*.FindingCriteria.Criterion.updatedAt.LessThan | numeric |  |   1612290540000 
action_result.data.\*.FindingCriteria.Criterion.updatedAt.Lt | numeric |  |   1612290540000 
action_result.data.\*.Name | string |  |   my-test-high-severity-filter  find_instanceid 
action_result.data.\*.Rank | numeric |  |   1 
action_result.summary.total_filters | numeric |  |   1  3 
action_result.message | string |  |   Total filters: 1  Total filters: 3 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'REDACTED', 'Expiration': 'REDACTED', 'SecretAccessKey': 'REDACTED', 'SessionToken': 'REDACTED'}   

## action: 'list threats'
Lists the ThreatIntelSets of the GuardDuty service specified by the detector ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**limit** |  optional  | The maximum number of threat intel sets to be fetched. If not provided, then all the threat intel sets will be fetched | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.detector_id | string |  `aws guardduty detector id`  |   7eb38a3ebb7f20c83dcddbc35a46a0a4 
action_result.parameter.limit | numeric |  |   5 
action_result.data.\*.Format | string |  |   TXT 
action_result.data.\*.Location | string |  `url`  |   https://s3.amazonaws.com/phantom-guardduty/IPset1_file.txt 
action_result.data.\*.Name | string |  |   ThreatIPSet 
action_result.data.\*.Status | string |  |   INACTIVE 
action_result.data.\*.ThreatIntelSetId | string |  `md5`  |   04b517f3e469cdc30513629c7473c33d 
action_result.summary.total_threats | numeric |  |   2 
action_result.message | string |  |   Total threats: 2 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'REDACTED', 'Expiration': 'REDACTED', 'SecretAccessKey': 'REDACTED', 'SessionToken': 'REDACTED'}   

## action: 'list ip sets'
Lists the IPSets of the GuardDuty service specified by the detector ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**limit** |  optional  | The maximum number of IP sets to be fetched. If not provided, then all the IP sets will be fetched | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.detector_id | string |  `aws guardduty detector id`  |   7eb38a3ebb7f20c83dcddbc35a46a0a4 
action_result.parameter.limit | numeric |  |   51 
action_result.data.\*.Format | string |  |   TXT 
action_result.data.\*.IpSetId | string |  `md5`  |   18b517f39a5903e092182fe9a97467b9 
action_result.data.\*.Location | string |  `url`  |   https://s3.amazonaws.com/phantom-guardduty/IPset_file.txt 
action_result.data.\*.Name | string |  |   IPSet 
action_result.data.\*.Status | string |  |   ACTIVE 
action_result.summary.total_ip_sets | numeric |  |   1 
action_result.message | string |  |   Total ip sets: 1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'REDACTED', 'Expiration': 'REDACTED', 'SecretAccessKey': 'REDACTED', 'SessionToken': 'REDACTED'}   

## action: 'list detectors'
Lists detectorIds of all the existing Amazon GuardDuty detector resources

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.data.\*.CreatedAt | string |  |   2018-11-14T23:10:26.234Z 
action_result.data.\*.DataSources.CloudTrail.Status | string |  |   ENABLED 
action_result.data.\*.DataSources.DNSLogs.Status | string |  |   ENABLED 
action_result.data.\*.DataSources.FlowLogs.Status | string |  |   ENABLED 
action_result.data.\*.DataSources.S3Logs.Status | string |  |   DISABLED 
action_result.data.\*.DetectorId | string |  `aws guardduty detector id`  |   7eb38a3ebb7f20c83dcddbc35a46a0a4 
action_result.data.\*.FindingPublishingFrequency | string |  |   SIX_HOURS 
action_result.data.\*.ServiceRole | string |  |   arn:aws:iam::849257271967:role/aws-service-role/guardduty.amazonaws.com/AWSServiceRoleForAmazonGuardDuty 
action_result.data.\*.Status | string |  |   ENABLED 
action_result.data.\*.UpdatedAt | string |  |   2018-11-14T23:10:26.234Z 
action_result.summary.total_detectors | numeric |  |   0  1 
action_result.message | string |  |   Total detectors: 0  Total detectors: 1 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 
action_result.parameter.credentials | string |  `aws credentials`  |   {'AccessKeyId': 'REDACTED', 'Expiration': 'REDACTED', 'SecretAccessKey': 'REDACTED', 'SessionToken': 'REDACTED'} 