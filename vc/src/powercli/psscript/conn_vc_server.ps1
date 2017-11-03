
$server = "192.168.1.182"
$user = "administrator"
$password = "1qaz@WSX"

Add-PSSnapin VMware.VimAutomation.Core
$moduleName = Get-PSSnapin "VMware.VimAutomation.Core"

if ( $moduleName.Name -ne "VMware.VimAutomation.Core" ){
    Write-Warning "VMware.VimAutomation.Core 模块正在导入"
    Add-PSSnapin VMware.VimAutomation.Core
}
Write-Host "VMware.VimAutomation.Core 模块状态可用"

Write-Host "连接vCenter Server..."
Connect-VIServer -Server $server -User $user -Password $password

