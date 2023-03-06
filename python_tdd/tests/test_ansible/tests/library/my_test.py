#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

import ansible.module_utils.basic

__metaclass__ = type

class CustomAnsibleModule:

    def __init__(self):
        self.result = self.get_default_results()
        self.module = self.get_ansible_module(self.get_user_arguments())
        self.exit_if_exclusively_check_mode()
        self.update_results()
        self.module_changed()
        self.check_for_failure()
        self.exit()

    @staticmethod
    def get_user_arguments():
        # define available arguments/parameters a user can pass to the module
        return dict(
            name=dict(type='str', required=True),
            new=dict(type='bool', required=False, default=False)
        )

    @staticmethod
    def get_default_results():
        # seed the result dict in the object
        # we primarily care about changed and state
        # changed is if this module effectively modified the target
        # state will include any data that you want your module to pass back
        # for consumption, for example, in a subsequent task
        return dict(
            changed=False,
            original_message='',
            message=''
        )

    @staticmethod
    def get_ansible_module(module_args):
        # the AnsibleModule object will be our abstraction working with Ansible
        # this includes instantiation, a couple of common attr would be the
        # args/params passed to the execution, as well as if the module
        # supports check mode
        return ansible.module_utils.basic.AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

    def exit_if_exclusively_check_mode(self):
        # if the user is working with this module in only check mode we do not
        # want to make any changes to the environment, just return the current
        # state with no modifications
        if self.module.check_mode:
            module.exit_json(**self.result)

    def update_results(self):
        # manipulate or modify the state as needed (this is going to be the
        # part where your module will do what it needs to do)
        self.result['original_message'] = self.module.params['name']
        self.result['message'] = 'goodbye'

    def module_changed(self):
        # use whatever logic you need to determine whether or not this module
        # made any modifications to your target
        if self.module.params['new']:
            self.result['changed'] = True

    def check_for_failure(self):
        # during the execution of the module, if there is an exception or a
        # conditional state that effectively causes a failure, run
        # AnsibleModule.fail_json() to pass in the message and the result
        if self.module.params['name'] == 'fail me':
            self.module.fail_json(msg='You requested this to fail', **self.result)

    def exit(self):
        # in the event of a successful module execution, you will want to
        # simple AnsibleModule.exit_json(), passing the key/value results
        self.module.exit_json(**self.result)


def main():
    CustomAnsibleModule()

if __name__ == '__main__':
    main()
