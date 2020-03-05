#!/bin/bash

sudo mv /tmp/jupyter-notebook.service /etc/systemd/system/
sudo systemctl enable jupyter-notebook.service
sudo systemctl daemon-reload
sudo systemctl restart jupyter-notebook.service

conda create -y -n notebook_env python=3.7 notebook nb_conda_kernels

# HelPedestorML19
passwd_hash="sha1:c7048e5d63f2:ea31f240526f28376bb1d315fb44db8f62c5afe1"
echo "c.NotebookApp.password = u'${passwd_hash}'" >> /home/ubuntu/.jupyter/jupyter_notebook_config.py
