import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

python_version = os.environ['PYTHON_VERSION']


def get_ansible_pyenv_users(host):
    """ Get pyenv_users variable from Ansible. """
    try:
        return host.ansible.get_variables()['pyenv_users']
    except KeyError:
        # No-users-defined testcase, return
        return []


def get_pyenv_root(host, user):
    """ Construct pyenv_root variable from fragments. """
    home = host.user(user['name']).home
    pyenv_root = user.get('root', '.pyenv')
    return "{0}/{1}".format(home, pyenv_root)


def test_pyenv_isinstalled(host):
    """ Test whether pyenv actually installed fine. """

    for user in get_ansible_pyenv_users(host):
        pyenv_root = get_pyenv_root(host, user)

        assert host.file(pyenv_root).is_directory
        assert host.file("{0}/bin/pyenv".format(pyenv_root)).exists


def test_pyenv_executes(host):
    """ Test whether pyenv outputs its version. """
    for user in get_ansible_pyenv_users(host):
        pyenv_root = get_pyenv_root(host, user)

        command = 'PYENV_ROOT={0} {0}/bin/pyenv --version'.format(pyenv_root)
        with host.sudo(user['name']):
            commandoutput = host.run(command)
            assert commandoutput.stdout.startswith('pyenv')


def test_pyenv_compiles(host):
    """ Test whether pyenv is able to compile PYTHON_VERSION. """
    try:
        user = get_ansible_pyenv_users(host)[0]
    except IndexError:
        # No-users-defined testcase, return
        return
    pyenv_location = get_pyenv_root(host, user)

    command = 'PYENV_ROOT={0} {0}/bin/pyenv install {1}'.\
        format(pyenv_location, python_version)
    with host.sudo(user['name']):
        commandoutput = host.run(command)
        assert 'Installed Python-{0}'.format(python_version) in \
            commandoutput.stderr


def test_pyenv_compiled_python(host):
    """ Test whether compiled PYTHON_VERSION acutally works. """
    try:
        user = get_ansible_pyenv_users(host)[0]
    except IndexError:
        # No-users-defined testcase, return
        return
    pyenv_location = get_pyenv_root(host, user)
    command = '{0}/versions/{1}/bin/python --version'.format(
        pyenv_location, python_version)
    with host.sudo(user['name']):
        commandoutput = host.run(command)
        assert python_version in commandoutput.stdout
