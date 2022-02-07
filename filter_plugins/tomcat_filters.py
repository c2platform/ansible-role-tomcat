"""tomcat filters."""
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


# Return properties for element in servers.xml
def tomcat_server_xml_properties(xml_props):
    # pprint({'ds_cmd(cmd_config)': cmd_config})
    xml = ''
    for k in xml_props:
        if k == 'state':
            continue
        v = xml_props[k]
        xml += '{}="{}" '.format(k, v)
    return xml


class FilterModule(object):
    """ansible filters."""

    def filters(self):
        return {
            'tomcat_server_xml_properties': tomcat_server_xml_properties,
        }
