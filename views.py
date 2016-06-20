from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib import messages
from GMT.models import *
from GMT.form import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User, Group
from decimal import *
from datetime import date
import csv
from django.db.models import Q
# Create your views here.

def check_user_active(request):
    if request.user.is_active==True:
        group = Group.objects.get(name='Admin')
        if group in request.user.groups.all():
            return 1
        else:
            return 2
    else:
        return auth_logout(request)

def auth_logout(request):
	logout(request)
	return HttpResponseRedirect('/gmt/login/')

@login_required
def reset_password(request,user_id):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    u = User.objects.get(username__exact=user_id)
    u.set_password(user_id)
    u.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
@login_required
def change_password(request):
    if request.method=='POST':
        user = request.user
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        if user.check_password(old_password) == True:
            u = User.objects.get(username__exact=user)
            u.set_password(new_password)
            u.save()
            user_log = authenticate(username=request.user.username, password=new_password)
            auth_login(request,user_log)
            messages.success(request, "correct")
            #return HttpResponseRedirect(request.path)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         #   return render_to_response('change_password.html',{'win_close':'1'},RequestContext(request))
        else:
            messages.success(request, "incorrect")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            #return HttpResponseRedirect(request.path)
         #   return render_to_response('change_password.html',{'popup':'1'},RequestContext(request))
    else:
        return render_to_response('change_password.html',{},RequestContext(request))

@login_required(login_url='/gmt/login/')
def user_manager(request):
	if check_user_active(request) != 1:
		return HttpResponse('Contact Admin')
	emp_list = Zser.objects.filter(Archived=False)
	user_list = User.objects.exclude(username="admin")
	usrnm_list = []
	emp_id_list = []
	for usr in user_list:
		usrnm_list.append(usr.username)
	
	for emp in emp_list:
		emp_id_list.append(emp.Emp_ID)
	
	for emp_id in emp_id_list:
		if emp_id not in usrnm_list:
			user =User.objects.create_user(emp_id, '',emp_id)
			user.is_staff = True
			user.is_active = False
			user.first_name = Zser.objects.get(Emp_ID=emp_id).Emp_Name
			user.save()
        
	user_list = User.objects.exclude(username="admin")
	groups = Group.objects.all()
	if request.method=="POST":
		for usr in user_list:
			if usr.username+"Deactivate" in request.POST:
				User.objects.filter(username=usr).update(is_active=False,is_staff=False)
			if usr.username+"Activate" in request.POST:
				User.objects.filter(username=usr).update(is_active=True,is_staff=True)
		user_list = User.objects.exclude(username="admin")
		lis = {'emp_list':emp_list,'user_list':user_list}
	groups = Group.objects.all()
	lis = {'emp_list':emp_list,'user_list':user_list}
	return render_to_response('user_manager.html',lis,context_instance = RequestContext(request))
	
	
@login_required(login_url='/gmt/login/')
def user_manager_2(request, emp_id=None):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    user_obj = User.objects.get(username=str(emp_id))
    groups = Group.objects.all()
    lis = {'groups':groups,'user_obj':user_obj}
    if request.method =='POST':
        if "add" in request.POST:
            group = request.POST['group']
            if group=='1':
                Group.objects.get(id=2).user_set.remove(user_obj)
            if group=='2':
                Group.objects.get(id=1).user_set.remove(user_obj)
            group_obj = Group.objects.get(id=group)
            group_obj.user_set.add(user_obj)
            user_obj = User.objects.get(username=str(emp_id))
            return render_to_response('user_manager_2.html',lis,context_instance = RequestContext(request))
    if request.method =='POST':
        if "remove" in request.POST:
            group = request.POST['group']
            if group=='1':
                Group.objects.get(id=2).user_set.add(user_obj)
            if group=='2':
                Group.objects.get(id=1).user_set.add(user_obj)
            group_obj = Group.objects.get(id=group)
            group_obj.user_set.remove(user_obj)
            user_obj = User.objects.get(username=str(emp_id))
            return render_to_response('user_manager_2.html',lis,context_instance = RequestContext(request))
    return render_to_response('user_manager_2.html',lis,context_instance = RequestContext(request))

def login(request):
	if request.user.is_active==True:
		return HttpResponseRedirect('/gmt/timesheet/')
	else:
		if request.method=='POST':
			uname = request.POST['username']
			pswrd = request.POST['password']
			user = authenticate(username=uname, password=pswrd)
			if user is not None:
				if user.is_active:
					auth_login(request,user)
					return HttpResponseRedirect('/gmt/timesheet/')
	return render_to_response('login.html',{},context_instance = RequestContext(request))


