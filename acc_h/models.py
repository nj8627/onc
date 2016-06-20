from django.db import models

class CHNL_ID_M(models.Model):
    CHNL_ID	 = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    def __str__(self):          
        return self.CHNL_ID

class CHNL_NM_M(models.Model):
    CHNL_NM	 = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    def __str__(self):          
        return self.CHNL_NM

class CHNL_ID_NM_M(models.Model):
    CHNL_ID	 = models.ForeignKey(CHNL_ID_M,db_index=True)
    CHNL_NM	 = models.ForeignKey(CHNL_NM_M,db_index=True)
    
		
class CHNL_VAL_M(models.Model):
    CHNL_VAL	 = models.CharField(max_length=250,null=True,blank=True,db_index=True)
    def __str__(self):          
        return self.CHNL_VAL

		
class PFZ_MKT_M(models.Model):
    PFZ_MKT_NM = models.CharField(max_length=250,null=True,blank=True,db_index=True)
    def __str__(self):          
        return self.PFZ_MKT_NM

class TIME_BCKT_M(models.Model):
    TIME_BCKT = models.CharField(max_length=250,null=True,blank=True,db_index=True)
    def __str__(self):          
        return self.TIME_BCKT

class BRAND_NM_M(models.Model):
    PFZ_MKT	 = models.ForeignKey(PFZ_MKT_M,db_index=True)
    BRAND_NM = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    def __str__(self):          
        return self.BRAND_NM

class PARENT_M(models.Model):
    PARENT_ID	 = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    PARENT_NM	 = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    PARENT_FULL_ADDR	 = models.CharField(max_length=250,null=True,blank=True)
    def __str__(self):          
        return self.PARENT_ID

class CHILD_M(models.Model):
    CHILD_ID	 = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    CHILD_NM	 = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    CHILD_FULL_ADDR	 = models.CharField(max_length=250,null=True,blank=True)
    def __str__(self):          
        return self.CHILD_ID

class ACCOUNT_INFO(models.Model):
    CHNL_ID	 = models.ForeignKey(CHNL_ID_M,db_index=True)
    CHNL_NM	 = models.ForeignKey(CHNL_NM_M,db_index=True)
    CHNL_VAL	 = models.ForeignKey(CHNL_VAL_M,db_index=True)
    CHILD	 = models.ForeignKey(CHILD_M,null=True,blank=True,db_index=True)
    PARENT	 = models.ForeignKey(PARENT_M,null=True,blank=True,db_index=True)
    PFZ_MKT	 = models.ForeignKey(PFZ_MKT_M,db_index=True)
    BRAND_NM	 = models.ForeignKey(BRAND_NM_M,db_index=True)
    TIME_BCKT = models.ForeignKey(TIME_BCKT_M,db_index=True)
    CURR_TRX_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_DOL_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_UNIT_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_NEW_PTNT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_TOTAL_PTNT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_TRX_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_DOL_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_UNIT_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_TRX_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_DOL_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_UNIT_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_NEW_PTNT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_TOTAL_PTNT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_TRX_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_DOL_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_UNIT_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_DTL = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_DTL_TCL = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP_TCL = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP_WITH_DTL = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP_TCL_WITH_DTL = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP_WITH_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP_TCL_WITH_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)

class BIG_TABLE(models.Model):
    CHNL_ID = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    CHNL_NM = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    CHNL_VAL = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    CHILD_ID = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    CHILD_NM = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    CHILD_FULL_ADDR = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    PARENT_ID = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    PARENT_NM = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    PARENT_FULL_ADDR = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    PFZ_MKT_NM = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    BRAND_NM = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    TIME_BCKT = models.CharField(db_index=True,max_length=250,null=True,blank=True)
    CURR_TRX_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_DOL_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_UNIT_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_NEW_PTNT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_TOTAL_PTNT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_TRX_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_DOL_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    CURR_UNIT_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_TRX_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_DOL_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_UNIT_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_NEW_PTNT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_TOTAL_PTNT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_TRX_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_DOL_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    PREV_UNIT_SLS_MKT = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_DTL = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_DTL_TCL = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP_TCL = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP_WITH_DTL = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP_TCL_WITH_DTL = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP_WITH_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)
    NUM_HCP_TCL_WITH_SLS = models.DecimalField(max_digits=19, decimal_places=0,null=True,blank=True)


    

	
	
# Create your models here.
