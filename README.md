ansible-role-pyenv
==================

[![Build Status](https://travis-ci.org/azmodude/ansible-role-pyenv.svg?branch=master)](https://travis-ci.org/azmodude/ansible-role-pyenv)

Install [pyenv](https://github.com/yyuu/pyenv) using [pyenv-installer](https://github.com/yyuu/pyenv-installer).

Requirements
------------

None.

Role Variables
--------------

Available variables are listed below, along with default values (see defaults/main.yml):

    pyenv_users:
      - name: user_a
      - name: user_b
        root: .pyenv_alternate

Install pyenv for given user(s). Default `pyenv_root` is set in `defaults/main.yml` (defaults to `.pyenv`); specifying `root` for a pyenv\_user overrides it.

Dependencies
------------

None.

Example Playbook
----------------

    - hosts: servers
      vars_files:
        - vars/main.yml
      roles:
        - role: azmodude.pyenv
          pyenv_users:
            - name: user_a
            - name: user_b
              root: .pyenv_alternate

License
-------

MIT

Author Information
------------------

None.
