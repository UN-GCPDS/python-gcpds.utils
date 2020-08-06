import os
import shutil
from jinja2 import Template
import logging
from colorama import Fore


TEMPLATE_EXTENSION = '.j2'


########################################################################
class Distutils:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, dst: str) -> None:
        """Constructor"""
        self.src = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'template')
        self.dst = dst

        self.collect_data()
        self.clone_pkg()
        self.contextualize()

    # ----------------------------------------------------------------------
    def collect_data(self, **kwargs):
        """"""
        if not kwargs:
            print("""
This command line will help you to create a standard Python package with a
documentation template preconfigured and 'CGPDS' as the namespace.""", end="\n\n")

            print("Documentation: https://gcpds.readthedocs.io/projects/utils/en/latest/_notebooks/05-distutils.html", end="\n\n")

        def read(hint, default=None):
            if default:
                v = input(f"{Fore.MAGENTA}> {hint} [{default}]: {Fore.RESET}")
            else:
                v = input(f"{Fore.MAGENTA}> {hint}: {Fore.RESET}")

            if not v and not default:
                print(f"{Fore.RED}* Please enter some text.{Fore.RESET}")
                return read(hint)
            elif not v and default:
                return default
            else:
                return v

        pkg_name = read('Package name', default=kwargs.get('PKG_NAME', None))
        author = read('Author', default=kwargs.get('AUTHOR', None))
        author_email = read(
            'Author email', default=kwargs.get('AUTHOR_EMAIL', None))

        maintainer = read(
            f'Maintainer', default=kwargs.get('MAINTAINER', author))
        maintainer_email = read(
            f'Maintainer email', default=kwargs.get('MAINTAINER_EMAIL', author_email))

        requieres = read(f'Requieres (separated by comma)',
                         default=kwargs.get('PKG_REQUIERES', None))

        self.data = {
            'PKG_NAME': pkg_name.lower().replace(' ', '_').replace('-', '_'),
            'AUTHOR': author.title(),
            'AUTHOR_EMAIL': author_email.lower(),
            'MAINTAINER': maintainer.title(),
            'MAINTAINER_EMAIL': maintainer_email.lower(),
            'PKG_REQUIERES': ', '.join([p.strip() for p in requieres.split(',')]),
        }

        print('\n')
        for key in self.data:
            print(f"{Fore.GREEN}> {key}: {self.data[key]}{Fore.RESET}")

        ok = None
        while not ok in ['y', 'n']:
            ok = input(
                f'\n{Fore.MAGENTA}> input data is ok? [Y/n]: {Fore.RESET}')
            ok = ok.lower()
            ok = ok.strip()
            if ok == '':
                ok = 'y'

        if ok == 'n':
            return self.collect_data(**self.data)

    # ----------------------------------------------------------------------
    def clone_pkg(self):
        """"""

        self.pkg_user = os.path.join(self.dst, self.data['PKG_NAME'])

        try:
            shutil.copytree(self.src, self.pkg_user)
        except:
            logging.warning(
                f"Impossible to create the package '{os.path.split(self.dst)[1]}' "
                f"in '{os.path.split(self.dst)[0]}', already exists?")
            return

        os.rename(os.path.join(self.pkg_user, 'gcpds', '{{PKG_NAME}}'),
                  os.path.join(self.pkg_user, 'gcpds', self.data['PKG_NAME']))

    # ----------------------------------------------------------------------
    def contextualize(self):
        """"""
        for root, dirs, files in os.walk(self.pkg_user):

            for file in files:

                if not os.path.splitext(file)[-1] == TEMPLATE_EXTENSION:
                    continue

                filepath = os.path.join(root, file)

                with open(filepath, 'rb') as file:
                    content = file.read()

                template = Template(content.decode())
                content = template.render(**self.data)

                with open(filepath, 'wb') as file:
                    file.write(content.encode())

                os.rename(filepath, os.path.join(
                    *os.path.splitext(filepath)[:-1]))