@login_required(login_url='/gmt/login/')
def add_timesheet(request,month=None):
    check_user_active(request)
    aaj = datetime.date.today()
    sd = aaj - datetime.timedelta(days=10)
    ed = aaj + datetime.timedelta(days=21)
    zs_cal  = ZS_Calender.objects.filter(Date__range=(sd,ed))
    if request.method=='POST' and 'timesubmit' not in request.POST:
        sd = date(int(request.POST['start_date'][0:4]),int(request.POST['start_date'][5:7]),int(request.POST['start_date'][8:10]))
        ed = date(int(request.POST['end_date'][0:4]),int(request.POST['end_date'][5:7]),int(request.POST['end_date'][8:10]))
        if sd != '' and ed != '':
            zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed))
    if request.method=='POST' and 'timesubmit' in request.POST:
        sd = date(int(request.POST['start_date'][0:4]),int(request.POST['start_date'][5:7]),int(request.POST['start_date'][8:10]))
        ed = date(int(request.POST['end_date'][0:4]),int(request.POST['end_date'][5:7]),int(request.POST['end_date'][8:10]))
        if sd != '' and ed != '':
            zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed))
        for t1 in zs_cal:
            for p1 in Project_Member.objects.filter(Zser=Zser.objects.get(Emp_ID=request.user.username)):
                if p1.Project.Start_Date<=t1.Date and p1.Project.End_Date>=t1.Date:
                    if request.POST[str(p1.Project.id)+str(t1.id)]=='':
                        if Time_Entry.objects.filter(Date=t1,Project=p1.Project,Zser=Zser.objects.get(Emp_ID=request.user.username)).count() > 0:
                            Time_Entry.objects.filter(Project=p1.Project,Zser=Zser.objects.get(Emp_ID=request.user.username),Date=t1).delete()
                    else:
                        hours =Decimal(request.POST[str(p1.Project.id)+str(t1.id)])
                        if Time_Entry.objects.filter(Date=t1,Project=p1.Project,Zser=Zser.objects.get(Emp_ID=request.user.username)).count() == 0:
                            Time_Entry.objects.create(Project=p1.Project,Zser=Zser.objects.get(Emp_ID=request.user.username),Date=t1,Hours=hours)
                        else:
                            Time_Entry.objects.filter(Project=p1.Project,Zser=Zser.objects.get(Emp_ID=request.user.username),Date=t1).update(Hours=hours)
    zs_calender_list = zs_cal.order_by('Date')
    mem_pro_list = Project_Member.objects.filter(Zser=Zser.objects.get(Emp_ID=request.user.username)).order_by('Project__TMS_ID').reverse()
    project_list = []
    for pro in mem_pro_list:
	    if pro.Project.End_Date >= sd and pro.Project.Start_Date <= ed and pro.Project.Archived==False:
		    project_list.append(pro)
    Time_Entry_List = Time_Entry.objects.filter(Zser=Zser.objects.get(Emp_ID=request.user.username),Date__in=zs_cal)
    lis = {'zs_calender_list':zs_calender_list,'project_list':project_list,'Time_Entry_List':Time_Entry_List,'sd':sd,'ed':ed,'aaj':aaj}
    return render_to_response('timesheet.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def check_ava(request,pro_id=None,zser_id=None):
	if check_user_active(request) != 1:
		return HttpResponse('Contact Admin')
	pro = Project.objects.get(id=pro_id)
	zs_cal = ZS_Calender.objects.filter(Date__range=(pro.Start_Date,pro.End_Date))
	zser = Zser.objects.get(id=zser_id)
	plan_hours = Planned_Hours.objects.filter(Zser=zser,Date__Date__range=(pro.Start_Date,pro.End_Date))
	pro_list=[]
	for ph in plan_hours:
		if ph.Project not in pro_list:
			pro_list.append(ph.Project)
	if pro not in pro_list:
		pro_list.append(pro)
	if request.method == 'POST':
		for t1 in zs_cal:
			for p1 in pro_list:
				if request.POST[str(p1.id)+str(t1.id)]=='':
					if Planned_Hours.objects.filter(Date=t1,Project=p1,Zser=zser).count() > 0:
						Planned_Hours.objects.filter(Date=t1,Project=p1,Zser=zser).delete()
				else:
					hours =Decimal(request.POST[str(p1.id)+str(t1.id)])
					if Planned_Hours.objects.filter(Date=t1,Project=p1,Zser=zser).count() == 0:
						Planned_Hours.objects.create(Date=t1,Project=p1,Zser=zser,Hours=hours)
					else:
						Planned_Hours.objects.filter(Date=t1,Project=p1,Zser=zser).update(Hours=hours)
	cal_hours = {}
	for cal in zs_cal:
		tot_hours = Planned_Hours.objects.filter(Zser=zser,Date=cal).aggregate(Sum('Hours'))['Hours__sum']
		if tot_hours == None:
			cal_hours[cal] = 0
		else:
			cal_hours[cal] = tot_hours
	plan_hours = Planned_Hours.objects.filter(Zser=zser,Date__Date__range=(pro.Start_Date,pro.End_Date))
	lis = {'pro':pro,'zs_cal':zs_cal,'plan_hours':plan_hours,'zser':zser,'pro_list':pro_list,'cal_hours':cal_hours}
	return render_to_response('check_ava.html',lis,context_instance = RequestContext(request))
	
@login_required(login_url='/gmt/login/')	
def add_pro_mem(request,id=None):
	if check_user_active(request) != 1:
		return HttpResponse('Contact Admin')
	pro = Project.objects.get(id=id)
	zsers = Zser.objects.filter(Archived=False)
	role_list = Pro_Role.objects.all()
	zser_skills = ZserSkills.objects.all()
	if request.method=='POST':
		for zser in zsers:
			if str(zser.id) in request.POST.keys():
				if Project_Member.objects.filter(Project=pro,Zser=zser).count() == 0:
					pro_id = request.POST[str(zser.id)+'Role']
					#if request.POST[str(zser.id)+'ZS_Rate']== '':
					#	zs_r = 0
					#else:
					#	zs_r = request.POST[str(zser.id)+'ZS_Rate']
					#if request.POST[str(zser.id)+'TMS_BillingRate'] == '':
					tms_r = Pro_Role.objects.get(id=pro_id).BillingRate
					#else:
					#	tms_r = request.POST[str(zser.id)+'TMS_BillingRate']
					Project_Member.objects.create(Project=pro,Zser=zser,Role=Pro_Role.objects.get(id=pro_id),ZS_Rate=0,TMS_BillingRate=tms_r)
				else:
					pro_id = request.POST[str(zser.id)+'Role']
					ZS_Rate= 0 #Decimal(request.POST[str(zser.id)+'ZS_Rate'])
					Tms_Billing_rate = Pro_Role.objects.get(id=pro_id).BillingRate
					Project_Member.objects.filter(Project=pro,Zser=zser).update(Role=Pro_Role.objects.get(id=pro_id),ZS_Rate=ZS_Rate,TMS_BillingRate=Tms_Billing_rate)
			else:
				Project_Member.objects.filter(Project=pro,Zser=zser).delete()
			if 'm_'+str(zser.id) in request.POST.keys():
				if Project_Manager.objects.filter(Project=pro,Zser=zser).count() == 0:
					Project_Manager.objects.create(Project=pro,Zser=zser)
			else:
				Project_Manager.objects.filter(Project=pro,Zser=zser).delete()
		#redirect_url = reverse('plan_hours/'+str(id))
		return HttpResponseRedirect('/gmt/add_master/plan_hours/'+str(id)+'/')
	pro_mem_list = Project_Member.objects.filter(Project=pro)
	pro_mng_list = Project_Manager.objects.filter(Project=pro)
	zser_avl = {}
	zser_plnd_hr = {}
	zser_act_hr = {}
	wrkng_days = ZS_Calender.objects.filter(Date__range=(pro.Start_Date,pro.End_Date)).aggregate(Sum('working_day'))['working_day__sum']
	for zser in Zser.objects.filter(Archived=False):
		hours = Planned_Hours.objects.filter(Zser=zser,Date__Date__range=(pro.Start_Date,pro.End_Date)).aggregate(Sum('Hours'))['Hours__sum']
		if hours == None:
			zser_avl[zser] = 100
		else:
			zser_avl[zser] =100-round((int(hours)/(wrkng_days*.08)))
		pln_hours = Planned_Hours.objects.filter(Zser=zser,Project=pro).aggregate(Sum('Hours'))['Hours__sum']
		if pln_hours == None:
			zser_plnd_hr[zser] = 0
		else:
			zser_plnd_hr[zser] = pln_hours
		act_hours = Time_Entry.objects.filter(Zser=zser,Project=pro).aggregate(Sum('Hours'))['Hours__sum']
		if act_hours == None:
			zser_act_hr[zser] = 0
		else:
			zser_act_hr[zser] = act_hours
	lis = {'pro_mng_list':pro_mng_list,'zser_act_hr':zser_act_hr,'pro_mem_list':pro_mem_list,'zsers':zsers,'pro':pro,'role_list':role_list,'zser_skills':zser_skills,'zser_avl':zser_avl,'zser_plnd_hr':zser_plnd_hr}
	return render_to_response('add_pro_mem.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def plan_hours(request,id=None):
	if check_user_active(request) != 1:
		return HttpResponse('Contact Admin')
	pro= Project.objects.get(id=id)
	zs_cal = ZS_Calender.objects.filter(Date__range=(pro.Start_Date,pro.End_Date))
	pro_mem_list = Project_Member.objects.filter(Project=pro)
	if request.method=='POST':
		for t1 in ZS_Calender.objects.filter(Date__range=(pro.Start_Date,pro.End_Date)):
			for p1 in Project_Member.objects.filter(Project=pro):
				if request.POST[str(p1.Zser.id)+str(t1.id)]=='':
					if Planned_Hours.objects.filter(Date=t1,Project=pro,Zser=p1.Zser).count() > 0:
						Planned_Hours.objects.filter(Date=t1,Project=pro,Zser=p1.Zser).delete()
				else:
					hours =Decimal(request.POST[str(p1.Zser.id)+str(t1.id)])
					if Planned_Hours.objects.filter(Date=t1,Project=pro,Zser=p1.Zser).count() == 0:
						Planned_Hours.objects.create(Project=pro,Zser=p1.Zser,Date=t1,Hours=hours)
					else:
						Planned_Hours.objects.filter(Date=t1,Project=pro,Zser=p1.Zser).update(Hours=hours)
	plan_hours = Planned_Hours.objects.filter(Project=pro)
	lis = {'pro':pro,'pro_mem_list':pro_mem_list,'zs_cal':zs_cal,'plan_hours':plan_hours}
	return render_to_response('add_pro_mem_plan_hour.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def add_pro(request,id=None):
    check_user_active(request)
    pro_mngs = Project_Manager.objects.all()
    if id=='new':
        if request.user.is_superuser == False:
            return HttpResponse("Only PMO can add new project.")
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            if form.is_valid():
                form.save()
                redirect_url = reverse('add_pro')
                return HttpResponseRedirect(redirect_url)
            else:
                lis = {'form':form,'flag':'Add'}
                return render_to_response('add_pro_new.html',lis,context_instance = RequestContext(request))
        else:
            form = ProjectForm()
            lis = {'form':form,'flag':'Add'}
            return render_to_response('add_pro_new.html',lis,context_instance = RequestContext(request))
    if id != None:
        pro = Project.objects.get(id=id)
        form = ProjectForm(instance = pro)
        project_list = Project.objects.all()
        if request.method == 'POST':
            form = ProjectForm(request.POST, instance = pro)
            lis = {'form':form}
            if form.is_valid():
                form.save()
                redirect_url = reverse('add_pro')
                return HttpResponseRedirect(redirect_url)
            else:
                return render_to_response('add_pro_new.html',lis,context_instance = RequestContext(request))
        else:
            lis = {'form':form,'flag':'Edit'}
            return render_to_response('add_pro_new.html',lis,context_instance = RequestContext(request))
    id_list = []
    for pro_s in ProjectStatus.objects.all():
        id_list.append(pro_s.id)
    clients = Client.objects.all().order_by('Name')
    clt_list=[]
    for clt in clients:
        clt_list.append(clt.id)
    arch = False
    archive = ''
    if request.method == 'POST' and 'pro_list' in request.POST:
        id_list = request.POST.getlist('pro_status_list')
        clt_list = request.POST.getlist('client_list')
        if 'archived' in request.POST:
            archive = 'checked'
            arch = True
    pro_status_list = {}
    for stat in ProjectStatus.objects.all().order_by('Status'):
        if stat.id in id_list:
            pro_status_list[stat] = 'Selected'
        else:
            pro_status_list[stat] = ''
    project_list = Project.objects.filter(Project_Status__in=ProjectStatus.objects.filter(id__in=id_list),Client__in=Client.objects.filter(id__in=clt_list),Archived=arch)
    pro_list={}
    for pro in project_list:
        pro_list[pro] = Project_Member.objects.filter(Project=pro)
    lis = {'pro_mngs':pro_mngs,'pro_list':pro_list,'pro_status':pro_status_list,'clt_list':clt_list,'clients':clients,'archived':archive}
    return render_to_response('add_pro.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def all_timesheet2(request,year=None):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    Month = datetime.date.today().month
    Year = datetime.date.today().year
    dt = datetime.date.today()
    sd = ZS_Calender.objects.filter(week=ZS_Calender.objects.get(Date=dt).week,year=ZS_Calender.objects.get(Date=dt).year)[0].Date
	#sd = dt - datetime.timedelta(days=3)
    ed = ZS_Calender.objects.filter(week=ZS_Calender.objects.get(Date=dt).week,year=ZS_Calender.objects.get(Date=dt).year).order_by('-id')[0].Date
    #ed = dt + datetime.timedelta(days=10)
    #zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed)).order_by('Date')
    zs_cal = ZS_Calender.objects.filter(week=ZS_Calender.objects.get(Date=dt).week,year=ZS_Calender.objects.get(Date=dt).year).order_by('Date')
    loc = Location.objects.all().order_by('loc')
    des = Designation.objects.all().order_by('Dsg')
    loc_sel = [Zser.objects.get(Emp_ID=request.user).Location.id]
    des_sel = ['19','15','13','11','7','2']
    actuals = "Checked"
    missing = "Checked"
    planned = ""
    show_skill = ""
    zser_lst = Zser.objects.filter(Archived=False).values_list('id',flat=True)
    all_skills = Skill.objects.all()
    skill_lst = Skill.objects.values_list('id',flat=True)
    if request.method == 'POST':
        sd = date(int(request.POST['start_date'][0:4]),int(request.POST['start_date'][5:7]),int(request.POST['start_date'][8:10]))
        ed = date(int(request.POST['end_date'][0:4]),int(request.POST['end_date'][5:7]),int(request.POST['end_date'][8:10]))
        if sd != '' and ed != '':
            zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed)).order_by('Date')
        loc_sel = request.POST.getlist('loc_list')
        zser_lst = request.POST.getlist('zser_lst')
        skill_lst = Skill.objects.filter(id__in=request.POST.getlist('skill_lst')).values_list('id',flat=True)
        des_sel = request.POST.getlist('des_list')
        if 'actuals' in request.POST:
            actuals = "Checked"
        else:
            actuals = ""
        if 'planned' in request.POST:
            planned = "Checked"
        else:
            planned = ""
        if 'missing' in request.POST:
            missing = "Checked"
        else:
            missing = ""
        if 'show_skill' in request.POST:
            show_skill = "Checked"
        else:
            show_skill = ""
    if skill_lst.count() == all_skills.count():
        zsers = Zser.objects.filter(id__in=zser_lst,Archived=False,Location__in=Location.objects.filter(id__in=loc_sel),Designation=Designation.objects.filter(id__in=des_sel)).order_by('Emp_Name')
    else:
        zser_lst = ZserSkills.objects.filter(Skill__in=Skill.objects.filter(id__in=request.POST.getlist('skill_lst'))).values_list('Zser__id',flat=True)
        zsers = Zser.objects.filter(id__in=zser_lst,Archived=False,Location__in=Location.objects.filter(id__in=loc_sel),Designation=Designation.objects.filter(id__in=des_sel)).order_by('Emp_Name')
    all_zsers = Zser.objects.filter(Archived=False,Location__in=Location.objects.filter(id__in=loc_sel),Designation=Designation.objects.filter(id__in=des_sel)).order_by('Emp_Name')
    zser_proj = {}
    if  ed < dt:
	    tot_days = ZS_Calender.objects.filter(Date__range=(sd,ed),working_day=1).count()
    else:
        tot_days = ZS_Calender.objects.filter(Date__range=(sd,dt),working_day=1).count()
    for emp in zsers:
        act_plan = {}
        x = 0
        if actuals == "Checked":
            dt_list_actual = {}
            for dt in zs_cal:
                act_hours = Time_Entry.objects.filter(Zser=emp,Date=dt).aggregate(Sum('Hours'))['Hours__sum']
                if act_hours == None:
                    dt_list_actual[dt]=''
                else:
                    dt_list_actual[dt]=str(act_hours)
                    x = x + act_hours
            dt_list_actual['act_tot'] = str(Time_Entry.objects.filter(Zser=emp,Date__in=zs_cal).aggregate(Sum('Hours'))['Hours__sum'])
            dt_list_actual['coach'] = CoachMap.objects.filter(Team_Member=emp)
            act_plan['Actuals'] = dt_list_actual
        if planned == "Checked":
            dt_list_plan = {}
            for dt in zs_cal:
                plan_hours = Planned_Hours.objects.filter(Zser=emp,Date=dt).aggregate(Sum('Hours'))['Hours__sum']
                if plan_hours == None:
                    dt_list_plan[dt]=''
                else:
                    dt_list_plan[dt]=str(plan_hours)
                    x = x + plan_hours
            dt_list_plan['pln_tot'] = str(Planned_Hours.objects.filter(Zser=emp,Date__in=zs_cal).aggregate(Sum('Hours'))['Hours__sum'])
            act_plan['Planned'] = dt_list_plan
        if x < tot_days*8 and missing == "Checked":
            zser_proj[emp] = act_plan
        elif missing != "Checked":
            zser_proj[emp] = act_plan
    zser_skill = []
    if show_skill == "Checked":
        zser_skill = ZserSkills.objects.filter(Zser__in=zsers)		
    if 'Export' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="CHRONUS-Availability_By_Member.csv"'
        writer = csv.writer(response)
        dt_lis =[]
        dt_lis.append("Name")
        dt_lis.append("Designation")
        dt_lis.append("Location")
        dt_lis.append("Coach")
        dt_lis.append("Actuals/Planned")
        for dt in zs_cal:
            x = dt.Date
            dt_lis.append(x)
        dt_lis.append('Total')
        writer.writerow(dt_lis)
        for key,val in zser_proj.items():
            for a_p,hr in val.items():
                r = []
                r.append(key)
                r.append(key.Designation)
                r.append(key.Location)
                c_lis = ''
                if hr['coach'] != None:
                    for coach in hr['coach']:
                        c_lis = c_lis + coach.Coach.Coach.Emp_Name
                r.append(c_lis)
                r.append(a_p)
              #  r.append(hr)
                for dt in zs_cal:
#				for dt,hr in hr.items():
                    r.append(hr[dt])
                if a_p == 'Actuals':
                    r.append(hr['act_tot'])
                elif a_p == 'Planned':
                    r.append(hr['pln_tot'])
                writer.writerow(r)
        return response
    lis = {'missing':missing,'zser_lst':zser_lst,'all_zser':all_zsers,'zser_proj':zser_proj,'zs_cal':zs_cal,'sd':sd,'ed':ed,'loc_list':loc,'loc_sel':loc_sel,'des_list':des,'des_sel':des_sel,'actual':actuals,'plan':planned,'all_skills':all_skills,'skill_lst':skill_lst,'zser_skill':zser_skill,'show_skill':show_skill}
    return render_to_response('all_timesheet2.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def all_timesheet1(request,year=None):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    Month = datetime.date.today().month
    Year = datetime.date.today().year
    dt = datetime.date.today()
    sd = dt - datetime.timedelta(days=5)
    ed = dt + datetime.timedelta(days=10)
    zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed))
    id_list = ['2','1','3','4','5']
    sap_list = []
    for sap in SAP.objects.all():
        sap_list.append(str(sap.id))
    if request.method == 'POST':
        sd = date(int(request.POST['start_date'][0:4]),int(request.POST['start_date'][5:7]),int(request.POST['start_date'][8:10]))
        ed = date(int(request.POST['end_date'][0:4]),int(request.POST['end_date'][5:7]),int(request.POST['end_date'][8:10]))
        id_list = request.POST.getlist('pro_status_list')
        sap_list = request.POST.getlist('sap_list')
        if sd != '' and ed != '':
            zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed))
    zsers = Zser.objects.filter().order_by('Emp_Name')
    projects = Project.objects.filter(Project_Status__in=ProjectStatus.objects.filter(id__in=id_list),SAP_Code__in=SAP.objects.filter(id__in=sap_list))
    zser_list = []
    proj_list = []
    proj_zser = {}
    for emp in zsers:
        if Time_Entry.objects.filter(Zser=emp,Date__Date__range=(sd,ed)).count()>0:
            zser_list.append(emp)
    for pro in projects:
        if Time_Entry.objects.filter(Project=pro,Date__Date__range=(sd,ed)).count()>0:
            proj_list.append(pro)
    for pro in proj_list:
        emp_list={}
        for emp in zser_list:
            time_list = []
            ent_list = Time_Entry.objects.filter(Zser=emp,Project=pro,Date__Date__range=(sd,ed))
            if ent_list.count()>0:
                for entry in ent_list:
                    time_list.append(entry)
            if len(time_list)>0:
                emp_list[emp] = time_list
        proj_zser[pro] = emp_list
    pro_status_list = {}
    for stat in ProjectStatus.objects.all().order_by('Status'):
        if str(stat.id) in id_list:
            pro_status_list[stat] = 'Selected'
        else:
            pro_status_list[stat] = ''
    sap_code_list = {}
    for sap in SAP.objects.all():
        if str(sap.id) in sap_list:
            sap_code_list[sap] = 'Selected'
        else:
            sap_code_list[sap] = ''
    lis = {'proj_zser':proj_zser,'zs_cal':zs_cal,'sd':sd,'ed':ed,'pro_status':pro_status_list,'sap_code_list':sap_code_list}
    return render_to_response('all_timesheet1.html',lis,context_instance = RequestContext(request))

	
	
