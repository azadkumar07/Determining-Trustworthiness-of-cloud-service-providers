from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import xlrd
def date(s):
	if s=="":
		return 15
	s=s[::-1]
	ans=""
	for i in range(4):
		ans=s[i]+ans
	for i in range(21):
		if str(i+2000)==ans:
			return 15-i
	return 15
	

mp={}
scale=10
def pre():
	mx = [0,0,0,0,0,0,0,0,0,0,0]
	for i in mp:
		k=0
		for j in mp[i]:
			if j>mx[k]:
				mx[k]=j
			k=k+1
	lamda=0
	for i in mp:
		k=0
		for j in mp[i]:
			lamda+=k
			if j==0:
				j=((scale*lamda)+(mx[k]*lamda))%mx[k]
				j=((scale*j)+(lamda*j))%mx[k]
			mp[i][k]=round(scale-(mx[k]-j),1)
			k=k+1


def index(request):
	location="/dataset.xlsx"
	workbook=xlrd.open_workbook(location)
	sheet=workbook.sheet_by_index(0)
	data=[[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	cloud_provider=set([])
	for i in range(sheet.nrows):
		if i==0:
			continue
		cloud_provider.add(data[i][1])

	check={}
	for name in cloud_provider:
		name=name.upper()
		check[name]="false"
	total = [0,0,0,0,0,0,0,0,0,0,0,0]
	for name in cloud_provider:
		temp1=name
		temp1=temp1.upper()
		if check[temp1]=="true":
			continue
		a = [0,0,0,0,0,0,0,0,0,0,0,0]
		c=0
		for i in range(sheet.nrows):
			if i==0:
				continue
			temp2=data[i][1];
			temp2=temp2.upper()
			if temp2==temp1:
				c=c+1
				for j in range(12):
					sm=0
					if data[i][j+2]!="": 
						sm=sm+int(data[i][j+2])
					
					if data[i][14]!="":
						sm=sm*int(data[i][14])

					sm=sm/date(str(data[i][15]))

					a[j]=a[j]+sm


		for j in range(12):
			a[j]=c*a[j]
			total[j]=total[j]+a[j]
	check2={}
	for name in cloud_provider:
		name=name.upper()
		check2[name]="false"

	for name in cloud_provider:
		temp1=name
		temp1=temp1.upper()
		if check2[temp1]=="true":
			continue
		a = [0,0,0,0,0,0,0,0,0,0,0,0]
		c=0
		for i in range(sheet.nrows):
			if i==0:
				continue
			temp2=data[i][1];
			temp2=temp2.upper()
			if temp2==temp1:
				c=c+1
				for j in range(12):
					sm=0
					if data[i][j+2]!="": 
						sm=sm+int(data[i][j+2])
					
					if data[i][14]!="":
						sm=sm*int(data[i][14])
					
					sm=sm/date(str(data[i][15]))

					a[j]=a[j]+sm

		
		for j in range(12):
			a[j]=c*a[j]
			if total[j]==0:
				continue
			a[j]=(a[j]/total[j])*scale

			a[j]=round(a[j],1)
		b = [0,0,0,0,0,0,0,0,0,0,0]
		b[0]=a[0]
		for j in range(12):
			if j<=1:
				continue;
			b[j-1]=a[j]

		mp[name]=b
		check2[temp1]="true"
	pre()
	t0tal=0
	for name in mp:
		for i in mp[name]:
			t0tal+=i
	tmp={}
	for name in mp:
		temp=0
		for i in mp[name]:
			temp+=i
		temp*=scale
		tmp[name]=round((temp/t0tal)*100,1)

	return render(request,'index.html',{"cloud_provider":cloud_provider,"data":tmp})


def all(request):
	return render(request,'all.html',{"data":mp})

def company(request):
	cname=request.GET.get('company','1and1')
	Tdata=mp['1and1']
	for name in mp:
		if cname==name:
			Tdata=mp[name]
	return render(request,'company.html',{"Tdata":Tdata,"Tname":cname})



