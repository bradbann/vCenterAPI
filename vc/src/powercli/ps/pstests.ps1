#组织json形式的数据
$json = @"
{
    "vmname": "test_vm01",
    "ostype": "Linux",
    "disk": [
        {"diskname":"vdisk01", "size":100},
        {"diskname":"vdisk02", "size":200}
    ],
    "ip":"192.168.1.100"
 }
"@
 
#转换成json格式
$info = ConvertFrom-Json -InputObject $json
 
#访问json数据
$info.vmname
$info.disk
$info.ip