# c2platform.tomcat CHANGELOG

This file is used to list changes made in each version of the [c2platform.tomcat](https://github.com/c2platform/ansible-role-tomcat) cookbook.

## 0.1.6 (2022-10-24)

* Moved to GitLab see [c2platform.mw.tomcat](https://gitlab.com/c2platform/ansible-collection-mw/-/blob/master/roles/tomcat/README.md).

## 0.1.4 (2022-05-30)

* tomcat home not world readable using `tomcat_home_dir_mode`.

## 0.1.3 (2022-04-05)

* don't trigger restart handler if `tomcat_service_enabled: false`
* using [c2platform.core.cacerts2](https://github.com/c2platform/ansible-collection-core/tree/master/roles/cacerts2) for certificates

## 0.1.2 (2022-04-01)

* don't trigger restart handler if `tomcat_service_enabled: false`
* using [c2platform.core.cacerts2](https://github.com/c2platform/ansible-collection-core/tree/master/roles/cacerts2) for certificates

## 0.1.1 (2022-03-03)

* removed tasks dependency

## 0.1.0 (2022-02-14)

* initial role
