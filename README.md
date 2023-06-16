# ansible-role-mongo #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-mongo/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-mongo/actions)
[![CodeQL](https://github.com/cisagov/ansible-role-mongo/workflows/CodeQL/badge.svg)](https://github.com/cisagov/ansible-role-mongo/actions/workflows/codeql-analysis.yml)

An Ansible role for installing [MongoDB](https://www.mongodb.com/).

## Requirements ##

None.

## Role Variables ##

None.

<!--
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| optional_variable | Describe its purpose. | `default_value` | No |
| required_variable | Describe its purpose. | n/a | Yes |
-->

## Dependencies ##

- [cisagov/ansible-role-disable-numa](https://github.com/cisagov/ansible-role-disable-numa)
- [GekoCloud/ansible-role-disable-thp](https://github.com/GekoCloud/ansible-role-disable-thp)
- [cisagov/ansible-role-numactl](https://github.com/cisagov/ansible-role-numactl)
- [cisagov/ansible-role-pip](https://github.com/cisagov/ansible-role-pip)
- [cisagov/ansible-role-python](https://github.com/cisagov/ansible-role-python)

## Example Playbook ##

Here's how to use it in a playbook:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  tasks:
    - name: Install MongoDB
      ansible.builtin.include_role:
        name: mongo
```

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.

## Author Information ##

Shane Frasier - <jeremy.frasier@gwe.cisa.dhs.gov>
