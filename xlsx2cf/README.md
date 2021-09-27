=========================
#cf_from_worksheet README
=========================

This script is intended to generate a cloudformation template from an Excel spreadsheet. The spreadsheet should be provided by Systems Engineering and contains all relevant details necessary to create resources (EC2 & RDS Instances). This script is intended to be used across security fabrics.

=========================
##Requirements
=========================
- Python 3
- SE supplied VDD Excel Spreadsheet
- All modules contained in requirements.txt
- Server used to execute commands should have appropriate permissions to kick off CloudFormation Stack

=========================
##Usage
=========================
To create a resource by supplying an Instance Name (ex. Auto-GP-01)
- python3 cf_from_worksheet.py -N <Instance Name> -S <spreadsheet name>

To create a resource by supplying an Instance Hostname (ex. GCAUE1ALAGP01)
- python3 cf_from_worksheet.py -H <Hostname> -S <spreadsheet name>

To create a resource by supplying a Jira Ticket Number (ex. FG-9999)
- python3 cf_from_worksheet.py -J <Jira Ticket Number> -S <spreadsheet name>

