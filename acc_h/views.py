from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse
from acc_h.models import *
from django.db.models import Sum
import time
from django.db.models import Q
from django.core.urlresolvers import reverse
import json
from django.core.serializers.json import DjangoJSONEncoder
import operator
from collections import OrderedDict
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect


def child_ajax(request,mkt_id,chnl_id,brand_id,metric,time_period,chnl_nm,acc_id,blnk):
    if brand_id == '0':
        sel_brand = BRAND_NM_M.objects.filter()
    else:
        sel_brand = BRAND_NM_M.objects.filter(id=brand_id)
    sel_chnl_id = CHNL_ID_M.objects.get(id=chnl_id)
    sel_chnl_nm = CHNL_NM_M.objects.get(id=chnl_nm)
    parent = PARENT_M.objects.get(id=acc_id)
    time_period = TIME_BCKT_M.objects.get(id=time_period)
    if blnk == '1':
        if metric == '1':
            child_accs = ACCOUNT_INFO.objects.filter(BRAND_NM__in=sel_brand,CHNL_ID=sel_chnl_id,CHNL_NM=sel_chnl_nm,PARENT = parent,TIME_BCKT = time_period).values('CHILD__CHILD_ID','CHILD__CHILD_NM','CHILD__CHILD_FULL_ADDR','CURR_TRX_SLS','PREV_TRX_SLS','CURR_TRX_SLS_MKT','CURR_DOL_SLS','PREV_DOL_SLS','CURR_DOL_SLS_MKT','CURR_UNIT_SLS','PREV_UNIT_SLS','CURR_UNIT_SLS_MKT','CURR_NEW_PTNT','CURR_TOTAL_PTNT','NUM_HCP_TCL', 'NUM_HCP_TCL_WITH_DTL', 'NUM_DTL_TCL', 'NUM_HCP_TCL_WITH_SLS',).order_by('CURR_TRX_SLS')
        elif metric == '2':
            child_accs = ACCOUNT_INFO.objects.filter(BRAND_NM__in=sel_brand,CHNL_ID=sel_chnl_id,CHNL_NM=sel_chnl_nm,PARENT = parent,TIME_BCKT = time_period).values('CHILD__CHILD_ID','CHILD__CHILD_NM','CHILD__CHILD_FULL_ADDR','CURR_TRX_SLS','PREV_TRX_SLS','CURR_TRX_SLS_MKT','CURR_DOL_SLS','PREV_DOL_SLS','CURR_DOL_SLS_MKT','CURR_UNIT_SLS','PREV_UNIT_SLS','CURR_UNIT_SLS_MKT','CURR_NEW_PTNT','CURR_TOTAL_PTNT','NUM_HCP_TCL', 'NUM_HCP_TCL_WITH_DTL', 'NUM_DTL_TCL', 'NUM_HCP_TCL_WITH_SLS',).order_by('CURR_DOL_SLS')
        elif mertic == '3':
            child_accs = ACCOUNT_INFO.objects.filter(BRAND_NM__in=sel_brand,CHNL_ID=sel_chnl_id,CHNL_NM=sel_chnl_nm,PARENT = parent,TIME_BCKT = time_period).values('CHILD__CHILD_ID','CHILD__CHILD_NM','CHILD__CHILD_FULL_ADDR','CURR_TRX_SLS','PREV_TRX_SLS','CURR_TRX_SLS_MKT','CURR_DOL_SLS','PREV_DOL_SLS','CURR_DOL_SLS_MKT','CURR_UNIT_SLS','PREV_UNIT_SLS','CURR_UNIT_SLS_MKT','CURR_NEW_PTNT','CURR_TOTAL_PTNT','NUM_HCP_TCL', 'NUM_HCP_TCL_WITH_DTL', 'NUM_DTL_TCL', 'NUM_HCP_TCL_WITH_SLS',).order_by('CURR_UNIT_SLS')
    else:
        if metric == '1':
	        child_accs = ACCOUNT_INFO.objects.filter(BRAND_NM__in=sel_brand,CHNL_ID=sel_chnl_id,CHNL_NM=sel_chnl_nm,PARENT = parent,TIME_BCKT = time_period).exclude(PARENT=1,CHILD=1).values('CHILD__CHILD_ID','CHILD__CHILD_NM','CHILD__CHILD_FULL_ADDR','CURR_TRX_SLS','PREV_TRX_SLS','CURR_TRX_SLS_MKT','CURR_DOL_SLS','PREV_DOL_SLS','CURR_DOL_SLS_MKT','CURR_UNIT_SLS','PREV_UNIT_SLS','CURR_UNIT_SLS_MKT','CURR_NEW_PTNT','CURR_TOTAL_PTNT','NUM_HCP_TCL', 'NUM_HCP_TCL_WITH_DTL', 'NUM_DTL_TCL', 'NUM_HCP_TCL_WITH_SLS',).order_by('CURR_TRX_SLS')
        if metric == '2':
            child_accs = ACCOUNT_INFO.objects.filter(BRAND_NM__in=sel_brand,CHNL_ID=sel_chnl_id,CHNL_NM=sel_chnl_nm,PARENT = parent,TIME_BCKT = time_period).exclude(PARENT=1,CHILD=1).values('CHILD__CHILD_ID','CHILD__CHILD_NM','CHILD__CHILD_FULL_ADDR','CURR_TRX_SLS','PREV_TRX_SLS','CURR_TRX_SLS_MKT','CURR_DOL_SLS','PREV_DOL_SLS','CURR_DOL_SLS_MKT','CURR_UNIT_SLS','PREV_UNIT_SLS','CURR_UNIT_SLS_MKT','CURR_NEW_PTNT','CURR_TOTAL_PTNT','NUM_HCP_TCL', 'NUM_HCP_TCL_WITH_DTL', 'NUM_DTL_TCL', 'NUM_HCP_TCL_WITH_SLS',).order_by('CURR_DOL_SLS')
        if metric == '3':
            child_accs = ACCOUNT_INFO.objects.filter(BRAND_NM__in=sel_brand,CHNL_ID=sel_chnl_id,CHNL_NM=sel_chnl_nm,PARENT = parent,TIME_BCKT = time_period).exclude(PARENT=1,CHILD=1).values('CHILD__CHILD_ID','CHILD__CHILD_NM','CHILD__CHILD_FULL_ADDR','CURR_TRX_SLS','PREV_TRX_SLS','CURR_TRX_SLS_MKT','CURR_DOL_SLS','PREV_DOL_SLS','CURR_DOL_SLS_MKT','CURR_UNIT_SLS','PREV_UNIT_SLS','CURR_UNIT_SLS_MKT','CURR_NEW_PTNT','CURR_TOTAL_PTNT','NUM_HCP_TCL', 'NUM_HCP_TCL_WITH_DTL', 'NUM_DTL_TCL', 'NUM_HCP_TCL_WITH_SLS',).order_by('CURR_UNIT_SLS')
    data = json.dumps(list(child_accs), cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type='application/json')

