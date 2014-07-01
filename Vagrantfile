Vagrant.configure("2") do |config|
  config.vm.provision "shell", :path => "./vagrant_up.sh"
  config.vm.box = "hashicorp/precise32"

  config.vm.define "cass1" do |cass1|
    cass1.vm.box = "hashicorp/precise32"
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
