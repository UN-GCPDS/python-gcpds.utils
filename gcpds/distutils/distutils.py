import os
import shutil
from jinja2 import Template
import logging
from colorama import Fore
from pathlib import Path
import configparser

TEMPLATE_EXTENSION = '.j2'


########################################################################
class Distutils:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, dst: str) -> None:
        """Constructor"""
        self.src = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'project_template'
        )
        self.src_sphinx = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'sphinx_template'
        )
        self.src_notebooks = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'notebooks_template'
        )
        self.dst = dst

        self.collect_data()
        self.docs = os.path.join(
            dst, f"python-gcpds.{self.data['PKG_NAME']}", 'docs'
        )
        self.notebooks_dir = os.path.join(self.docs, 'source', 'notebooks')

        self.clone_pkg()
        self.contextualize(self.pkg_user)
        self.build_documentation()
        self.contextualize(self.notebooks_dir, extension=False)

    # ----------------------------------------------------------------------
    def collect_data(self, **kwargs):
        """"""
        if not kwargs:
            print(
                """
This command line will help you to create a standard Python package with a
documentation template preconfigured and 'CGPDS' as the namespace.""",
                end="\n\n",
            )

            print(
                "Documentation: https://gcpds.readthedocs.io/projects/utils/en/latest/_notebooks/05-distutils.html",
                end="\n\n",
            )

        def read(hint, default=None, empty=False):
            if default:
                v = input(
                    f"{Fore.MAGENTA}> {hint} [{default}]: {Fore.RESET}"
                )
            else:
                v = input(f"{Fore.MAGENTA}> {hint}: {Fore.RESET}")

            if not v and not default and not empty:
                print(f"{Fore.RED}* Please enter some text.{Fore.RESET}")
                return read(hint)
            elif not v and default:
                return default
            elif not v and empty:
                return ''
            else:
                return v

        pkg_name = read('Package name', default=kwargs.get('PKG_NAME', None))
        author = read('Author', default=kwargs.get('AUTHOR', None))
        author_email = read(
            'Author email', default=kwargs.get('AUTHOR_EMAIL', None)
        )

        maintainer = read(
            f'Maintainer', default=kwargs.get('MAINTAINER', author)
        )
        maintainer_email = read(
            f'Maintainer email',
            default=kwargs.get('MAINTAINER_EMAIL', author_email),
        )

        requieres = read(
            f'Requirements (separated by comma)',
            default=kwargs.get('PKG_REQUIERES', None),
            empty=True,
        )

        if requieres.strip():
            pkg_requieres = [p.strip() for p in requieres.strip().split(',')]
        else:
            pkg_requieres = ''

        self.data = {
            'PKG_NAME': pkg_name.lower().replace(' ', '_').replace('-', '_'),
            'AUTHOR': author.title(),
            'AUTHOR_EMAIL': author_email.lower(),
            'MAINTAINER': maintainer.title(),
            'MAINTAINER_EMAIL': maintainer_email.lower(),
            'PKG_REQUIERES': pkg_requieres,
        }

        print('\n')
        for key in self.data:
            print(f"{Fore.GREEN}> {key}: {self.data[key]}{Fore.RESET}")

        ok = None
        while not ok in ['y', 'n']:
            ok = input(
                f'\n{Fore.MAGENTA}> input data is ok? [Y/n]: {Fore.RESET}'
            )
            ok = ok.lower()
            ok = ok.strip()
            if ok == '':
                ok = 'y'

        if ok == 'n':
            return self.collect_data(**self.data)

    # ----------------------------------------------------------------------
    def clone_pkg(self):
        """"""

        self.pkg_user = os.path.join(
            self.dst, f"python-gcpds.{self.data['PKG_NAME']}"
        )

        try:
            shutil.copytree(self.src, self.pkg_user)
        except:
            logging.warning(
                f"Impossible to create the package '{os.path.split(self.dst)[1]}' "
                f"in '{os.path.split(self.dst)[0]}', already exists?"
            )
            return

        os.rename(
            os.path.join(self.pkg_user, 'gcpds', '{{PKG_NAME}}'),
            os.path.join(self.pkg_user, 'gcpds', self.data['PKG_NAME']),
        )

        os.rename(
            os.path.join(self.pkg_user, 'dot.gitignore'),
            os.path.join(self.pkg_user, '.gitignore'),
        )

        os.rename(
            os.path.join(self.pkg_user, 'dot.readthedocs.yml'),
            os.path.join(self.pkg_user, '.readthedocs.yml'),
        )

    # ----------------------------------------------------------------------
    def contextualize(self, target, extension=True):
        """"""
        for root, dirs, files in os.walk(target):

            for file in files:

                if extension:
                    if not os.path.splitext(file)[-1] == TEMPLATE_EXTENSION:
                        continue

                filepath = os.path.join(root, file)

                with open(filepath, 'rb') as file:
                    content = file.read()

                template = Template(content.decode())
                content = template.render(**self.data)

                with open(filepath, 'wb') as file:
                    file.write(content.encode())

                os.rename(
                    filepath, os.path.join(*os.path.splitext(filepath)[:-1])
                )

    # ----------------------------------------------------------------------
    def build_documentation(self):
        """"""
        os.mkdir(self.docs)
        os.chdir(self.docs)

        project_dir = f"../gcpds/{self.data['PKG_NAME']}"

        command = f"""sphinx-quickstart

        --author={self.data['AUTHOR']}
        --project={self.data['PKG_NAME']}
        --templatedir={self.src_sphinx}
        -d project_dir={project_dir}

        --no-use-make-mode
        --makefile
        --quiet
        --sep

        --ext-autodoc
        --ext-coverage
        --ext-viewcode
        --ext-todo
        --ext-mathjax
        --extensions='sphinx.ext.napoleon,sphinx.ext.autosectionlabel,nbsphinx,sphinxcontrib.bibtex'
        """
        os.system(command.replace('\n', ''))

        try:
            shutil.copytree(
                self.src_notebooks,
                self.notebooks_dir,
            )
        except:
            logging.warning(
                f"Impossible to create the package '{self.notebooks_dir}' "
                f"in '{os.path.split(self.notebooks_dir)[0]}', already exists?"
            )
            return


if __name__ == '__main__':
    Distutils(os.path.expanduser('~/'))
