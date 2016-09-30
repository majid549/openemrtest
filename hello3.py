#!/usr/bin/python

import os
import subprocess
import fileinput
import ConfigParser

parser = ConfigParser.RawConfigParser()
config = {}

parser.add_section('platform')
parser.add_section('configure')
parser.add_section('git_repo')
parser.add_section('git_repo_cred')
parser.add_section('CI')
parser.add_section('art_repo')
parser.add_section('CD')
parser.add_section('dep_plat')
parser.add_section('chatops')


def menu(prompt, choices):
    print '\n\n{0}\n'.format(prompt)
    count = len(choices)
    for i in range(count):
        print '({0}) {1}'.format(i + 1, choices[i])
    response = 0
    while response < 1 or response > count:
        response = raw_input('    Type a number (1-{0}): '.format(count))
        if response.isdigit():
            response = int(response)
        else:
            response = 0
    return response

def do_configuration():

    bashCommand = 'mkdir -p ~/.aws'
    bashCommand1 = 'echo "[default]" > ~/.aws/config'
    bashCommand2 = 'echo "output = json" >> ~/.aws/config'
    bashCommand3 = 'echo "region = us-west-2" >> ~/.aws/config'
    bashCommand4 = 'echo "[default]" > ~/.aws/credentials'
    bashCommand5 = 'echo "aws_access_key_id = replace" >> ~/.aws/credentials'
    bashCommand6 = 'echo "aws_secret_access_key = here" >> ~/.aws/credentials'
    os.system(bashCommand)
    os.system(bashCommand1)
    os.system(bashCommand2)
    os.system(bashCommand3)
    os.system(bashCommand4)
    os.system(bashCommand5)
    os.system(bashCommand6)

    access_key_id = raw_input("Please enter your AWS_access_key_id: ")
    config['access_key_id'] = access_key_id
    parser.set('configure', 'access_key_id', access_key_id)

    f = open('/root/.aws/credentials','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace("replace",access_key_id)
    f = open('/root/.aws/credentials','w')
    f.write(newdata)
    f.close()

    secret_access_key = raw_input("please enter your AWS_secret_access_key: ")
    config['secret_access_key'] = secret_access_key 
    parser.set('configure', 'secret_access_key', secret_access_key)

    f = open('/root/.aws/credentials','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace("here",secret_access_key)
    f = open('/root/.aws/credentials','w')
    f.write(newdata)
    f.close()
   
    region = raw_input("please enter the region in which you want to launch application: ")
    config['region'] = region
    parser.set('configure', 'region', region)
   
    f = open('/root/.aws/config','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace("us-west-2",region)
    f = open('/root/.aws/config','w')
    f.write(newdata)
    f.close()

    input_format = raw_input("please enter the input format(default json): ")
    config['input_format'] = input_format
    parser.set('configure', 'input_format', input_format)

    f = open('/root/.aws/config','r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace("json",input_format)
    f = open('/root/.aws/config','w')
    f.write(newdata)
    f.close()
    print "input saved"
    options()

def choose_scm():
    response = menu('Choose SCM Tool', ['On Premise Git Server', 'BitBucket', 'GitHub', 'GitLab' ])
    if response == 1:
     parser.set('git_repo','repository','on_prem_git')
     bashCommand3 = "yum install git-all -y"
     os.system(bashCommand3)
     config['scm_tool'] = 'On Premise Git Server'
     show_status()
     options()
    
    elif response == 2:
     config['scm_tool'] = 'BitBucket'
     parser.set('git_repo','repository','BitBucket')
     url = raw_input("please enter git repository URL (ends with .git) : ")
     config['git_url'] = url
     username  = raw_input("please enter username of git repository : ")
     config['git_username'] = username
     parser.set('git_repo_cred','username',username)
     password  = raw_input("please enter password of git repository : ")
     config['git_password'] = password
     parser.set('git_repo_cred','password',password)
     show_status()
     options()

    elif response == 3:
     config['scm_tool'] = 'Github'
     parser.set('git_repo','repository','GitHub')
     url = raw_input("please enter git repository URL (ends with .git) : ")
     config['git_url'] = url
     username  = raw_input("please enter username of git repository : ")
     config['git_username'] = username
     parser.set('git_repo_cred','username',username)
     password  = raw_input("please enter password of git repository : ")
     config['git_password'] = password
     parser.set('git_repo_cred','password',password)
     show_status()
     options()

    elif response == 4:
     config['scm_tool'] = 'GitLab'
     parser.set('git_repo','repository','GitLab')
     url = raw_input("please enter git repository URL (ends with .git) : ")
     config['git_url'] = url
     username  = raw_input("please enter username of git repository : ")
     config['git_username'] = username
     parser.set('git_repo_cred','username',username)
     password  = raw_input("please enter password of git repository : ")
     config['git_password'] = password
     parser.set('git_repo_cred','password',password)
     show_status()
     options()

def choose_ci():
    response = menu('Choose CI Server', ['Jenkins', 'Bamboo', 'Teamcity', 'TFS', 'Circle CI' ])
    if response == 1:
     parser.set('CI','ci','Jenkins')
     print "response recorded"
     config['ci_server'] = 'jenkins'
     show_status()
     options()

    if response == 2:
     parser.set('CI','ci','Bamboo')
     print "not implemented yet"
     config['ci_server'] = 'bamboo'
     show_status()
     options()

    if response == 3:
     parser.set('CI','ci','Teamcity')
     print "not yet implemented"
     config['ci_server'] = 'teamcity'
     show_status()
     options()

    if response == 4:
     parser.set('CI','ci','TFS')
     print "not yet implemented"
     config['ci_server'] = 'tfs'
     show_status()
     options()

    if response == 5:
     parser.set('CI','ci','CircleCI')
     print "not yet implemented"
     config['ci_server'] = 'circleci'
     show_status()
     options()	 
	 
def choose_artif_repo():
    response = menu('Choose Artifact Repository', ['nexus'])
    if response == 1:
     parser.set('art_repo','artifatct_repo','nexus')
     print "\n\t\t\t\t\tyour selected repository is nexus"
     config['artif_repo'] = 'nexus'
     show_status()
     options()

def choose_deploy_tool():
     response = menu('Choose deployment tool', ['Rundeck', 'Octopus Deploy'])
     if response == 1:
      parser.set('CD','CD_Tool','Rundeck')
      print "\n\t\t\t\t\tyour selected deployment tool is Rundeck"
      config['dep_tool'] = 'rundeck'
      show_status()
      options()
     if response == 2:
      parser.set('CD','CD_Tool','OctopusDeploy')
      print "\n\t\t\t\tnot yet implemented"
      config['dep_tool'] = 'octopus'
      show_status()
      options()

def choose_deployment_platform():
     response = menu('Choose deployment platform', ['IaaS', 'PaaS'])
     if response == 1:
      parser.set('dep_plat','dep_plat','Iaas')
      print "\n\t\t\t\tdeployment platform selected as Iaas"
      config['dep_plat'] = 'ec2'
      show_status()
      options()
     if response == 2:
      parser.set('dep_plat','dep_plat','Paas')
      print "\n\t\t\t\tnot yet implemented"
      config['dep_plat'] = 'elasticbeanstalk'
      show_status()
      options()

def  inst_chatops():
     response = menu('Do you want to install ChatOps', ['Yes', 'No'])
     if response == 1:
      parser.set('chatops','Install','yes')
      print "\n\t\t\t\tYou have opted to install ChatOps"
      config['inst_chatops'] = 'yes'
      show_status()
      options()
     if response == 2:
      parser.set('chatops','Install','no')
      print "\n\t\t\t\tYou have opted not to install ChatOps"
      config['inst_chatops'] = 'no'
      show_status()
      options()

def options():
    response = menu('Configuration page', ['Configure AWS Cli', 'Choose SCM', 'Choose CI Server', 'Choose Artifact Repository', 'Choose Deployment Tool', 'Choose Deployemt Platform', 'Install ChatOps', 'Back'])
    if response == 1:
     do_configuration()
    if response == 2:
     choose_scm()
    if response == 3:
     choose_ci()
    if response == 4:
     choose_artif_repo()
    if response == 5:
     choose_deploy_tool()
    if response == 6:
     choose_deployment_platform()
    if response == 7:
     inst_chatops()
    if response == 8:
     launch()

def launch():
    response = menu('Select Cloud Platform', ['AWS', 'Azure', 'GCE', 'Back'])
    config['platform'] = int(response)
    if response == 1:
     parser.set('platform', 'cloud', 'AWS')
     options()
    elif response == 2:
     parser.set('platform', 'cloud', 'Azure')
     print "\n\t\t\t\t\tCurrently not supported"
     launch()
    elif response == 3:
     parser.set('platform', 'cloud', 'GCE')
     print "\n\t\t\t\t\tCurrently not supported"
     launch()
    elif response == 99:
     print "thanks for using capgemini CLI"

def load():
    print "Load functionality not yet implemented"
    # Do something

def delete():
    print "delete functionality not yet implemented"
    # Do something

def show_status():
    print "\n\n========================================================="
    print "|You have selected:\t\t\t\t\t|"
    print "---------------------------------------------------------"
    print "|Git repository      :",  config.get("scm_tool"),   "\t\t\t\t"
    print "|CI Server           :",  config.get("ci_server"),  "\t\t\t\t"
    print "|Artifact repository :",  config.get("artif_repo"), "\t\t\t\t"
    print "|Deployment Tool     :",  config.get("dep_tool"),   "\t\t\t\t"
    print "|Deployment Platform :",  config.get("dep_plat"),   "\t\t\t\t"
    print "|Install ChatOps     :",  config.get("inst_chatops"),"\t\t\t\t"
    print "========================================================="

# ======================================================================
# Main program starts here
# ======================================================================

bashCommand2 = "clear"
os.system(bashCommand2)
print"================================================================================================================================="
print"                                                    CAPGEMINI CLI                                                                "
print"================================================================================================================================="
main_menu_response = 0
while main_menu_response != 3:
    main_menu_response = menu('What to do?', ['Create CI/CD Pipeline', 'Delete CI/CD Pipeline', 'Load configuration', 'Exit'])
    if main_menu_response == 1:
        launch()
    elif main_menu_response == 2:
        delete()
    elif main_menu_response == 3:
        load()
    elif main_menu_response == 4:
        break

print "\n\t\t\tThanks For using Capgemini CLI\n\n"
with open('example.cfg', 'wb') as configfile:
    parser.write(configfile)
