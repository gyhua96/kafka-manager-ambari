#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
from resource_management import Script
from resource_management.core.logger import Logger
from resource_management.core.resources.system import Execute, File, Directory
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import Direction
from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.check_process_status import check_process_status
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.functions import upgrade_summary
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions.show_logs import show_logs
from resource_management.libraries.resources.properties_file import PropertiesFile

class KafkaManager(Script):
  def install(self, env):
    import params

    # delete  the cmak_home dir
    cmd='rm -rf ' + params.cmak_home
    Execute('echo "Running ' + cmd + '"')
    Execute('echo "deleting cmak home dir if exists."')
    Execute(cmd, ignore_failures=True)

    ensure_base_directories()




    cmd = '/bin/tar' + ' -zxf ' + params.archive_file + ' --strip 1 -C ' + params.cmak_home
    Execute('echo "Running ' + cmd + '"')
    Execute('echo "unzipping cmak files."')
    Execute(cmd)
    Execute('chown -R ' + params.cmak_user + ':' + params.user_group + ' ' + params.cmak_home)

    cmd = '/bin/ln' + ' -s ' + params.cmak_home  + '/bin/kafka-manager /bin/kafka-manager'
    Execute('echo "Running ' + cmd + '"')

    self.configure(env, True)




  def configure(self, env, isInstall=False):
    import params
    env.set_params(params)


    kafka_consumer_config = mutable_config_dict(params.config['configurations']['kafka-consumer'])
    PropertiesFile("consumer.properties",
                      dir=params.conf_dir,
                      properties=kafka_consumer_config,
                      owner=params.cmak_user,
                      group=params.user_group,
    )

    kafka_manager_config = mutable_config_dict(params.config['configurations']['kafka-manager'])
    # kafka_manager_config['kafka-manager.zkhosts'] = '"' + params.zookeeper_connect + '"'
    PropertiesFile("application.conf",
                      dir=params.conf_dir,
                      properties=kafka_manager_config,
                      owner=params.cmak_user,
                      group=params.user_group,
    )


  def stop(self, env):
    import params
    from resource_management.core import sudo
    if params.cmak_pid_file and os.path.isfile(params.cmak_pid_file):
      pid = str(sudo.read_file(params.cmak_pid_file))
      Execute('kill -9 ' + pid, user=params.cmak_user)
    Execute('rm ' + params.cmak_pid_file, ignore_failures=True)


  def start(self, env):
    import params
    self.stop(env)

    self.configure(env)

    cmd = 'nohup ' + params.cmak_bin + ' -Dhttp.port='+ params.port +' -Dplay.server.pidfile.path=' + params.cmak_pid_file + ' -Dapplication.home=/var/log/cmak & '
    Execute('echo "Running ' + cmd + '"')
    Execute('echo "start cmak."')
    Execute(cmd, user=params.cmak_user)


  def status(self, env):
    import params
    check_process_status(params.cmak_pid_file)

def ensure_base_directories():
  import params
  Directory([params.cmak_pid_dir, params.cmak_log_dir, params.cmak_home],
          owner=params.cmak_user,
          group=params.user_group
  )

def mutable_config_dict(config):
  rv = {}
  for key, value in config.iteritems():
    rv[key] = value
  return rv

if __name__ == "__main__":
  KafkaManager().execute()

