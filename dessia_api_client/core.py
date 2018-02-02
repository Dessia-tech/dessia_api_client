#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 10:35:32 2017

@author: steven
"""

import requests

#import json
import jwt
import time
import getpass

import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy
jsonpickle_numpy.register_handlers()


class AuthenticationError(Exception):
    pass
    
class Client:
    def __init__(self,username=None,password=None,token=None,api_url='https://api.software.dessia.tech'):

        self.username=username
        self.password=password
        self.token=token
        if self.token:
            self.token_exp=jwt.decode(self.token,verify=False)['exp']
        else:
            self.token_exp=0.
        self.api_url=api_url
#        self.token_nbf=time.time()
    def _get_auth_header(self):
        if self.token_exp<time.time():
            if (not self.username)|(not self.password):
                if self.username is None:
                    self.username=input('Email(User)/name(Technical Account) for DessIA API:')
                else:
                    print('Using {} as email'.format(self.email))
                if self.password is None:
                    self.password=getpass.getpass('Password for DessIA API:')
            print('Token expired, reauth')
            # Authenticate
            r = requests.post('{}/auth'.format(self.api_url), json={"username": self.username,"password":self.password})
            print(r)
            if r.status_code==200:
                self.token=r.json()['access_token']
                self.token_exp=jwt.decode(self.token,verify=False)['exp']
                print('Auth in {}s'.format(r.elapsed.total_seconds()))
            else:
                raise AuthenticationError
                
        auth_header={'Authorization':'JWT {}'.format(self.token)}
        return auth_header
    
    auth_header=property(_get_auth_header)
    
    def CreateUser(self,email,password,first_name,last_name):
        data={'email':email,'password':password,'first_name':first_name,
              'last_name':last_name}
        r=requests.post('{}/users/create'.format(self.api_url),json=data)

        return r
    
    def CreateTechnicalAccount(self,name,password,company_id=None,active=None,admin=None):
        data={'name':name,'password':password}
        if company_id!=None:
            data['company_id']=company_id
        if active!=None:
            data['active']=active
        if admin!=None:
            data['admin']=admin
            
        r=requests.post('{}/technical_accounts/create'.format(self.api_url),
                        json=data,headers=self.auth_header)

        return r
    
    def VerifyEmail(self,token):
        data={'token':token}
        r=requests.post('{}/account/verify-email'.format(self.api_url),json=data)
        return r
        
    def MyAccount(self):
        r=requests.get('{}/account/infos'.format(self.api_url),headers=self.auth_header)
        return r
    
        
    def AddResult(self,result,name,infos,owner_type='user',owner_id=None):
        data={'result':jsonpickle.encode(result,keys=True),'name':name,'infos':infos}
        if owner_id:
            data['owner_type']=owner_type
            data['owner_id']=owner_id
        r=requests.post('{}/results/add'.format(self.api_url),
                        headers=self.auth_header,json=data)
        return r
    
    
    def SubmitJob(self,job_type,input_data):
        data={'job_type':job_type,'input_data':input_data}
        r=requests.post('{}/job/submit'.format(self.api_url),
                        headers=self.auth_header,json=data)
        return r
        
    def JobDetails(self,job_id):
        r=requests.get('{}/job/{}/infos'.format(self.api_url,job_id),

                       headers=self.auth_header)
        return r


    def CompanyDetails(self,company_id):
        r=requests.get('{}/companies/{}'.format(self.api_url,company_id),
                       headers=self.auth_header)
        return r
    
    def UserTeams(self):
        r=requests.get('{}/teams/list'.format(self.api_url),
                       headers=self.auth_header)
        return r
    
    def CreateTeam(self,name,membership=True):
        data={'name':name,'membership':membership}
        r=requests.post('{}/teams/create'.format(self.api_url),
                       headers=self.auth_header,json=data)
        return r
    
    def CreateProject(self,name,owner_type='user',owner_id=None):
        data={'name':name,'owner_type':owner_type,'owner_id':owner_id}
        r=requests.post('{}/projects/create'.format(self.api_url),
                       headers=self.auth_header,json=data)
        return r
    
    def CreateJob(self,celery_id,owner_type,owner_id):
        data={'celery_id':celery_id,'owner_type':owner_type,'owner_id':owner_id}
        r=requests.post('https://api.software.dessia.tech/jobs/create',
                       headers=self.auth_header,json=data)
        return r    

#    def SubmitJob(self,job_type,input_data,owner_type='user',owner_id=None):
#        data={'job_type':job_type,'input_data':input_data}
#        if owner_id:
#            data['owner_type']=owner_type
#            data['owner_id']=owner_id
#        r=requests.post('https://api.software.dessia.tech/jobs/submit',
#                        headers=self.auth_header,json=data)
#        return r
        
    
    def Users(self,users_id):
        r=requests.post('{}/users'.format(self.api_url),
                       headers=self.auth_header,json=users_id)
        return r
    
    def Teams(self,teams_id):
        r=requests.post('{}/teams'.format(self.api_url),
                       headers=self.auth_header,json=teams_id)
        return r
    
    def MyTeamsInvitation(self):
        r=requests.get('{}/account/team_invitations'.format(self.api_url),
                       headers=self.auth_header)
        return r
    
    
    def CreateResult(self,result,name,infos,owner_type='user',owner_id=None):
        data={'result':jsonpickle.encode(result,keys=True),'name':name,'infos':infos}
        if owner_id:
            data['owner_type']=owner_type
            data['owner_id']=owner_id
        r=requests.post('https://api.software.dessia.tech/results/create',
                        headers=self.auth_header,json=data)
        return r


    def Result(self,result_id):
        r=requests.get('https://api.software.dessia.tech/results/{}'.format(result_id),
                       headers=self.auth_header)
        return r

    def ResultDict(self,result_id):
        r=requests.get('https://api.software.dessia.tech/results/{}/dict'.format(result_id),
                       headers=self.auth_header)
        return r
    
    def ResultObject(self,result_id):
        r=requests.get('https://api.software.dessia.tech/results/{}/object'.format(result_id),
                       headers=self.auth_header)
        if r.status_code==200:
            return jsonpickle.decode(r.text,keys=True)
        else:
            return r
        
    def ResultSTLToken(self,result_id,solution_id):
        r=requests.get('https://api.software.dessia.tech/results/{}/solutions/{}/stl/token'.format(result_id,solution_id),
                       headers=self.auth_header)
        return r
        
    