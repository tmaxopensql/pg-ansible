from conftest import get_pg_unix_socket_dir, get_primary, get_standbys, load_ansible_vars


def test_setup_replication_user():
    ansible_vars = load_ansible_vars()
    pg_user = ansible_vars["pg_owner"]

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Select * from pg_user where usename = 'repuser' and userepl = 't'"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, "repuser was not succesfully created"


def test_setup_replication_slots():
    ansible_vars = load_ansible_vars()
    pg_user = ansible_vars["pg_owner"]

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Select * from pg_replication_slots"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip().split("\n")

    assert len(result) > 0, "Replication did not create replication slots"


def test_setup_replication_stat_replication():
    ansible_vars = load_ansible_vars()
    pg_user = ansible_vars["pg_owner"]

    host = get_primary()
    rep_count = len(get_standbys())
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Select application_name from pg_stat_replication"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip().split("\n")

    assert len(result) == rep_count, "Replication was not successful on master"


def test_setup_replication_stat_wal_receiver():
    ansible_vars = load_ansible_vars()
    pg_user = ansible_vars["pg_owner"]

    hosts = get_standbys()
    socket_dir = get_pg_unix_socket_dir()
    res = []

    for host in hosts:
        with host.sudo(pg_user):
            query = "Select slot_name from pg_stat_wal_receiver"
            cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
            result = cmd.stdout.strip().split("\n")

        if len(result) > 0:
            res.append(result)

    assert len(res) == len(hosts), "Replication was not successful on standby(s)"
