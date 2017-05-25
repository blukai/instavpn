import platform, os, logging_subprocess, random, string, logging, sys, fileinput

logger = logging.getLogger()

string_pool = string.ascii_letters + string.digits
gen_random_text = lambda s: ''.join(map(lambda _: random.choice(string_pool), range(s)))

def run_command(cmd):
    return not (logging_subprocess.call(cmd,
            stdout_log_level=logging.DEBUG,
            stderr_log_level=logging.DEBUG,
            shell=True))

def check_os():
    if platform.linux_distribution() != ('Ubuntu', '14.04', 'trusty'):
        logger.debug('OS: ' + ' '.join(platform.linux_distribution()))
        return False
    return True

def not_sudo():
    return os.getuid() != 0

def install_packages():
    logger.debug('Update package lists')
    if not run_command("apt-get update"):
        return False

    logger.debug('Update packages')
    if not run_command("apt-get -y upgrade"):
        return False

    logger.debug('Install vnstat')
    if not run_command("apt-get install -y vnstat"):
        return False

    logger.debug('Install VPN server packages')
    if not run_command("DEBIAN_FRONTEND=noninteractive apt-get install -q -y openswan xl2tpd ppp lsof"):
        return False

    return True


def setup_sysctl():
    if not run_command("sh files/sysctl.sh"):
        return False
    return True


def setup_passwords():
    try:
        char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits
        f = open('/etc/ppp/chap-secrets', 'w')
        pw1 = gen_random_text(12)
        pw2 = gen_random_text(12)
        f.write("username1 l2tpd {} *\n".format(pw1))
        f.write("username2 l2tpd {} *".format(pw2))
        f.close()
        f = open('/etc/ipsec.secrets', 'w')
        f.write('1.2.3.4 %any: PSK "{}"'.format(gen_random_text(16)))
        f.close()
    except:
        logger.exception("Exception creating passwords:")
        return False

    return True

def cp_configs():
    logger.debug('xl2tpd.conf')
    if not run_command("cp files/xl2tpd.conf /etc/xl2tpd/xl2tpd.conf"):
        return False

    logger.debug('options.xl2tpd')
    if not run_command("cp files/options.xl2tpd /etc/ppp/options.xl2tpd"):
        return False

    logger.debug('ipsec.conf.template')
    if not run_command("cp files/ipsec.conf.template /etc/ipsec.conf.template"):
        return False

    return True

def setup_vpn():
    logger.debug('Write setup-vpn.sh to /etc')
    if not run_command("cp files/setup-vpn.sh /etc/setup-vpn.sh"):
        return False

    logger.debug('Add to rc.local')
    try:
        open("/etc/rc.local", "w").write("bash /etc/setup-vpn.sh\n" + open("/etc/rc.local").read())
    except:
        logger.exception("Exception setting up vpn:")
        return False

    logger.debug('Execute setup-vpn.sh')
    if not run_command("bash /etc/setup-vpn.sh"):
        return False

    logger.debug('Ufw default forward policy')

    try:
        for line in fileinput.input("/etc/default/ufw", inplace=True):
            print line.replace('DEFAULT_FORWARD_POLICY="DROP"', 'DEFAULT_FORWARD_POLICY="ACCEPT"'),
        run_command("service ufw restart")
    except OSError as e:
        logger.warn('ufw not found')

    logger.debug('Copy CLI')
    if not run_command("chmod +x files/instavpn && cp files/instavpn /usr/bin/instavpn"):
        return False

    return True

def info():
    logger.info('')

    logger.info("Completed. Run 'instavpn -h' for help")
