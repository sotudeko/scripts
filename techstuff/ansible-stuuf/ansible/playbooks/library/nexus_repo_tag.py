#!/usr/bin/python

DOCUMENTATION = '''
---
module: nexus_repo_tag
short_description: Manage your tags in Nexus Repository 
'''

EXAMPLES = '''
- name: Create a tag
  nexus_repo_tag:
    tag_name: "tag name"
    repo_name: "repository name",
    description: "This is your first repository"
    state: present
  register: result

- name: Delete a tag
  nexus_repo_tag:
    tag_name: "tag name"
    repo_name: "repository name",
    state: absent
  register: result
'''

from ansible.module_utils.basic import *

def nexus_repo_tag_present(data):
	has_changed = False
	#meta = {"present": "not yet implemented"}
	#return (has_changed, meta)
        new_module_args = ()
        new_module_args.update(
            dict(
                url="http://localhost:8081/service/rest/beta/tags",
                method=POST,
                user="admin",
                password="admin123",
                body='{ "name": "Ansible-Demo-15", "attributes": { "user": "sotudeko", "type": "ansible type", "id": "14" } }',
                force_basic_auth=yes,
                body_format=json
            ),
        )
        result.update(
            self._execute_module(
                module_name='uri',
                module_args=new_module_args,
                task_vars=task_vars,
                tmp=tmp,
                delete_remote_tmp=False,
            )
        )


        if result.get('changed', False) and self._play_context.diff:
                result['diff'] = diff

	return result

def nexus_repo_tag_absent(data=None):
	has_changed = False
	meta = {"absent": "not yet implemented"}
	return (has_changed, meta)

def main():

	#sh 'curl -s -X POST -u admin:admin123 -H "Content-Type: application/json" -d @$TAG_FILE http://localhost:8081/service/rest/beta/tags'

	fields = {
		"tag_name": {"required": True, "type": "str"},
		"repo_name": {"required": True, "type": "str"},
		"state": {
			"default": "present", 
			"choices": ['present', 'absent'],  
			"type": 'str' 
		},
	}

	choice_map = {
		"present": nexus_repo_tag_present,
		"absent": nexus_repo_tag_absent, 
	}

	module = AnsibleModule(argument_spec=fields)
	has_changed, result = choice_map.get(module.params['state'])(module.params)
	module.exit_json(changed=has_changed, meta=result)


if __name__ == '__main__':
    main()

