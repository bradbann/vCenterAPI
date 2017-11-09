
#新建数据库
#new-psdrive -name db -psp SQLite -root "Data Source=C:\VMware\data.sqlite"

#创建表，表名字：vc_ps_netlabel，字段：netlabel
#new-item db:/vc_ps_netlabel -netlabel text
#new-item db:/vc_ps_datastore_host_relation -datastore text -esxi text


#插入数据到表
#new-item db:/vc_ps_netlabel -netlabel '4562'
#new-item db:/vc_ps_datastore_host_relation -datastore "189" -esxi "192.168.1.189"

# 获取所有数据
#get-childitem db:/vc_ps_netlabel

# 获取表字段
#get-childitem db:/vc_ps_netlabel | select netlabel, id

# 通过网络标签过滤
#get-childitem db:/vc_ps_netlabel -filter "netlabel='br-vlan'" | select netlabel, id 

# 通过ID过滤
#get-childitem db:/vc_ps_netlabel -filter "id=187" | select netlabel, id

# 更新数据（将br-int更新为jimbo）
#set-item db:/vc_ps_netlabel -filter "netlabel='br-int'" -value @{ netlabel='jimbo' }

# 通过id更新数据
#set-item db:/vc_ps_netlabel -filter "id=186" -value @{ netlabel='vlan1900' }

# 通过id 删除数据
#remove-item db:/vc_ps_netlabel -filter "id=186"

# 通过网络标签删除
#remove-item db:/vc_ps_netlabel -filter "netlabel='test'"