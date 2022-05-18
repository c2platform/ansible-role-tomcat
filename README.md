# Ansible Role c2platform.tomcat

[![Linters ( Ansible, YAML )](https://github.com/c2platform/ansible-role-tomcat/actions/workflows/ci.yml/badge.svg)](https://github.com/c2platform/ansible-role-tomcat/actions/workflows/ci.yml) [![Release and deploy to Galaxy](https://github.com/c2platform/ansible-role-tomcat/actions/workflows/release.yml/badge.svg)](https://github.com/c2platform/ansible-role-tomcat/actions/workflows/release.yml)

Install and configure [Apache Tomcat](https://tomcat.apache.org/) on your system.

<!-- MarkdownTOC levels="2,3,4" autolink="true" -->

- [Requirements](#requirements)
  - [Java](#java)
- [Role Variables](#role-variables)
  - [Environment variables](#environment-variables)
  - [Java options JAVA_OPTS](#java-options-java_opts)
  - [Catalina options CATALINA_OPTS](#catalina-options-catalina_opts)
  - [Java CLASSPATH](#java-classpath)
  - [Config from Git](#config-from-git)
    - [Delegate to control node](#delegate-to-control-node)
    - [Custom Git checkout](#custom-git-checkout)
  - [Contexts e.g. ROOT](#contexts-eg-root)
  - [PAM limites](#pam-limites)
  - [Certificate Subject Alternative Names](#certificate-subject-alternative-names)
- [Dependencies](#dependencies)
- [Example Playbook](#example-playbook)
- [Notes](#notes)

<!-- /MarkdownTOC -->

## Requirements

<!-- Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required. -->

### Java

Tomcat requires Java to be installed. `java_home` directory, expose java_home set to Yes.

## Role Variables

<!--  A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well. -->

### Environment variables

To set for example `JAVA_HOME` or `JRE_HOME` in `setenv.sh`

```yaml
tomcat_environment_variables:
  - name: JRE_HOME
    value: "{{ tomcat_jre_home }}"
```
### Java options JAVA_OPTS

Java runtime options aka `JAVA_OPTS` can be configured using `tomcat_java_opts` for example as follows:

```yaml
tomcat_java_opts: >-
  -Xms512m
  -Xmx1024m
```

### Catalina options CATALINA_OPTS

Java runtime options `CATALINA_OPTS` can be configured using `tomcat_catalina_opts` for example as follows.

```yaml
tomcat_catalina_opts: >-
  -Dcom.sun.management.jmxremote.port=8375
  -Dcom.sun.management.jmxremote.ssl=false
  -Dcom.sun.management.jmxremote.authenticate=false
  -Dfile.encoding=UTF-8
  -Dsun.net.inetaddr. ttl=300
  -server
  -Dorg.apache.tomcat.util.http.Parameters.MAX_COUNT=8192
  -Xms3000m
  -Xmx3000m
  -XX:MaxPermSize=500m
  -XX:+UseConcMarkSweepGC
  -XX:+CMSIncrementalMode
  -XX:+PrintGCDateStamps
  -verbose:gc
  -XX:+PrintGCDetails
  -Xloggc:"{{ tomcat_home_version }}/logs/garbage.log"
  -XX:+UseGCLogFileRotation
  -XX:NumberOfGCLogFiles=10
  -XX:GCLogFileSize=100M
  -Djavax.sql.DataSource.Factory=org.apache.commons.dbcp.BasicDataSourceFactory
```

### Java CLASSPATH

To change the Tomcat `CLASSPATH` use `tomcat_classpath` 

```yaml
tomcat_classpath: /etc/tomcat/myapp:/etc/tomcat/otherapp  
```

### Config from Git

Using var `tomcat_git_config` you can fetch additional configuration for applications from a Git repository using [ansible.builtin.git](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html)

```yaml
tomcat_git_config:
  repo: https://github.com/c2platform/tomcat-git-config
```
For each application you can then define one or more configurations file to copy from the Git repository to the file system.

```yaml
tomcat_apps:
  - name: broker
    properties-git:
      files:
        t4_authorization:
          dest: /etc/tomcat/suwinet/broker_t4_authorization.properties
          source: myapp.properties 
```

This will create a clone of the configured repository in `/var/tmp` with prefix `tomcat-git-config`

```bash
root@bkd-brut:~# ls /var/tmp/tomcat-git-config-79971bb80eb8f641c1844d6c060c45c18a87ca81/
LICENSE  myapp.properties  README.md
```

Note: if you want to provide authentication with the URL, the [Ansible git module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html) does not support that directly. You can put the credentials in the URL. 

```yaml
tomcat_git_config:
  repo: {{ githubuser | urlencode }}:{{ githubpassword | urlencode }}@https://github.com/c2platform/tomcat-git-config
```

The git clone will be created by default in directory `tomcat_git_config_parent_dir` which is default `/var/tmp`.

#### Delegate to control node

It is possible to delegate the git clone to the control node using

```yaml
tomcat_git_config_control_node: yes
```

#### Custom Git checkout

The [ansible.builtin.git](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html) module has limitations for example you cannot configure a proxy server. In fact you cannot do any [git configuration](https://www.git-scm.com/book/en/v2/Customizing-Git-Git-Configuration) with this module. Using `tomcat_git_config_script` you can provide your own Git checkout script for example:


```yaml
tomcat_git_config_script: |
  if [ ! -d "{{ tomcat_git_config['dir'] }}" ]; then
    git init {{ tomcat_git_config['dir'] }}
    cd {{ tomcat_git_config['dir'] }}
    git remote add origin {{ tomcat_git_config['repo'] }}
    git config http.proxy {{ tomcat_git_config['proxy'] }}
  fi
  cd {{ tomcat_git_config['dir'] }}  
  git pull origin master
```

### Contexts e.g. ROOT

Using `contexts` `Context` elements can be added for example to make a certain application run in the root context. Example fragment below places an application `ig` in the root context.

```yaml
tomcat_services:
  - name: Catalina
    engine:
      host:
        contexts:
          - path: ''
            docBase: ig
          - path: ROOT
            docBase: ROOT          
```

This fragment will generate for example in `server.xml` the `Context` elements as shown below

```xml
      <Host name="localhost" appBase="webapps" unpackWARS="true" autoDeploy="true" >
        <Valve className="org.apache.catalina.valves.ErrorReportValve" showReport="false" showServerInfo="false"  />
        <Context path="" docBase="ig"  />
        <Context path="ROOT" docBase="ROOT"  />
      </Host>
```
### PAM limites

Using `tomcat_pam_limits_nofile` set PAM limits for example

```yaml
tomcat_pam_limits_nofile:
- limit_type: soft
  value: 65536
- limit_type: hard
  value: 131072
```

### Certificate Subject Alternative Names

Use `tomcat_cert_subject_alt_names` to configure alternative names see [rfc5280](https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.6) and [openssl_csr](https://docs.ansible.com/ansible/latest/collections/community/crypto/openssl_csr_module.html#parameter-subject_alt_name).

```yaml
tomcat_cert_subject_alt_names:
  - DNS:www.my-nice-fqdn.com
  - DNS:my-nice-fqdn.com
```

Note: for the common name default `ansible_fqdn` is used.


## Dependencies

<!--   A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles. -->

* Collection [c2platform.core](https://galaxy.ansible.com/c2platform/core)

## Example Playbook

<!--   Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too: -->

```yaml
---
- name: myapp
  hosts: myapp
  become: yes

  roles:
    - { role: c2platform.core.common,  tags: ["common"] }
    - { role: c2platform.core.java,    tags: ["java"] }
    - { role: c2platform.tomcat,       tags: ["tomcat"] }

```

## Notes

- [java - CATALINA_OPTS vs JAVA_OPTS - What is the difference? - Stack Overflow](https://stackoverflow.com/questions/11222365/catalina-opts-vs-java-opts-what-is-the-difference).

