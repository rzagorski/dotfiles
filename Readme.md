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
    git clone git@github.com:afterdesign/dotfiles.git ~/.dotfiles
    cd ~/.dotfiles
    $(python -m site --user-base)/bin/ansible-playbook --ask-become-pass -i local.hosts playbook.yml
    ```

# License

Licensed under the [MIT license](http://opensource.org/licenses/MIT).
