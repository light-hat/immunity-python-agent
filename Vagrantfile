# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "agent_test_vm" do |agent|
    agent.vm.box = "ubuntu/focal64"
    agent.vm.hostname = "agent"
    config.vm.network "private_network", ip: "192.168.33.10"
    agent.vm.network "forwarded_port", guest: 8000, host: 8000
    agent.vm.network "forwarded_port", guest: 5000, host: 5000

    config.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.cpus = "2"
    end

    config.vm.provision "shell", inline: <<-SHELL
        apt-get update
        apt-get install -y python3-pip
        pip install Django Flask
    SHELL

  end

end