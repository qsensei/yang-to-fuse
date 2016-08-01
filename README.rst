yang-to-fuse
############

.. image:: https://travis-ci.org/qsensei/yang-to-fuse.svg?branch=master
  :target: https://travis-ci.org/qsensei/yang-to-fuse

pyang_ plugin to generate Q-Sensei Fuse indexschema.

Installation
============

It is recommended to use virutalenv when using this python library. For
ubuntu:

.. code-block:: bash

  sudo apt-get update
  sudo apt-get install python-pip python-virtualenv

Create the virtual python environment. This allows for creation of quick python
environments without installing directly to system paths.

.. code-block:: bash

  virtualenv env
  source env/bin/activate
  which pip
  # /home/ubuntu/env/bin/pip
  which python
  # /home/ubuntu/env/bin/python

*Note: When you're done with your virtualenv, run deactivate to deactivate
the virtual python environment from your shell session.*

First, install source code. For the editable development version, run the
following. This will also install the pyang_ script as well.

.. code-block::

  git clone git@github.com:qsensei/yang-to-fuse.git
  cd yang-to-fuse
  pip install -r requirements.txt

Usage
=====

By using the ``qsensei-fuse`` output format, we can automatically create an
indexschema using this pyang_ plugin.

.. code-block:: bash

  pyang --plugindir ./plugins/ -f qsensei-fuse mymodel.yang > indexschema.json
  mv indexschema.json /path/to/my/pkg/indexschema.json

See pyang_ for additional usage.

.. _pyang: https://github.com/mbj4668/pyang