def brand_ajax(request,mkt_id):
    if mkt_id == '0':
        sel_brand_lis = BRAND_NM_M.objects.filter().values('BRAND_NM','id')
    else:
        sel_brand_lis = BRAND_NM_M.objects.filter(PFZ_MKT=PFZ_MKT_M.objects.get(id=mkt_id)).values('BRAND_NM','id')
    data = json.dumps(list(sel_brand_lis), cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type='application/json')

	
	
def part_2(request):
    return HttpResponseRedirect('/acc_h/new/0/')
	
def ifnull(var, val):
  if var is None:
    return val
  return var
 
  
def part_1(request,mkt_id=None,chnl_id=None,brand_id=None,metric=None,time_period=None,blnk=0):
    if mkt_id == '0':
        brand_lis = BRAND_NM_M.objects.filter()
    else:
        brand_lis = BRAND_NM_M.objects.filter(PFZ_MKT=PFZ_MKT_M.objects.get(id=mkt_id))
    mkt_lis = PFZ_MKT_M.objects.all()
    chnl_id_lis = CHNL_ID_M.objects.all()
    tim_bkt_lis = []
    for x in [1, 3, 4, 2, 5]:
        tim_bkt_lis.append(TIME_BCKT_M.objects.get(id=x))
    st = time.time()
    lis = {'brand_lis':brand_lis,'chnl_id_lis':chnl_id_lis,'mkt_id':mkt_id,'tim_bkt_lis':tim_bkt_lis,'blnk':blnk,'mkt_lis':mkt_lis}
    metric_sel = ''
    if chnl_id != None and brand_id != None and metric != None and time_period != None:
        chnl_nm_lis = {}
        if brand_id == '0' and mkt_id == '0':
            sel_brand = BRAND_NM_M.objects.filter()
        elif brand_id == '0':
            sel_brand = BRAND_NM_M.objects.filter(PFZ_MKT=PFZ_MKT_M.objects.get(id=mkt_id))
        else:
            sel_brand = BRAND_NM_M.objects.filter(id=brand_id)
        sel_chnl_id = CHNL_ID_M.objects.get(id=chnl_id)
        sel_time_prd = TIME_BCKT_M.objects.get(id=time_period)
        if metric == '1' :
            metric_sel = 'TRx'
        if metric == '2' :
            metric_sel = 'Dollar'
        if metric == '3' :
            metric_sel = 'Unit'
        for CHNL in CHNL_ID_NM_M.objects.filter(CHNL_ID=sel_chnl_id):
            if blnk == '1':
                parent_acc = PARENT_M.objects.filter(PARENT_ID__in=ACCOUNT_INFO.objects.filter(BRAND_NM=sel_brand,CHNL_NM=CHNL.CHNL_NM,CHNL_ID=sel_chnl_id,TIME_BCKT=sel_time_prd).values('PARENT__PARENT_ID').distinct())
                accs = ACCOUNT_INFO.objects.filter(BRAND_NM=sel_brand,CHNL_NM=CHNL.CHNL_NM,CHNL_ID=sel_chnl_id,TIME_BCKT=sel_time_prd)
            elif CHNL.CHNL_NM.id ==1:
                continue
            else:
                parent_acc = PARENT_M.objects.filter(PARENT_ID__in=ACCOUNT_INFO.objects.filter(BRAND_NM__in=sel_brand,CHNL_NM=CHNL.CHNL_NM,CHNL_ID=sel_chnl_id,TIME_BCKT=sel_time_prd).values('PARENT__PARENT_ID').exclude(PARENT=1,CHILD=1).distinct())
                accs = ACCOUNT_INFO.objects.filter(BRAND_NM__in=sel_brand,CHNL_NM=CHNL.CHNL_NM,CHNL_ID=sel_chnl_id,TIME_BCKT=sel_time_prd).exclude(PARENT=1,CHILD=1)
            parent_m_lis = {}
            chnl_new_ptnt = 0
            chnl_t_ptnt = 0
            chnl_metric = 0
            chnl_grwth = 0
            chnl_mkt = 0
            NUM_HCP_TCL = 0
            NUM_HCP_TCL_WITH_DTL = 0
            NUM_DTL_TCL = 0
            NUM_HCP_TCL_WITH_SLS  = 0
            for parent in parent_acc:
                parent_m_lis[parent] = [0,0,0,0,0,0,0,0,0] # Metric, Growth, Share, New Ptnt, Total Ptnt, NUM_HCP_TCL, NUM_HCP_TCL_WITH_DTL, NUM_DTL_TCL, NUM_HCP_TCL_WITH_SLS 
            for acc in accs:
                parent_m_lis[acc.PARENT][3] = parent_m_lis[acc.PARENT][3]+ acc.CURR_NEW_PTNT
                parent_m_lis[acc.PARENT][4] = parent_m_lis[acc.PARENT][4]+ acc.CURR_TOTAL_PTNT
                chnl_new_ptnt = chnl_new_ptnt + acc.CURR_NEW_PTNT
                chnl_t_ptnt = chnl_t_ptnt + acc.CURR_TOTAL_PTNT
                NUM_HCP_TCL = NUM_HCP_TCL + acc.NUM_HCP_TCL
                NUM_HCP_TCL_WITH_DTL = NUM_HCP_TCL_WITH_DTL + acc.NUM_HCP_TCL_WITH_DTL
                NUM_DTL_TCL = NUM_DTL_TCL + acc.NUM_DTL_TCL
                NUM_HCP_TCL_WITH_SLS  = NUM_HCP_TCL_WITH_SLS + acc.NUM_HCP_TCL_WITH_SLS
                parent_m_lis[acc.PARENT][5] = parent_m_lis[acc.PARENT][5]+ acc.NUM_HCP_TCL
                parent_m_lis[acc.PARENT][6] = parent_m_lis[acc.PARENT][6]+ acc.NUM_HCP_TCL_WITH_DTL
                parent_m_lis[acc.PARENT][7] = parent_m_lis[acc.PARENT][7]+ acc.NUM_DTL_TCL
                parent_m_lis[acc.PARENT][8] = parent_m_lis[acc.PARENT][8]+ acc.NUM_HCP_TCL_WITH_SLS
                if metric == '1' :
                    parent_m_lis[acc.PARENT][0] = parent_m_lis[acc.PARENT][0]+ acc.CURR_TRX_SLS
                    chnl_metric = chnl_metric + acc.CURR_TRX_SLS
                    parent_m_lis[acc.PARENT][1] = parent_m_lis[acc.PARENT][1]+ ifnull(acc.PREV_TRX_SLS,0)
                    chnl_grwth = chnl_grwth + ifnull(acc.PREV_TRX_SLS,0)
                    parent_m_lis[acc.PARENT][2] = parent_m_lis[acc.PARENT][2]+ acc.CURR_TRX_SLS_MKT
                    chnl_mkt = chnl_mkt + acc.CURR_TRX_SLS_MKT
                if metric == '2' :
                    parent_m_lis[acc.PARENT][0] = parent_m_lis[acc.PARENT][0]+ acc.CURR_DOL_SLS
                    chnl_metric = chnl_metric + acc.CURR_DOL_SLS
                    parent_m_lis[acc.PARENT][1] = parent_m_lis[acc.PARENT][1]+ ifnull(acc.PREV_DOL_SLS,0)
                    chnl_grwth = chnl_grwth + ifnull(acc.PREV_DOL_SLS,0)
                    parent_m_lis[acc.PARENT][2] = parent_m_lis[acc.PARENT][2]+ acc.CURR_DOL_SLS_MKT
                    chnl_mkt = chnl_mkt + acc.CURR_DOL_SLS_MKT
                if metric == '3' :
                    parent_m_lis[acc.PARENT][0] = parent_m_lis[acc.PARENT][0]+ acc.CURR_UNIT_SLS
                    chnl_metric = chnl_metric + acc.CURR_UNIT_SLS
                    parent_m_lis[acc.PARENT][1] = parent_m_lis[acc.PARENT][1]+ ifnull(acc.PREV_UNIT_SLS,0)
                    chnl_grwth = chnl_grwth + ifnull(acc.PREV_UNIT_SLS,0)
                    parent_m_lis[acc.PARENT][2] = parent_m_lis[acc.PARENT][2]+ acc.CURR_UNIT_SLS_MKT
                    chnl_mkt = chnl_mkt + acc.CURR_UNIT_SLS_MKT
                # code for sorting parent Account
            parent_m_lis_sort = OrderedDict()
            temp_lis = {}
            for key, value in parent_m_lis.items():
                temp_lis[key] = value[0]
            for a,b in sorted(temp_lis.items(), key=operator.itemgetter(1),reverse=True):
                parent_m_lis_sort[a] = parent_m_lis[a]
            chnl_nm_lis[CHNL] = [parent_m_lis_sort,chnl_metric,chnl_grwth,chnl_mkt,chnl_new_ptnt,chnl_t_ptnt,NUM_HCP_TCL, NUM_HCP_TCL_WITH_DTL, NUM_DTL_TCL, NUM_HCP_TCL_WITH_SLS ]
        chnl_nm_lis_sort = OrderedDict()
        temp_lis = {}
        for key, value in chnl_nm_lis.items():
            if blnk == '1':
                temp_lis[key] = value[1]
            elif value[1] > 0:
                temp_lis[key] = value[1]
        for a,b in sorted(temp_lis.items(), key=operator.itemgetter(1),reverse=True):
            chnl_nm_lis_sort[a] = chnl_nm_lis[a]
        lis['chnl_lis'] = chnl_nm_lis_sort
    et = time.time()
    lis['st'] = et - st
    #lis['temp_lis'] = temp
    lis['chnl_id'] = chnl_id
    lis['brand_id'] = brand_id
    lis['metric'] = metric
    lis['metric_sel'] = metric_sel
    lis['time_period'] = time_period
    return render_to_response('page_1.html',lis,context_instance = RequestContext(request))

