import os
import json
import subprocess

scriptDir = os.path.dirname(os.path.realpath(__file__))
configFilepath = os.path.join(scriptDir, 'config.json')

def validate_config(config):
  keys = [
    'email',
    'api_key',
    'mailgun_domain',
  ]

  for key in keys:
    if not key in config:
      die('Must specify "{0}" in config.json'.format(keyA))

def sendHTML(senderName, subject, content):
  with open(configFilepath) as configFile:
    config = json.load(configFile)

  validate_config(config)

  command = ' '.join(["/bin/bash -c \"set -o xtrace; set -o errexit; curl", '-s',
    '--user', "'api:{}'".format(config['api_key']),
    'https://api.mailgun.net/v3/{}/messages'.format(config['mailgun_domain']),
    '-F', "from='{} <mailgun@{}>'".format(senderName, config['mailgun_domain']),
    '-F', 'to={}'.format(config['email']),
    '-F', "subject='{}'".format(subject),
    '-F', "html=\\'$'{}'\\'".format(content),
    '\"',
  ])

  return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()

