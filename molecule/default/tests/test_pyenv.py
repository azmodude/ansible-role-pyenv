import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

PYTHON_VERSION = "3.6.3"


def get_ansible_pyenv_users(host):
    """ Get pyenv_users variable from Ansible. """
    return host.ansible.get_variables()['pyenv_users']


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
    user = get_ansible_pyenv_users(host)[0]
    pyenv_location = get_pyenv_root(host, user)

    command = 'PYENV_ROOT={0} {0}/bin/pyenv --version'.format(pyenv_location)
    with host.sudo(user['name']):
        commandoutput = host.run(command)
    assert commandoutput.stdout.startswith('pyenv')


def test_pyenv_compiles(host):
    """ Test whether pyenv is able to compile PYTHON_VERSION. """
    user = get_ansible_pyenv_users(host)[0]
    pyenv_location = get_pyenv_root(host, user)

    command = 'PYENV_ROOT={0} {0}/bin/pyenv install {1}'.\
        format(pyenv_location, PYTHON_VERSION)
    with host.sudo(user['name']):
        commandoutput = host.run(command)
    assert 'Installed Python-{0}'.format(PYTHON_VERSION) in \
        commandoutput.stderr
