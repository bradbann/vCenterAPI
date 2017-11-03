C:\VMware\vc\src\powercli\psscript\conn_vc_server.ps1

Import-Module SQLite
new-psdrive -name db -psp SQLite -root "Data Source=C:\VMware\data.sqlite"


# 获取网络标签数据
$label = Get-VirtualPortGroup

#数据去重
$dt = $label.Name | Sort-Object -Unique

#写入数据库
foreach ($n in $dt)
{
    Write-Host "数据 网络标签：$n 入库"
    new-item db:/vc_ps_netlabel -netlabel $n
}
