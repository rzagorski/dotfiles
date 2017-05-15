## Dotfiles

My dotfiles for quick macOS/OS X.

## Run configuration

1. Install xcode and CLI tools:

    ```
    xcode-select --install
    ```

1. Install ansible:

    ```
    sudo easy_install pip
    pip install --user ansible
    ```

1. Run ansible:

    ```
    git clone git@github.com:rzagorski/dotfiles.git ~/.dotfiles
    cd ~/.dotfiles
    $(python -m site --user-base)/bin/ansible-playbook --ask-become-pass -i local.hosts playbook.yml
    ```

1. Cleanup:

    ```
    /usr/local/bin/pip list --user --format=freeze | xargs pip uninstall -y $1
    sudo /usr/local/bin/pip uninstall -y pip
    ```

# License

Licensed under the [MIT license](http://opensource.org/licenses/MIT).
