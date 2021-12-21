[comment]: # "Auto-generated SOAR connector documentation"
# AWS GuardDuty

Publisher: Splunk  
Connector Version: 2\.1\.6  
Product Vendor: AWS  
Product Name: GuardDuty  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This app integrates with AWS GuardDuty to investigate findings

[comment]: # " File: readme.md"
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

      

-   **Scheduled\|Interval Polling**

      

    -   The scheduled\|interval polling fetches the findings (in oldest first order to ensure zero
        data loss) based on the same logic of the manual polling for the first run. The 'updatedAt'
        time of the last fetched finding gets stored in this first run.
    -   For the consecutive runs, the findings get fetched after the stored 'updatedAt' time in the
        previous run.
    -   If the `         filter_name        ` gets changed at an intermediate stage of the
        scheduled\|interval polling, the next run of polling will auto-detect the change and it will
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
**access\_key** |  optional  | password | AWS Access Key
**secret\_key** |  optional  | password | AWS Secret Key
**region** |  required  | string | AWS Region
**filter\_name** |  optional  | string | Name of the saved filter on UI of AWS GuardDuty
**poll\_now\_days** |  optional  | numeric | Number of days prior current date to start polling \(Default\: 30\)
**use\_role** |  optional  | boolean | Use attached role when running Phantom in EC2

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[on poll](#action-on-poll) - Callback action for the on\_poll ingest functionality  
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
Callback action for the on\_poll ingest functionality

Type: **ingest**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container\_id** |  optional  | Container IDs to limit the ingestion to | string | 
**start\_time** |  optional  | Start of time range, in epoch time \(milliseconds\) | numeric | 
**end\_time** |  optional  | End of time range, in epoch time \(milliseconds\) | numeric | 
**container\_count** |  optional  | Maximum number of container records to query for | numeric | 
**artifact\_count** |  optional  | Maximum number of artifact records to query for | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'update finding'
Updates specified Amazon GuardDuty findings as useful or not useful

Type: **generic**  
Read only: **False**

For the parameter 'finding\_id', if the user provides comma\-separated values and one or more values are invalid, then those values will be simply ignored and only correct values will be used for further processing\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector\_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**finding\_id** |  required  | The IDs of the findings \(Comma separated IDs allowed\) | string |  `aws guardduty finding id` 
**feedback** |  required  | Feedback value of the finding | string | 
**comment** |  optional  | Additional feedback about the finding | string | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.comment | string | 
action\_result\.parameter\.detector\_id | string |  `aws guardduty detector id` 
action\_result\.parameter\.feedback | string | 
action\_result\.parameter\.finding\_id | string |  `aws guardduty finding id` 
action\_result\.data | string | 
action\_result\.summary\.total\_updated\_findings | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'run query'
Fetch the findings as per the filters applied

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector\_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**instance\_id** |  optional  | The ID of the EC2 instance | string |  `aws guardduty instance id` 
**severity** |  optional  | The severity of the finding | string |  `aws guardduty severity` 
**public\_ip** |  optional  | Public IP address of the EC2 instance | string |  `ip` 
**private\_ip** |  optional  | Private IP address of the EC2 instance | string |  `ip` 
**limit** |  optional  | The maximum number of results to be fetched\. If not provided, then all the results will be fetched | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.detector\_id | string |  `aws guardduty detector id` 
action\_result\.parameter\.instance\_id | string |  `aws guardduty instance id` 
action\_result\.parameter\.limit | numeric | 
action\_result\.parameter\.private\_ip | string |  `ip` 
action\_result\.parameter\.public\_ip | string |  `ip` 
action\_result\.parameter\.severity | string |  `aws guardduty severity` 
action\_result\.data\.\*\.AccountId | string | 
action\_result\.data\.\*\.Arn | string | 
action\_result\.data\.\*\.CreatedAt | string | 
action\_result\.data\.\*\.Description | string | 
action\_result\.data\.\*\.Id | string |  `aws guardduty finding id` 
action\_result\.data\.\*\.NextToken | string | 
action\_result\.data\.\*\.Partition | string | 
action\_result\.data\.\*\.Region | string | 
action\_result\.data\.\*\.Resource\.AccessKeyDetails\.AccessKeyId | string | 
action\_result\.data\.\*\.Resource\.AccessKeyDetails\.PrincipalId | string | 
action\_result\.data\.\*\.Resource\.AccessKeyDetails\.UserName | string | 
action\_result\.data\.\*\.Resource\.AccessKeyDetails\.UserType | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.AvailabilityZone | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.IamInstanceProfile\.Arn | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.IamInstanceProfile\.Id | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.ImageDescription | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.ImageId | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.InstanceId | string |  `aws guardduty instance id` 
action\_result\.data\.\*\.Resource\.InstanceDetails\.InstanceState | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.InstanceType | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.LaunchTime | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.NetworkInterfaceId | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.PrivateDnsName | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.PrivateIpAddress | string |  `ip` 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.PrivateDnsName | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.PrivateIpAddresses\.\*\.PrivateIpAddress | string |  `ip` 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.PublicDnsName | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.PublicIp | string |  `ip` 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.SecurityGroups\.\*\.GroupId | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.SecurityGroups\.\*\.GroupName | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.SubnetId | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.NetworkInterfaces\.\*\.VpcId | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.Tags\.\*\.Key | string | 
action\_result\.data\.\*\.Resource\.InstanceDetails\.Tags\.\*\.Value | string | 
action\_result\.data\.\*\.Resource\.ResourceType | string | 
action\_result\.data\.\*\.SchemaVersion | string | 
action\_result\.data\.\*\.Service\.Action\.ActionType | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.Api | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.CallerType | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.ErrorCode | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.RemoteIpDetails\.City\.CityName | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.RemoteIpDetails\.Country\.CountryName | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.RemoteIpDetails\.GeoLocation\.Lat | numeric | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.RemoteIpDetails\.GeoLocation\.Lon | numeric | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.RemoteIpDetails\.IpAddressV4 | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.RemoteIpDetails\.Organization\.Asn | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.RemoteIpDetails\.Organization\.AsnOrg | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.RemoteIpDetails\.Organization\.Isp | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.RemoteIpDetails\.Organization\.Org | string | 
action\_result\.data\.\*\.Service\.Action\.AwsApiCallAction\.ServiceName | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.Blocked | boolean | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.ConnectionDirection | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.LocalIpDetails\.IpAddressV4 | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.LocalPortDetails\.Port | numeric | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.LocalPortDetails\.PortName | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.Protocol | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemoteIpDetails\.City\.CityName | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemoteIpDetails\.Country\.CountryName | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemoteIpDetails\.GeoLocation\.Lat | numeric | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemoteIpDetails\.GeoLocation\.Lon | numeric | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemoteIpDetails\.IpAddressV4 | string |  `ip` 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemoteIpDetails\.Organization\.Asn | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemoteIpDetails\.Organization\.AsnOrg | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemoteIpDetails\.Organization\.Isp | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemoteIpDetails\.Organization\.Org | string | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemotePortDetails\.Port | numeric | 
action\_result\.data\.\*\.Service\.Action\.NetworkConnectionAction\.RemotePortDetails\.PortName | string | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.Blocked | boolean | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.LocalPortDetails\.Port | numeric | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.LocalPortDetails\.PortName | string | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.RemoteIpDetails\.City\.CityName | string | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.RemoteIpDetails\.Country\.CountryName | string | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.RemoteIpDetails\.GeoLocation\.Lat | numeric | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.RemoteIpDetails\.GeoLocation\.Lon | numeric | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.RemoteIpDetails\.IpAddressV4 | string |  `ip` 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.RemoteIpDetails\.Organization\.Asn | string | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.RemoteIpDetails\.Organization\.AsnOrg | string | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.RemoteIpDetails\.Organization\.Isp | string | 
action\_result\.data\.\*\.Service\.Action\.PortProbeAction\.PortProbeDetails\.\*\.RemoteIpDetails\.Organization\.Org | string | 
action\_result\.data\.\*\.Service\.Archived | boolean | 
action\_result\.data\.\*\.Service\.Count | numeric | 
action\_result\.data\.\*\.Service\.DetectorId | string |  `md5` 
action\_result\.data\.\*\.Service\.EventFirstSeen | string | 
action\_result\.data\.\*\.Service\.EventLastSeen | string | 
action\_result\.data\.\*\.Service\.Evidence\.ThreatIntelligenceDetails\.\*\.ThreatListName | string | 
action\_result\.data\.\*\.Service\.ResourceRole | string | 
action\_result\.data\.\*\.Service\.ServiceName | string | 
action\_result\.data\.\*\.Service\.UserFeedback | string | 
action\_result\.data\.\*\.Severity | string |  `aws guardduty severity` 
action\_result\.data\.\*\.Title | string | 
action\_result\.data\.\*\.Type | string | 
action\_result\.data\.\*\.UpdatedAt | string | 
action\_result\.summary\.total\_findings | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'archive finding'
Archives Amazon GuardDuty findings specified by the detector ID and list of finding IDs

Type: **contain**  
Read only: **False**

For the parameter 'finding\_id', if the user provides comma\-separated values and one or more values are invalid, then those values will be simply ignored and only correct values will be used for further processing\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector\_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**finding\_id** |  required  | The IDs of the findings \(Comma separated IDs allowed\) | string |  `aws guardduty finding id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.detector\_id | string |  `aws guardduty detector id` 
action\_result\.parameter\.finding\_id | string |  `aws guardduty finding id` 
action\_result\.data | string | 
action\_result\.summary\.total\_findings | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'unarchive finding'
Unarchives Amazon GuardDuty findings specified by the detector ID and list of finding IDs

Type: **correct**  
Read only: **False**

For the parameter 'finding\_id', if the user provides comma\-separated values and one or more values are invalid, then those values will be simply ignored and only correct values will be used for further processing\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector\_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**finding\_id** |  required  | The IDs of the findings \(Comma separated IDs allowed\) | string |  `aws guardduty finding id` 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.detector\_id | string |  `aws guardduty detector id` 
action\_result\.parameter\.finding\_id | string |  `aws guardduty finding id` 
action\_result\.data | string | 
action\_result\.summary\.total\_findings | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'list filters'
Returns a paginated list of the current filters

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector\_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**limit** |  optional  | The maximum number of filters to be fetched | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.detector\_id | string |  `aws guardduty detector id` 
action\_result\.parameter\.limit | numeric | 
action\_result\.data\.\*\.Action | string | 
action\_result\.data\.\*\.Description | string | 
action\_result\.data\.\*\.FilterName | string | 
action\_result\.data\.\*\.FindingCriteria\.Criterion\.id\.Eq | string | 
action\_result\.data\.\*\.FindingCriteria\.Criterion\.resource\.instanceDetails\.instanceId\.Eq | string | 
action\_result\.data\.\*\.FindingCriteria\.Criterion\.service\.archived\.Eq | string | 
action\_result\.data\.\*\.FindingCriteria\.Criterion\.severity\.Eq | string | 
action\_result\.data\.\*\.FindingCriteria\.Criterion\.updatedAt\.GreaterThan | numeric | 
action\_result\.data\.\*\.FindingCriteria\.Criterion\.updatedAt\.Gt | numeric | 
action\_result\.data\.\*\.FindingCriteria\.Criterion\.updatedAt\.LessThan | numeric | 
action\_result\.data\.\*\.FindingCriteria\.Criterion\.updatedAt\.Lt | numeric | 
action\_result\.data\.\*\.Name | string | 
action\_result\.data\.\*\.Rank | numeric | 
action\_result\.summary\.total\_filters | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'list threats'
Lists the ThreatIntelSets of the GuardDuty service specified by the detector ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector\_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**limit** |  optional  | The maximum number of threat intel sets to be fetched\. If not provided, then all the threat intel sets will be fetched | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.detector\_id | string |  `aws guardduty detector id` 
action\_result\.parameter\.limit | numeric | 
action\_result\.data\.\*\.Format | string | 
action\_result\.data\.\*\.Location | string |  `url` 
action\_result\.data\.\*\.Name | string | 
action\_result\.data\.\*\.Status | string | 
action\_result\.data\.\*\.ThreatIntelSetId | string |  `md5` 
action\_result\.summary\.total\_threats | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'list ip sets'
Lists the IPSets of the GuardDuty service specified by the detector ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**detector\_id** |  required  | The ID of the detector | string |  `aws guardduty detector id` 
**limit** |  optional  | The maximum number of IP sets to be fetched\. If not provided, then all the IP sets will be fetched | numeric | 
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.detector\_id | string |  `aws guardduty detector id` 
action\_result\.parameter\.limit | numeric | 
action\_result\.data\.\*\.Format | string | 
action\_result\.data\.\*\.IpSetId | string |  `md5` 
action\_result\.data\.\*\.Location | string |  `url` 
action\_result\.data\.\*\.Name | string | 
action\_result\.data\.\*\.Status | string | 
action\_result\.summary\.total\_ip\_sets | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials`   

## action: 'list detectors'
Lists detectorIds of all the existing Amazon GuardDuty detector resources

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**credentials** |  optional  | Assumed role credentials | string |  `aws credentials` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.data\.\*\.CreatedAt | string | 
action\_result\.data\.\*\.DataSources\.CloudTrail\.Status | string | 
action\_result\.data\.\*\.DataSources\.DNSLogs\.Status | string | 
action\_result\.data\.\*\.DataSources\.FlowLogs\.Status | string | 
action\_result\.data\.\*\.DataSources\.S3Logs\.Status | string | 
action\_result\.data\.\*\.DetectorId | string |  `aws guardduty detector id` 
action\_result\.data\.\*\.FindingPublishingFrequency | string | 
action\_result\.data\.\*\.ServiceRole | string | 
action\_result\.data\.\*\.Status | string | 
action\_result\.data\.\*\.UpdatedAt | string | 
action\_result\.summary\.total\_detectors | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.parameter\.credentials | string |  `aws credentials` 