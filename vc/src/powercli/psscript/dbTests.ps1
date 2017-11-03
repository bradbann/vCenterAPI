
#新建数据库
#new-psdrive -name db -psp SQLite -root "Data Source=C:\VMware\data.sqlite"

#创建表，表名字：vc_ps_netlabel，字段：netlabel
#new-item db:/vc_ps_netlabel -netlabel text

#插入数据到表
#new-item db:/vc_ps_netlabel -netlabel '4562'