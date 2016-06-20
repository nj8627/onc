from django.contrib import admin
from acc_h.models import *
from django.db.models import get_models, get_app
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

class CHNL_ID_M_Resource(resources.ModelResource):
	class Meta:
		model = CHNL_ID_M
class CHNL_ID_M_IE (ImportExportModelAdmin):
    resource_class = CHNL_ID_M_Resource
    pass
admin.site.register(CHNL_ID_M,CHNL_ID_M_IE)

class CHNL_NM_M_Resource(resources.ModelResource):
	class Meta:
		model = CHNL_NM_M
class CHNL_NM_M_IE (ImportExportModelAdmin):
    resource_class = CHNL_NM_M_Resource
    pass
admin.site.register(CHNL_NM_M,CHNL_NM_M_IE)

class CHNL_ID_NM_M_Resource(resources.ModelResource):
	class Meta:
		model = CHNL_ID_NM_M
class CHNL_ID_NM_M_IE (ImportExportModelAdmin):
    resource_class = CHNL_ID_NM_M_Resource
    pass
admin.site.register(CHNL_ID_NM_M,CHNL_ID_NM_M_IE)



class CHNL_VAL_M_Resource(resources.ModelResource):
	class Meta:
		model = CHNL_VAL_M
class CHNL_VAL_M_IE (ImportExportModelAdmin):
    resource_class = CHNL_VAL_M_Resource
    pass
admin.site.register(CHNL_VAL_M,CHNL_VAL_M_IE)



class PFZ_MKT_M_Resource(resources.ModelResource):
	class Meta:
		model = PFZ_MKT_M
class PFZ_MKT_M_IE (ImportExportModelAdmin):
    resource_class = PFZ_MKT_M_Resource
    pass
admin.site.register(PFZ_MKT_M,PFZ_MKT_M_IE )

class TIME_BCKT_M_Resource(resources.ModelResource):
	class Meta:
		model = TIME_BCKT_M
class TIME_BCKT_M_IE (ImportExportModelAdmin):
    resource_class = TIME_BCKT_M_Resource
    pass
admin.site.register(TIME_BCKT_M,TIME_BCKT_M_IE )

class BRAND_NM_M_Resource(resources.ModelResource):
	class Meta:
		model = BRAND_NM_M
class BRAND_NM_M_IE (ImportExportModelAdmin):
    resource_class = BRAND_NM_M_Resource
    pass
admin.site.register(BRAND_NM_M,BRAND_NM_M_IE)

class PARENT_M_Resource(resources.ModelResource):
	class Meta:
		model = PARENT_M
class PARENT_M_IE (ImportExportModelAdmin):
    resource_class = PARENT_M_Resource
    pass
admin.site.register(PARENT_M,PARENT_M_IE)

class CHILD_M_Resource(resources.ModelResource):
	class Meta:
		model = CHILD_M
class CHILD_M_IE (ImportExportModelAdmin):
    resource_class = CHILD_M_Resource
    pass
admin.site.register(CHILD_M,CHILD_M_IE)

class ACCOUNT_INFO_Resource(resources.ModelResource):
	class Meta:
		model = ACCOUNT_INFO
class ACCOUNT_INFO_IE (ImportExportModelAdmin):
    resource_class = ACCOUNT_INFO_Resource
    pass
admin.site.register(ACCOUNT_INFO,ACCOUNT_INFO_IE)

class BIG_TABLE_Resource(resources.ModelResource):
	class Meta:
		model = BIG_TABLE
class BIG_TABLE_IE (ImportExportModelAdmin):
    resource_class = BIG_TABLE_Resource
    pass
admin.site.register(BIG_TABLE,BIG_TABLE_IE)



# Register your models here.
