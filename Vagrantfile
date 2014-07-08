Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise32"
  config.vm.provision "shell", :path => "./scripts/vagrant_up.sh"
  config.vm.network :forwarded_port, host: 9160, guest: 9160
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
  end
end
