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
import os
from resource_management.libraries.functions import format
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.version import format_stack_version
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions.stack_features import get_stack_feature_version
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions.get_stack_version import get_stack_version
from resource_management.libraries.functions.is_empty import is_empty
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.get_not_managed_resources import get_not_managed_resources
from resource_management.libraries.functions.setup_ranger_plugin_xml import get_audit_configs, generate_ranger_service_config

# server configurations
config = Script.get_config()
stack_root = Script.get_stack_root()

# Version being upgraded/downgraded to
version = default("/componentVersionMap/KAFKA_MANAGER/KAFKA_MANAGER", None)

# default kafka parameters
cmak_home=format('{stack_root}/{version}/kafka-manager')

user_group = config['configurations']['cluster-env']['user_group']
# params from kafka-manager-env
cmak_user = config['configurations']['kafka-manager-env']['cmak_user']
cmak_log_dir = config['configurations']['kafka-manager-env']['cmak_log_dir']
cmak_pid_dir = config['configurations']['kafka-manager-env']['cmak_pid_dir']
port = config['configurations']['kafka-manager-env']['port']

cmak_bin=cmak_home+'/bin/kafka-manager'
conf_dir=cmak_home+'/conf'

service_package_dir = os.path.realpath(__file__).split('/scripts')[0]
archive_file=os.path.join(service_package_dir, 'files', 'kafka-manager-1.3.3.23.tgz')

cmak_pid_file=cmak_pid_dir + '/cmak.pid'


zookeeper_connect = config['configurations']['kafka-broker']['zookeeper.connect']

