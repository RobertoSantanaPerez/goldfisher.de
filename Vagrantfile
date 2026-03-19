Vagrant.configure("2") do |config|

  config.vm.define "goldfisher" do |goldfisher|
    goldfisher.vm.box = "generic/debian11"
    goldfisher.vm.network "private_network", ip: "192.168.56.111"
    goldfisher.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/provision.yml"
      ansible.verbose =  true
    end
  end

end
