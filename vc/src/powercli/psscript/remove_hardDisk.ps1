<#
#仅从虚拟机移除硬盘，并未从存储彻底移除
$vm = Get-VM "aaa"
$disk = Get-HardDisk $vm
Remove-HardDisk -HardDisk $disk -Confirm:$false


#添加现有的硬盘
$vm = Get-VM "aaa"
New-HardDisk -vm $vm -DiskPath "[189] aaa/aaa_2.vmdk"
New-HardDisk -vm $vm -DiskPath "[189] aaa/aaa_1.vmdk"
#>
