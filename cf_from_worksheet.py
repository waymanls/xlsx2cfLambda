#!/usr/bin/env python
import os
import sys
import json
import yaml
import boto3
import argparse
from datetime import date
from openpyxl import load_workbook
from jinja2 import Environment, FileSystemLoader

def getDatafromSheet(spreadsheet, name, ticketNumber):
	"""
	Query spreadsheet for either hostname or Instance name and pull relevant fields
	"""
	workbook = load_workbook(filename = spreadsheet)
	resourceName = name
	resourceDict = {}
	EC2worksheet = workbook.active
	session = boto3.session.Session()
	print("Hello world")

	for row in EC2worksheet.iter_rows(min_row=2,values_only=True):
		resourceDict['ServerType'] = row[0]
		resourceDict['ResourceType'] = row[1]
		resourceDict['ArchitectureID'] = row[2]
		resourceDict['AvailabilityZone'] = row[3]
		resourceDict['AmiId'] = row[4]
		resourceDict['OS'] = row[5]
		resourceDict['Version'] = row[6]
		resourceDict['InstanceType'] = row[7]
		resourceDict['RootVolSize'] = row[8]
		resourceDict['CloudEnvironment'] = row[9]
		resourceDict['Subnet'] = row[10]
		resourceDict['Environment'] = row[11]
		resourceDict['InstanceName'] = row[12]
		resourceDict['Hostname'] = row[13]
		resourceDict['WebAdaptorName'] = row[14]
		resourceDict['AdditionalVolSize'] = row[15]
		resourceDict['MissionOwner'] = row[16]
		resourceDict['Office'] = row[17]
		resourceDict['Product'] = row[18]
		resourceDict['Startup'] = row[19]
		resourceDict['Shutdown'] = row[20]
		resourceDict['Scheduled'] = row[21]
		resourceDict['SecurityGroup'] = row[22]
#		if name == row[9] or name == row[10]:
#			resourceDict['Domain'] = row[0]
#			resourceDict['Environment'] = row[1]
#			resourceDict['MissionOwner'] = row[2]
#			resourceDict['Office'] = row[3]
#			resourceDict['Product'] = row[4]
#			resourceDict['ArchitectureId'] = row[6]
#			resourceDict['Name'] = row[9]
#			resourceDict['Hostname'] = row[10]
#			resourceDict['ServerType'] = row[11]
#			resourceDict['VolSize'] = row[12]
#			resourceDict['InstanceType'] = row[16]
#			resourceDict['SubnetId'] = row[18]
#			resourceDict['Schedule'] = row[22]
#			resourceDict['Startup'] = row[23]
#			resourceDict['Shutdown'] = row[24]
	if not resourceDict:
		print("=================================================================================")
		print("                                     ERROR                                       ")
		print("=================================================================================")
		print(name + " not found in spreadsheet. Please verify that name is correct")
		print("")
		print("")
		print("Exiting...")
		print("=================================================================================")
		sys.exit()
#	else:
#		# Translate SubnetName to Id since we can evaluate formulas that define subnets in spreadsheet
#		resourceDict['JiraTicket'] = ticketNumber
#		ec2 = boto3.resource('ec2')
#		filters = [{'Name':'tag:Name','Values':[resourceDict['SubnetId']]}]
#		subnet = list(ec2.subnets.filter(Filters=filters))
#		resourceDict['SubnetId'] = str(subnet[0]).split('\'')[1]

	return resourceDict

#def genTemplate(resourceDict):
def genTemplate(spreadsheet):
	"""
	Generate Cloudformatin template using jinja2 using values from Spreadsheet
	"""
	env = Environment(loader = FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
	template = env.get_template('Server.template.jinja2')
	workbook = load_workbook(filename = spreadsheet)
	EC2worksheet = workbook.active
	#print(EC2worksheet['B2'].value)
	# Print each row, and generate a template based on the value in column
	# if resource is defined in spreadsheet include it in template, otherwise, don't
	for row in EC2worksheet.iter_rows(min_row=2,values_only=True):
            if row[1] == 'EC2':
                #print(spreadsheet, row[0], workbook.active.title)
                templateValues = getDatafromSheet(spreadsheet, row[0], workbook.active.title)
                print(template.render(templateValues))
            #if row[1] == 'RDS':
                #print("Generate RDS Resource Section")
	# print(template.render(resourceDict))
	# cfTemplate = template.render(resourceDict)

	#return cfTemplate

def buildStack(cfTemplate,ticketNumber,resourceName):
	"""
	Create CloudFormation stack using template generated in genTemplate()
	"""
	stackName = resourceName + "-" + ticketNumber + "-" + str(date.today())
	client = boto3.client('cloudformation')
	parameterFile = open("GovCloud-Automation-Test-Servers.json","r")
	params = json.load(parameterFile)
	response = client.create_stack(StackName=stackName,TemplateBody=cfTemplate,DisableRollback=True,Parameters=params)
	print("==============================================================================")
	print("                                  SUCCESS                                     ")
	print("==============================================================================")
	print("Stack has been created, please track progress in CloudFormation Web Console")
	print("==============================================================================")
	print(response['StackId'])
	print("==============================================================================")
	parameterFile.close()

def fileCheck():
	"""
	Check to see if jinja template and parameter files are in place
	"""
	if not os.path.exists("GovCloud-Automation-Test-Servers.json") or not os.path.exists("Server.template.jinja2"):
		sys.exit()
def main():
	parser = argparse.ArgumentParser(description="Tool to create server from spreadsheet via CloudFormation")
	parser.add_argument('-S', '--spreadsheet', help='Path to spreadsheet') 	
	args = parser.parse_args()
	cfTemplate = genTemplate(args.spreadsheet)

if __name__ == '__main__':
	main()
