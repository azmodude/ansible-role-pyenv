pyenv
=====

Install [pyenv](https://github.com/yyuu/pyenv) using [pyenv-installer](https://github.com/yyuu/pyenv-installer).

Requirements
------------

None.

Role Variables
--------------

Available variables are listed below, along with default values (see defaults/main.yml):

    pyenv_user: "{{ ansible_env.USER }}"

Install pyenv for given user.

    pyenv_root: "{{ ansible_env.HOME }}/.pyenv"

Install pyenv into given root.


Dependencies
------------

None.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      vars_files:
        - vars/main.yml
      roles:
         - { role: azmodude.pyenv }

License
-------

BSD

Author Information
------------------

None.