@login_required(login_url='/gmt/login/')
def all_timesheet3(request,year=None):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    Month = datetime.date.today().month
    Year = datetime.date.today().year
    sd = date(Year,Month,1)
    dt = datetime.date.today()
    ed=dt.replace(month=dt.month+1, day=1) - datetime.timedelta(days=1)
    zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed))
    if request.method == 'POST':
        sd = request.POST['start_date']
        ed = request.POST['end_date']
        if sd != '' and ed != '':
            zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed))
    zsers = Zser.objects.filter(Archived=False).order_by('Emp_Name')
    projects = Project.objects.all()
    time_entry = Time_Entry.objects.filter(Date__Date__range=(sd,ed))
    zser_list = []
    proj_list = []
    zser_proj = {}
    for emp in zsers:
        if Time_Entry.objects.filter(Zser=emp,Date__Date__range=(sd,ed)).count()>0:
            zser_list.append(emp)
    for pro in projects:
        if Time_Entry.objects.filter(Project=pro,Date__Date__range=(sd,ed)).count()>0:
            proj_list.append(pro)
    for emp in zser_list:
        pro_list={}
        for pro in proj_list:
            time_list = []
            ent_list = Time_Entry.objects.filter(Zser=emp,Project=pro,Date__Date__range=(sd,ed))
            if ent_list.count()>0:
                for entry in ent_list:
                    time_list.append(entry)
            if len(time_list)>0:
                pro_list[pro] = time_list
        zser_proj[emp] = pro_list
    lis = {'zser_proj':zser_proj,'zser_list':zser_list,'zs_cal':zs_cal,'proj_list':proj_list,'sd':sd,'ed':ed}
    return render_to_response('all_timesheet1.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def all_timesheet_menu(request,year=None):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    lis = {}
    return render_to_response('all_timesheet_menu.html',lis,context_instance = RequestContext(request))
	
	

@login_required(login_url='/gmt/login/')
def my_profile(request):
	check_user_active(request)
	zser = Zser.objects.get(Emp_ID=request.user)
	all_skills = Skill.objects.all()
	if request.method=='POST':
		for skill in all_skills:
			if str(skill.id)+'Add' in request.POST:
				ZserSkills.objects.create(Zser=zser,Skill=skill)
			if str(skill.id)+'Remove' in request.POST:
				ZserSkills.objects.filter(Zser=zser,Skill=skill).delete()
	my_coach = CoachMap.objects.filter(Team_Member=zser)
	my_skills = ZserSkills.objects.filter(Zser=zser)
	my_skill_list = []
	skill_list={}
	for skill in my_skills:
		my_skill_list.append(skill.Skill)
	for skill in all_skills:
		if skill in my_skill_list:
			skill_list[skill]='Remove'
		else:
			skill_list[skill]='Add'
	lis = {'zser':zser,'my_skills':my_skills,'my_coach':my_coach,'all_skills':skill_list}
	return render_to_response('my_profile.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def my_projects(request,arch="no",pro_id=None):
    check_user_active(request)
    if arch == "no":
        pro_list = Project_Manager.objects.filter(Zser=Zser.objects.get(Emp_ID=request.user),Project__in=Project.objects.filter(Archived=False))
    else:
        pro_list = Project_Manager.objects.filter(Zser=Zser.objects.get(Emp_ID=request.user))
    projects = {}
    pln_hrs = {}
    act_hrs = {}
    for pro in pro_list:
        project_det = {}
        pln_hours = Planned_Hours.objects.filter(Project=pro.Project).aggregate(Sum('Hours'))['Hours__sum']
        project_det['pln_hour'] = pln_hours
        act_hours = Time_Entry.objects.filter(Project=pro.Project).aggregate(Sum('Hours'))['Hours__sum']
        project_det['act_hour'] = act_hours
        project_det['team_mem'] = Project_Member.objects.filter(Project=pro.Project)
        project_det['sap_code'] = proj_sap.objects.filter(pro=pro.Project)
        projects[pro] = project_det
    pro_mems = []
    pro_mngs = []
    lis = {'arch':arch,'act_hrs':act_hrs,'pln_hrs':pln_hrs,'pro_mngs':pro_mngs,'pro_mems':pro_mems,'pro_list':pro_list,'projects':projects}
    if pro_id != None:
        sel_pro = Project.objects.get(id=pro_id)
        sel_pro_mems = Project_Member.objects.filter(Project= sel_pro)
        zs_cal = ZS_Calender.objects.filter(Date__range=(sel_pro.Start_Date,sel_pro.End_Date))
        time_sheets = Time_Entry.objects.filter(Project=sel_pro)
        plan_sheets = Planned_Hours.objects.filter(Project=sel_pro)
        lis['plan_sheets'] = plan_sheets
        lis['time_entry'] = time_sheets
        lis['sel_pro'] = sel_pro
        lis['sel_pro_mems'] = sel_pro_mems
        lis['zs_cal'] = zs_cal
        mem_act_hrs = {}
        mem_pln_hrs = {}
        for mem in sel_pro_mems:
            mem_act_hours = Time_Entry.objects.filter(Project=sel_pro,Zser=mem.Zser).aggregate(Sum('Hours'))['Hours__sum']
            if mem_act_hours==None:
                mem_act_hrs[mem.Zser] = ''
            else:
                mem_act_hrs[mem.Zser] = mem_act_hours
            mem_pln_hours = Planned_Hours.objects.filter(Project=sel_pro,Zser=mem.Zser).aggregate(Sum('Hours'))['Hours__sum']
            if mem_pln_hours==None:
                mem_pln_hrs[mem.Zser] = ''
            else:
                mem_pln_hrs[mem.Zser] = mem_pln_hours
        lis['mem_act_hrs'] = mem_act_hrs
        lis['mem_pln_hrs'] = mem_pln_hrs
        if request.method == 'POST':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Project Report.csv"'
            writer = csv.writer(response)
            dt_lis = []
            dt_lis.append('Project : '+sel_pro.TMS_ID+" - "+sel_pro.Project_Name)
            writer.writerow(dt_lis)
            dt_lis = []
            dt_lis.append('Report Time : '+str(datetime.datetime.now()))
            writer.writerow(dt_lis)
            writer.writerow('')
            dt_lis =[]
            dt_lis.append("Team Member")
            dt_lis.append("Actuals/Planned")
            for dt in zs_cal:
               x = dt.Date
               dt_lis.append(x)
            dt_lis.append('Total')
            writer.writerow(dt_lis)
            for mem in sel_pro_mems:
                r = []
                r1 = []
                r.append(mem.Zser)
                r.append('Actuals')
                r1.append(mem.Zser)
                r1.append('Planned')
                for dt in zs_cal:
                    r.append(Time_Entry.objects.filter(Project=sel_pro,Zser=mem.Zser,Date=dt).aggregate(Sum('Hours'))['Hours__sum'])
                    r1.append(Planned_Hours.objects.filter(Project=sel_pro,Zser=mem.Zser,Date=dt).aggregate(Sum('Hours'))['Hours__sum'])
                r.append(Time_Entry.objects.filter(Project=sel_pro,Zser=mem.Zser).aggregate(Sum('Hours'))['Hours__sum'])
                r1.append(Planned_Hours.objects.filter(Project=sel_pro,Zser=mem.Zser).aggregate(Sum('Hours'))['Hours__sum'])
                writer.writerow(r)
                writer.writerow(r1)
            return response
    return render_to_response('my_projects.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def my_projects_finance(request,pro_id=None):
    pro = Project.objects.get(id=pro_id)
    sd = pro.Start_Date
    ed = pro.End_Date
    if request.method=='POST':
        sd = date(int(request.POST['start_date'][0:4]),int(request.POST['start_date'][5:7]),int(request.POST['start_date'][8:10]))
        ed = date(int(request.POST['end_date'][0:4]),int(request.POST['end_date'][5:7]),int(request.POST['end_date'][8:10]))
    if sd != '' and ed != '':
        zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed))
    plan_bud = 0
    act_bud = 0
    margin = 0
    pro_mem = Project_Member.objects.filter(Project=pro)
    pro_mng = Project_Manager.objects.filter(Project=pro)
    pln_hr_mem = {}
    rol_hr_lis = {}
    for mem in Project_Member.objects.filter(Project=pro):
       if mem.Role not in rol_hr_lis:
           rol_hr_lis[mem.Role] = [str(0)]
       li = []	
       p_hr = Planned_Hours.objects.filter(Project=pro,Zser=mem.Zser,Date__in=zs_cal).aggregate(Sum('Hours'))['Hours__sum']
       li.append(p_hr)
       a_hr = Time_Entry.objects.filter(Project=pro,Zser=mem.Zser,Date__in=zs_cal).aggregate(Sum('Hours'))['Hours__sum']
       li.append(a_hr)
       if a_hr != None and p_hr != None:
           li.append(p_hr-a_hr)
           li.append(round((p_hr-a_hr)*mem.TMS_BillingRate,1))
           margin = margin+round((p_hr-a_hr)*mem.TMS_BillingRate,1)
       else:
           li.append("")
           li.append("")
       if p_hr != None:
           plan_bud = plan_bud + p_hr*mem.TMS_BillingRate
           li.append(round(p_hr*mem.TMS_BillingRate,1))
        #   rol_hr_lis[mem.Role] = [str( p_hr*mem.TMS_BillingRate + Decimal(rol_hr_lis[mem.Role][0])) , rol_hr_lis[mem.Role][1]]
       else:
           li.append(0)
       if  a_hr != None:
           act_bud = act_bud + a_hr*mem.TMS_BillingRate
           li.append(round(a_hr*mem.TMS_BillingRate,1))
           rol_hr_lis[mem.Role] = [ str( a_hr*mem.TMS_BillingRate + Decimal(rol_hr_lis[mem.Role][0]))]
           #rol_hr_lis[mem.Role] = [ rol_hr_lis[mem.Role][0],str( a_hr*mem.TMS_BillingRate + Decimal(rol_hr_lis[mem.Role][1]))]
       else:
           li.append(0)

       pln_hr_mem[mem] = li
    if pro.Budget != 0:
	    utl_per = str(round((act_bud/pro.Budget)*100,1)).replace(",", "")
    else:
        utl_per = 0
    total_bud = str(pro.Budget).replace(",", "")
    act_bud = str(round((act_bud),1)).replace(",", "")
    plan_bud = str(round((plan_bud),1)).replace(",", "")
    lis = {'sd':sd,'ed':ed,'plan_bud':plan_bud,'pro':pro,'act_bud':act_bud,'total_bud':total_bud,'utl_bud':utl_per,'pro_mem':pro_mem,'pro_mng':pro_mng,'pln_hr_mem':pln_hr_mem,'rol_hr_lis':rol_hr_lis,'margin':margin}
    return render_to_response('my_projects_finance.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def my_projects_finance_change_role(request,pro_id=None):
    pro = Project.objects.get(id=pro_id)
    pro_mem = Project_Member.objects.filter(Project=pro)
    pro_mng = Project_Manager.objects.filter(Project=pro)
    role_list = Pro_Role.objects.all()
    if request.method == 'POST':
        for mem in pro_mem:
            mem_role = request.POST[str(mem.id)+'Role']
            sel_role = Pro_Role.objects.get(id=mem_role)
            Project_Member.objects.filter(id=mem.id).update(Role=sel_role,TMS_BillingRate=sel_role.BillingRate)
            if request.POST[str(mem.id)+'text'] != '':
                Project_Member.objects.filter(id=mem.id).update(TMS_BillingRate=request.POST[str(mem.id)+'text'])
    pro_mem = Project_Member.objects.filter(Project=pro)
    lis={'pro':pro,'pro_mem':pro_mem,'role_list':role_list,'pro_mng':pro_mng}
    return render_to_response('my_projects_finance_role.html',lis,context_instance = RequestContext(request))
	
@login_required(login_url='/gmt/login/')	
def help(request):
	check_user_active(request)
	lis = {}
	return render_to_response('help.html',lis,context_instance = RequestContext(request))

	
@login_required(login_url='/gmt/login/')
def reports(request):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    lis = {}
    return render_to_response('reports_menu.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def reports_pro(request):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    clients = Client.objects.all()
    clt_list=[]
    for clt in clients:
        clt_list.append(clt.id)
    sap_all = SAP.objects.all()
    sap_list = []
    for sap in sap_all:
        sap_list.append(sap.id)
    fte_all = FTE_Model.objects.all()
    fte_list = []
    for fte in fte_all:
        fte_list.append(fte.id)
    pro_status_list = {}
    id_list = ['1','2','3','4','5']
    pro_list = Project.objects.filter(Project_Status__in=ProjectStatus.objects.filter(id__in=id_list),Client__in=Client.objects.filter(id__in=clt_list),Archived=False)
    lis = {}
    if request.method == 'POST':
        id_list = request.POST.getlist('pro_status_list')
        clt_list = request.POST.getlist('client_list')
        #sap_list = request.POST.getlist('sap_list')
        fte_list = request.POST.getlist('fte_list')
        if 'archived' in request.POST:
            lis['archived'] = 'checked'
            pro_list = Project.objects.filter(FTE__in=FTE_Model.objects.filter(id__in=fte_list),SAP_Code__in=SAP.objects.filter(id__in=sap_list),Project_Status__in=ProjectStatus.objects.filter(id__in=id_list),Client__in=Client.objects.filter(id__in=clt_list))
        else:
            pro_list = Project.objects.filter(FTE__in=FTE_Model.objects.filter(id__in=fte_list),SAP_Code__in=SAP.objects.filter(id__in=sap_list),Project_Status__in=ProjectStatus.objects.filter(id__in=id_list),Client__in=Client.objects.filter(id__in=clt_list),Archived=False)
    for stat in ProjectStatus.objects.all().order_by('Status'):
        if str(stat.id) in id_list:
            pro_status_list[stat] = 'Selected'
        else:
            pro_status_list[stat] = ''
    lis['pro_list'] = pro_list
    lis['pro_status'] = pro_status_list
    lis['clients'] = clients
    lis['clt_list'] = clt_list
    lis['sap_list'] = sap_list
    lis['sap_all'] = sap_all
    lis['fte_list'] = fte_list
    lis['fte_all'] = fte_all
    tot_bud=0
    utl_bud = 0
    pro_list_2={}
    for pro in pro_list:
        pro_list_2[pro] = []
        tot_bud = tot_bud + pro.Budget
        pro_mng = Project_Manager.objects.filter(Project=pro)
        utl_bud_pro = 0
        for mem in Project_Member.objects.filter(Project=pro):
            if Time_Entry.objects.filter(Project=pro,Zser=mem.Zser).aggregate(Sum('Hours'))['Hours__sum'] != None:
                utl_bud_pro = utl_bud_pro + (mem.TMS_BillingRate*Time_Entry.objects.filter(Project=pro,Zser=mem.Zser).aggregate(Sum('Hours'))['Hours__sum'])
        utl_bud = utl_bud + utl_bud_pro
        pro_list_2[pro] = [round(utl_bud_pro,0),pro_mng,round(pro.Budget,0),round(pro.Budget-utl_bud_pro,0)]
    lis['tot_bud'] = round(tot_bud,0)
    lis['utl_bud'] = round(utl_bud,0)
    lis['pro_list_2'] = pro_list_2
    return render_to_response('reports.html',lis,context_instance = RequestContext(request))

	
@login_required(login_url='/gmt/login/')	
def shared_resource(request,tool_id=None,tool_inst_id=None,new_inst=None):
    check_user_active(request)
    tool_list = Tool.objects.all()
    table_flag = "0" 
    lis = {'tool_list':tool_list,'table_flag':"0"}
    if tool_id != None:
        tool_sel = Tool.objects.get(id=tool_id)
        tool_users = Tool_User.objects.filter(Tool=tool_sel)
        tool_admin = Tool_Admin.objects.filter(Tool=tool_sel)
        lis['tool_users'] = tool_users
        lis['tool_admin'] = tool_admin
        lis['msg'] = " "
        lis['table_flag'] = str(tool_id)
    if tool_inst_id !=None and tool_inst_id != "add_new":
        if request.method == 'POST':
            form = Tool_UserForm(request.POST,instance=Tool_User.objects.get(id=tool_inst_id))
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/gmt/shared_tool/"+tool_id+"/")
            else:
                lis['form'] = form
                lis['msg'] = " "
                return render_to_response('shared_resource.html',lis,context_instance = RequestContext(request))
        else:
            form = Tool_UserForm(instance=Tool_User.objects.get(id=int(tool_inst_id)))
            lis['form'] = form
            lis['msg'] = ""
            return render_to_response('shared_resource.html',lis,context_instance = RequestContext(request))
    if tool_inst_id=="add_new":
        if request.method == 'POST':
            form = Tool_UserForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/gmt/shared_tool/"+tool_id+"/")
        else:
            form = Tool_UserForm()
            lis['msg'] = " "
            lis['form'] = form
            if  Tool_Admin.objects.filter(Admin=Zser.objects.get(Emp_ID=request.user),Tool=tool_sel).count() > 0:
                lis['msg'] = ""
            else:
                lis['msg'] = "Only Admin can change."
    return render_to_response('shared_resource.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def shared_file(request,doc_id=None):
    tool_list = Tool.objects.all()
    doc_list = Document.objects.all()
    uploaded_by = Zser.objects.get(Emp_ID=request.user)
    lis = {'tool_list':tool_list,'doc_list':doc_list,'uploaded_by':uploaded_by}
    if doc_id != None and request.method == 'POST':
        form = DocForm(request.POST,request.FILES,instance=Document.objects.get(id=doc_id))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/gmt/shared_tool/files/")
        else:
            lis['form'] = form
            lis['flag'] = "1"
            return render_to_response('shared_file.html',lis,context_instance = RequestContext(request))
    if doc_id != None:
        form = DocForm(instance=Document.objects.get(id=int(doc_id)))
        lis['form'] = form
        lis['msg'] = "Edit Document"
        lis['flag'] = "1"
    return render_to_response('shared_file.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def shared_file_new(request):
    tool_list = Tool.objects.all()
    doc_list = Document.objects.all()
    uploaded_by = Zser.objects.get(Emp_ID=request.user)
    lis = {'tool_list':tool_list,'doc_list':doc_list,'uploaded_by':uploaded_by}
    form = DocForm()
    lis['form'] = form
    lis['msg'] = "Add Document"
    lis['flag'] = "1"
    if request.method == 'POST':
        form = DocForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/gmt/shared_tool/files/")
        else:
            lis['form'] = form
            return render_to_response('shared_file.html',lis,context_instance = RequestContext(request))
    return render_to_response('shared_file.html',lis,context_instance = RequestContext(request))
    
	
@login_required(login_url='/gmt/login/')
def avl_1_old(request):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    track_lis = Track.objects.all()
    des_lis = Designation.objects.all()
    zser_lis = Zser.objects.filter(Archived=0,Location=Location.objects.get(id=1))
    skill_lis = Skill.objects.all()
    lis = {}
    des_dd = ['19','15','13','11','7','2']
    lis['des_dd'] = Designation.objects.filter(id__in=des_dd)
    lis['track_dd'] = Track.objects.all()
    lis['zser_dd'] = Zser.objects.filter(Designation__in=lis['des_dd'],Archived=0,Location=Location.objects.get(id=1))
    lis['track_lis'] = track_lis
    lis['skill_lis'] = skill_lis
    lis['des_lis'] = des_lis
    lis['zser_lis'] = zser_lis
    aaj = datetime.date.today()
    sd = aaj 
    ed = aaj + datetime.timedelta(days=30)
    lis['sd'] = sd
    lis['ed'] = ed
    if request.method == 'POST':
        track_dd = request.POST.getlist('track_dd')
        lis['track_dd'] = Track.objects.filter(id__in=track_dd)
        des_dd = request.POST.getlist('des_dd')
        lis['des_dd'] = Designation.objects.filter(id__in=des_dd)
        zser_dd = request.POST.getlist('zser_dd')
        lis['zser_dd'] = Zser.objects.filter(id__in=zser_dd)
        lis['zser_lis'] = Zser.objects.filter(Archived=0,Track__in=lis['track_dd'],Designation__in=lis['des_dd'],Location=Location.objects.get(id=1))
        lis['sel_zser'] = Zser.objects.filter(Archived=0,Track__in=lis['track_dd'],Designation__in=lis['des_dd'],id__in=zser_dd,Location=Location.objects.get(id=1))
        sd = date(int(request.POST['start_date'][0:4]),int(request.POST['start_date'][5:7]),int(request.POST['start_date'][8:10]))
        ed = date(int(request.POST['end_date'][0:4]),int(request.POST['end_date'][5:7]),int(request.POST['end_date'][8:10]))
        if sd != '' and ed != '':
            zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed))
        lis['zs_cal'] = zs_cal
        lis['sd'] = sd
        lis['ed'] = ed
        mem_ava = {}
        for mem in lis['sel_zser']:
            mem_ava_lis = []
            mem_ava_lis.append(mem)
            x = 0
            by_dt_ava = {}
            for dt in ZS_Calender.objects.filter(Date__range=(sd,ed),working_day=1):
                by_dt_ava[dt] = 8
            if Zser_FTE.objects.filter(Team_mem=mem).count() > 0:
                for mem_FTE in Zser_FTE.objects.filter(Team_mem=mem):
                    for cal in zs_cal:
                        if mem_FTE.Start_Date <= cal.Date and mem_FTE.End_Date >= cal.Date and cal.working_day == 1:
                            x = x + 8*((mem_FTE.Staffing)/100)
                            if by_dt_ava[cal] > 0 :
                                by_dt_ava[cal] = by_dt_ava[cal] - 8*((mem_FTE.Staffing)/100)
            ava = round((100-(float(x)/(ZS_Calender.objects.filter(Date__range=(sd,ed),working_day=1).count()*.08))),1)
            if ava > 0:
                for cal in ZS_Calender.objects.filter(Date__range=(sd,ed),working_day=1):
                    y = Planned_Hours.objects.filter(Project__in=Project.objects.filter(FTE__in=FTE_Model.objects.filter(~Q(id=1))),Zser=mem,Date=cal).aggregate(Sum('Hours'))['Hours__sum']
                    if by_dt_ava[cal] > 0 and cal.working_day == 1 and y != None:
                        by_dt_ava[cal] = float(by_dt_ava[cal]) -  float(y)
                        x = float(x) + float(y)
            mem_ava_lis.append(by_dt_ava)
            ava = round((100-(float(x)/(ZS_Calender.objects.filter(Date__range=(sd,ed),working_day=1).count()*.08))),1)
            mem_ava_lis.append(ava)
            mem_ava_lis.append(ZserSkills.objects.filter(Zser=mem))
            if ava > 0:
                mem_ava[mem] = mem_ava_lis
        lis['mem_ava'] = mem_ava
    return render_to_response('avl_1.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def avl_1(request):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    track_lis = Track.objects.all()
    des_lis = Designation.objects.all()
    zser_lis = Zser.objects.filter(Archived=0,Location=Location.objects.get(id=1))
    skill_lis = Skill.objects.all()
    lis = {}
    des_dd = ['19','15','13','11','7','2']
    lis['des_dd'] = Designation.objects.filter(id__in=des_dd)
    lis['track_dd'] = Track.objects.all()
    lis['zser_dd'] = Zser.objects.filter(Designation__in=lis['des_dd'],Archived=0,Location=Location.objects.get(id=1))
    lis['track_lis'] = track_lis
    lis['skill_lis'] = skill_lis
    lis['des_lis'] = des_lis
    lis['zser_lis'] = zser_lis
    aaj = datetime.date.today()
    sd = aaj 
    ed = aaj + datetime.timedelta(days=30)
    lis['sd'] = sd
    lis['ed'] = ed
    if request.method == 'POST':
        track_dd = request.POST.getlist('track_dd')
        lis['track_dd'] = Track.objects.filter(id__in=track_dd)
        des_dd = request.POST.getlist('des_dd')
        lis['des_dd'] = Designation.objects.filter(id__in=des_dd)
        zser_dd = request.POST.getlist('zser_dd')
        lis['zser_dd'] = Zser.objects.filter(id__in=zser_dd)
        lis['zser_lis'] = Zser.objects.filter(Archived=0,Track__in=lis['track_dd'],Designation__in=lis['des_dd'],Location=Location.objects.get(id=1))
        lis['sel_zser'] = Zser.objects.filter(Archived=0,Track__in=lis['track_dd'],Designation__in=lis['des_dd'],id__in=zser_dd,Location=Location.objects.get(id=1))
        sd = date(int(request.POST['start_date'][0:4]),int(request.POST['start_date'][5:7]),int(request.POST['start_date'][8:10]))
        ed = date(int(request.POST['end_date'][0:4]),int(request.POST['end_date'][5:7]),int(request.POST['end_date'][8:10]))
        if sd != '' and ed != '':
            zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed))
        lis['zs_cal'] = zs_cal
        lis['sd'] = sd
        lis['ed'] = ed
        mem_ava = {}
        for mem in lis['sel_zser']:
            mem_ava_lis = []
            mem_ava_lis.append(mem)
            x = 0
            by_dt_ava = {}
            cur_mnth = int(datetime.datetime.now().month)
            for dt in ZS_Calender.objects.filter(Date__range=(sd,ed),working_day=1):
                by_dt_ava[dt] = 8
                if dt.Month <= cur_mnth:
                    y = Planned_Hours.objects.filter(Zser=mem,Date=dt).aggregate(Sum('Hours'))['Hours__sum'] 
                    if  y != None:
                        by_dt_ava[dt] = by_dt_ava[dt] - y
                        x = float(x) + float(y)
                else:
                    if Zser_FTE.objects.filter(Team_mem=mem).count() > 0:
                        for mem_FTE in Zser_FTE.objects.filter(Team_mem=mem):
                            if mem_FTE.Start_Date <= dt.Date and mem_FTE.End_Date >= dt.Date and dt.working_day == 1:
                                x = x + float(8*((mem_FTE.Staffing)/100))
                                by_dt_ava[dt] = by_dt_ava[dt] - 8*((mem_FTE.Staffing)/100)
                                y = Planned_Hours.objects.filter(Project__in=Project.objects.filter(FTE__in=FTE_Model.objects.filter(~Q(id__in=[1,4]))),Zser=mem,Date=dt).aggregate(Sum('Hours'))['Hours__sum']
                                if y != None:
                                    by_dt_ava[dt] = by_dt_ava[dt] - y
                                    x = float(x) + float(y)
            mem_ava_lis.append(by_dt_ava)
            ava = round((100-(float(x)/(ZS_Calender.objects.filter(Date__range=(sd,ed),working_day=1).count()*.08))),1)
            mem_ava_lis.append(ava)
            mem_ava_lis.append(ZserSkills.objects.filter(Zser=mem))
            mem_ava[mem] = mem_ava_lis
        lis['mem_ava'] = mem_ava
        if 'Export' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="CHRONUS-Availability_By_Member.csv"'
            writer = csv.writer(response)
            dt_lis =[]
            dt_lis.append("Name")
            dt_lis.append("Track")
            dt_lis.append("Designation")
            dt_lis.append("Skills")
            dt_lis.append("Availability")
            for dt in zs_cal:
                x = dt.Date
                dt_lis.append(x)
            writer.writerow(dt_lis)
            for key,val in mem_ava.items():
                r = []
                r.append(key)
                r.append(key.Track)
                r.append(key.Designation)
                skill_lis = ""
                for skill in val[3]:
                    skill_lis = skill_lis + str(skill.Skill) + "," 
                r.append(skill_lis)
                r.append(str(val[2])+"%")
                for cal in zs_cal:
                    if cal in val[1]:
                        r.append(val[1][cal])
                    else:
                        r.append('')
                writer.writerow(r)
            return response
    return render_to_response('avl_1.html',lis,context_instance = RequestContext(request))

	
@login_required(login_url='/gmt/login/')
def ftes(request):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    lis = {}    
    lis['fte_mem'] = Zser_FTE.objects.all()
    return render_to_response('ftes.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def ftes_new(request,id=None):
    if check_user_active(request) != 1:
        return HttpResponse('Contact Admin')
    lis = {}    
    if id != None:
        inst = Zser_FTE.objects.get(id=id)
        form = Zser_FTEForm(instance=inst)
        lis['form'] = form
        lis['inst'] = inst
        lis['flag'] = "Edit"
    else:
        form = Zser_FTEForm()
        lis['form'] = form
        lis['flag'] = "Add"
    lis['zsers'] = Zser.objects.filter(Archived=0)
    if request.method == 'POST':
        if id != None:
            inst = Zser_FTE.objects.get(id=id)
            form = Zser_FTEForm(request.POST,instance=inst)
        else:
            form = Zser_FTEForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/gmt/reports/availability/ftes/")
        else:
            lis['form'] = form
            return render_to_response('ftes_new.html',lis,context_instance = RequestContext(request))	
    return render_to_response('ftes_new.html',lis,context_instance = RequestContext(request))

import xlwt
@login_required(login_url='/gmt/login/')
def sap_summary(request,month=None):
    check_user_active(request)
    aaj = datetime.date.today()
    sap_loc = Zser.objects.get(Emp_ID=request.user.username).Location.sap_loc
    if aaj.day <= 15:
        sd = date(aaj.year,aaj.month,1)
        ed = date(aaj.year,aaj.month,15)
    else:
        sd = date(aaj.year,aaj.month,16)
        if aaj.month != 12:
            ld = date(aaj.year,aaj.month + 1,1)
            ed = date(aaj.year,aaj.month,(ld-datetime.timedelta(days=1)).day)
        else:
            ed = date(aaj.year,aaj.month,31)		
    zs_cal  = ZS_Calender.objects.filter(Date__range=(sd,ed))
    if request.method=='POST':
        sap_loc = request.POST['sap_loc']
        sd = date(int(request.POST['start_date'][0:4]),int(request.POST['start_date'][5:7]),int(request.POST['start_date'][8:10]))
        ed = date(int(request.POST['end_date'][0:4]),int(request.POST['end_date'][5:7]),int(request.POST['end_date'][8:10]))
        if sd != '' and ed != '':
            zs_cal = ZS_Calender.objects.filter(Date__range=(sd,ed))
    sap_lis = {}
    tot = []
    zser = Zser.objects.get(Emp_ID=request.user.username)
    staff_share = zser_sap.objects.filter(Zser=zser).aggregate(Sum('share'))['share__sum']
    for dt in zs_cal:
        if Time_Entry.objects.filter(Zser=zser,Date=dt).aggregate(Sum('Hours'))['Hours__sum'] != None:
            tot.append(round(Time_Entry.objects.filter(Zser=zser,Date=dt).aggregate(Sum('Hours'))['Hours__sum'],2))
        else:
            tot.append(0)
    sap_lis_all = []
    for pro in Project.objects.all():
        if pro.SAP_Code not in sap_lis_all:
            sap_lis_all.append(pro.SAP_Code)
    for sap in sap_lis_all:
        sap_dt_lis = {}
        y = 0
        for dt in zs_cal:
            x = 0
            for pro in Project.objects.filter(SAP_Code=sap):
                time_lis = Time_Entry.objects.filter(Zser=zser,Date=dt,Project=pro).aggregate(Sum('Hours'))['Hours__sum']
                if time_lis != None :
                    x = x + time_lis
                    y = y + time_lis
            if x == 0:
                sap_dt_lis[dt] = ''
            else:
                sap_dt_lis[dt] = round(x,2)
        if y > 0:
            sap_lis[sap] = sap_dt_lis
    lis = {'sd':sd,'ed':ed,'zs_cal':zs_cal,'sap_lis':sap_lis,'tot':tot,'staff_share':staff_share,'sap_loc':sap_loc}
    if 'Export' in request.POST:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=TSReport.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("SAP_Summary")
        dt_lis =[]
        dt_lis.append("Row")
        dt_lis.append("Employee ID")
        dt_lis.append("Project ID")
        dt_lis.append("Date")
        dt_lis.append("Work Location")
        dt_lis.append("Hours")
        dt_lis.append("Comments")
        for col_num in range(0,len(dt_lis)):
            ws.write(0,col_num,dt_lis[col_num])
        i = 1
        for sap,value in sap_lis.items():
            for dt in zs_cal:
                hrs = value[dt]
                dt_lis = []
                if hrs != '':
                    dt_lis.append(i)
                    dt_lis.append(request.user.username)
                    dt_lis.append(sap)
                    dt_lis.append(str(dt.year)+str('%02d' % dt.Month)+str('%02d' % dt.Day))
                    dt_lis.append(sap_loc)
                    dt_lis.append(hrs)
                    dt_lis.append('')
                    for col_num in range(0,len(dt_lis)):
                        ws.write(i,col_num,dt_lis[col_num])
                    i = i + 1
        wb.save(response)
        return response
    return render_to_response('sap_summary.html',lis,context_instance = RequestContext(request))

@login_required(login_url='/gmt/login/')
def utilization(request):
    des_lis = Designation.objects.all()
    des_info = {}
    for des in des_lis:
        info = []
        cnt = Zser.objects.filter(Archived=False,Designation=des).count()
        ed = datetime.date.today()
        sd = date(ed.year,ed.month,1)
        tot_hr = Time_Entry.objects.filter(Zser__in=Zser.objects.filter(Archived=False,Designation=des),Date__in=ZS_Calender.objects.filter(Date__range=(sd,ed))).aggregate(Sum('Hours'))['Hours__sum']
        tot_days = ZS_Calender.objects.filter(Date__range=(sd,ed),working_day=1).count()
        if tot_hr != None:
            utl = round((tot_hr/(8*tot_days*cnt))*100,2)
        else:
            utl = 0
        info.append(cnt)
        info.append(utl)
        des_info[des] = info
    lis = {'des_info':des_info}
    return render_to_response('utilization.html',lis,context_instance = RequestContext(request))
	
@login_required(login_url='/gmt/login/')
def my_staffing(request):
    sap_lis = SAP.objects.filter(Archived=False)
    zser = Zser.objects.get(Emp_ID=request.user.username)
    if request.method =='POST':
        for sap in sap_lis:
            shr = request.POST['sap'+str(sap.id)]
            if shr != '' and zser_sap.objects.filter(Zser=zser,sap=sap).count() == 0:
                zser_sap.objects.create(Zser=zser,sap=sap,share=shr)
            elif shr != '' and zser_sap.objects.get(Zser=zser,sap=sap) != None:
                zser_sap.objects.filter(Zser=zser,sap=sap).update(share=shr)
            elif shr == '' and zser_sap.objects.filter(Zser=zser,sap=sap).count() != 0:
                zser_sap.objects.filter(Zser=zser,sap=sap).delete()
    lis = {'sap_lis':sap_lis,'zser_sap':zser_sap.objects.filter(Zser=zser)}
    return render_to_response('my_staffing.html',lis,context_instance = RequestContext(request))		