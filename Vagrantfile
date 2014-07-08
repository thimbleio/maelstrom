Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise32"
  config.vm.provision "shell", :path => "./scripts/vagrant_up.sh"
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
  end
  config.vm.define "cass1" do |cass1|
    cass1.vm.box = "hashicorp/precise32"
    config.vm.network "forwarded_port", guest: 9160, host: 9160
  end

=begin
  config.vm.define "cass2" do |cass2|
    cass2.vm.box = "hashicorp/precise32"
  end
  
  config.vm.define "cass3" do |cass3|
    cass3.vm.box = "hashicorp/precise32"
  end
=end
end
