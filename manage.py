# -*- coding: utf-8 -*-
#@todo: fazer reanalize e melhorias

import os
import tablib
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash, redirect, make_response
from mysql_query import A,respQuery

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='123456'
))

@app.route('/')
def index():
    return render_template('index.html')
    

def report_name(name):

    report = {
        "tss-ch" : "Tss Chile",
	"tss-ar" : "Tss Argentina",
	"tss-mx" : "Tss Mexico",
	"tss-br" : "Tss Brasil",
	"tss-rd" : "Tss Republica Dominicana",
	"tss-gt" : "Tss Guatemala",
	"tss-co" : "Tss Colombia",
	"tss-pe" : "Tss Peru",
	"tfx-ch" : "Tss Fixo Chile",
	"tfx-gt" : "Tss Fixo Guatemala",
	"tfx-eq" : "Tss Fixo Equador",
	"tfx-rd" : "Tss Fixo Republica Dominicana",
	"tfx-br" : "Tss Fixo Brasil",
	"tmb-br" : "Tss Mobile Brasil",
	"tmb-ar" : "Tss Mobile Argentina",
	"tnt-mx" : "TNT Mexico",
	"tis-oi" : "Tis Oi BR",
        "nas-br" : "Net Assist"
    }
    return report[name]

@app.route('/report', methods=['POST'])
def show_entries():
    secure_login()
    reportType = request.form


    #Relatorio McAfee
    if 'relatorioMcAfee' in reportType:  
    	mes = reportType['mes']
    	ano = reportType['ano']
    	pais = reportType['pais']
        if 'paginator' in reportType:
            template = reportType['paginator']
        else:
            template = 'show_entries2.html'
    	entries = respQuery(mes,ano,pais,0)
    	data = tablib.Dataset()
    	data.headers = ['CCID','PartnerID','EmaildaLicensa','SKU','Licensa','DataDeAtivacao','Pacote']
    	counter = len(entries)	
    	count = 0  
    	commas = ","
    	jsonYUI = ""
        report = report_name(pais)
        for entry in entries: 
            count+=1
            if count==counter: 
                commas = ""
            jsonYUI+= "{ccid:'%s',PartnerID:'%s',EmailDaLicensa:'%s',SKU:'%s',Licensa:'%s',DataDeAtivacao:'%s',Pacote:'%s' } %s " % \
            (entry.CCID,entry.PartnerID,entry.EmailDaLicensa,entry.SKU,entry.Licensa,entry.DataDeAtivacao,entry.Pacote,commas)
	    data.append([entry.CCID,entry.PartnerID,entry.EmailDaLicensa,entry.SKU,entry.Licensa,entry.DataDeAtivacao,entry.Pacote])
        with open('reportcsv/report.csv', 'wb') as f:
            f.write(data.csv)

	jsonYUI = jsonYUI.decode("utf-8", 'ignore')
    	return render_template(template, entries=jsonYUI,counter=counter, mes=mes, ano=ano, pais=pais, report=report)


    #relatorioTisOiAtivos
    if 'relatorioAutomatizadoOiAtivos' in reportType:
        mes = reportType['mes']
        ano = reportType['ano']
        pais = 'tis-oi'
        entries = respQuery(mes,ano,pais,1)
        data = tablib.Dataset()
        data.headers = ['Msisdn','Email','Produto','Pacote','DataCompra','Valor','CanalDeVenda']
        counter = len(entries)
        count = 0
        commas = ","
        jsonYUI = ""
	report = report_name(pais)
        if 'paginator' in reportType:
            template = reportType['paginator']
        else:
            template = 'show_entries3.html'

        for entry in entries:
            count+=1
            if count==counter:
                commas = ""
            jsonYUI+= "{Msisdn:'%s',Email:'%s',Produto:'%s',Pacote:'%s',DataCompra:'%s',Valor:'%s',CanalDeVenda:'%s'} %s " % \
            (entry.msisdn,entry.email,entry.produto,entry.pacote,entry.dt_compra,entry.valor,entry.ds_channelsale,commas)
            data.append([entry.msisdn,entry.email,entry.produto,entry.pacote,entry.dt_compra,entry.valor,entry.ds_channelsale])
        with open('reportcsv/report.csv', 'wb') as f:
            f.write(data.csv)

	jsonYUI = jsonYUI.decode("utf-8", 'ignore')
        return render_template(template, entries=jsonYUI,counter=counter, mes=mes, ano=ano, pais=pais, report=report)
    
    #relatorioTisOiCancelados
    if 'relatorioAutomatizadoOiCancelados' in reportType:
        mes = reportType['mes']
        ano = reportType['ano']
        pais = 'tis-oi'
        entries = respQuery(mes,ano,pais,2)
        data = tablib.Dataset()
        data.headers = ['Msisdn','Email','Produto','Pacote','DataCompra','DataDeCancelamento','Valor','CanalDeVenda','UsuarioCancelamento']
        counter = len(entries)
        count = 0
        commas = ","
        jsonYUI = ""
        if 'paginator' in reportType:
            template = reportType['paginator']
        else:
            template = 'show_entries4.html'
        report = report_name(pais)
        for entry in entries:
            count+=1
            if count==counter:
                commas = ""
            jsonYUI+= "{Msisdn:'%s',Email:'%s',Produto:'%s',Pacote:'%s',DataCompra:'%s',DataDeCancelamento:'%s',Valor:'%s',CanalDeVenda:'%s',UsuarioCancelamento:'%s'} %s " % \
            (entry.msisdn,entry.email,entry.produto,entry.pacote,entry.dt_compra,entry.dt_cancel,entry.valor,entry.ds_channelsale,entry.ds_profile,commas)
            data.append([entry.msisdn,entry.email,entry.produto,entry.pacote,entry.dt_compra,entry.dt_cancel,entry.valor,entry.ds_channelsale,entry.ds_profile])
        with open('reportcsv/report.csv', 'wb') as f:
            f.write(data.csv)

	jsonYUI = jsonYUI.decode("utf-8", 'ignore')
        return render_template(template, entries=jsonYUI,counter=counter, mes=mes, ano=ano, pais=pais, report=report)

    
    #relatorioNetAssist
    if 'relatorioNetAssist' in reportType:
        mes = reportType['mes']
        ano = reportType['ano']
        pais = 'nas-br'
        entries = respQuery(mes,ano,pais,0)
        data = tablib.Dataset()
        data.headers = ['Email','Cpf/Cnpj','Pacote','Data','Status']
        counter = len(entries)
        count = 0 
        commas = "," 
        jsonYUI = ""
        if 'paginator' in reportType:
            template = reportType['paginator']
        else:
            template = 'show_entries8.html'
        report = report_name(pais)
        for entry in entries:
            count+=1
            if count==counter:
                commas = ""
            jsonYUI+= "{Email:'%s',CpfCnpj:'%s',Pacote:'%s',Data:'%s',Status:'%s'} %s " % (entry.email,entry.cpfcnpj,entry.pacote,entry.data,entry.status,commas)
            data.append([entry.email,entry.cpfcnpj,entry.pacote,entry.data,entry.status])
        with open('reportcsv/report.csv', 'wb') as f:
            f.write(data.csv)

	jsonYUI = jsonYUI.decode("utf-8", 'ignore')
        return render_template(template, entries=jsonYUI,counter=counter, mes=mes, ano=ano, pais=pais, report=report)

    return redirect(url_for('type_report'))



@app.route('/download',methods=['GET'])
def download():
    secure_login()
    with open('reportcsv/report.csv', 'r') as f:
        csv= f.read()
    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=report.csv"
    return response

@app.route('/mcafee_report', methods=['POST'])
def mcafee_report():
    secure_login()
    reportType = request.form

    if 'relatorioMcAfee' in reportType:
        flash('Relatorio McAfee Repasse Recorrente')
        return render_template('mcafee_report.html')

    if 'relatorioAutomatizadoOiEmpresas' in reportType: 
        flash('Relatorio Automatizado Oi Empresas')
        return render_template('oi_report.html')

    if 'relatorioNetAssist' in reportType: 
        flash('Relatorio Net Assist - Tss Help Desk')
        return render_template('netassist_report.html')

    return redirect(url_for('type_report'))

@app.route('/type_report', methods=['GET'])
def type_report():
    secure_login()
    flash('Relatorios disponiveis')
    return render_template('type_report.html')

@app.route('/login', methods=['GET','POST'])  
def login():
    error = None
    if request.method == 'POST'	:
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username/password'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username/password'  
        else:
            session['logged_in'] = True
            #flash('your were logged in')
            return redirect(url_for('type_report'))
    return render_template('index.html',error=error)

def secure_login():
    if not session.get('logged_in'):
        flash('Por favor, realize o login.')
        abort('401')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    #flash('you were logged out')
    return redirect(url_for('index'))



if __name__ == '__main__':
#roda o app normal usando o 127.0.0.1:5000	
    app.run() # roda assim python manage.py runserver
#se caso quisermos acessar a aplicacao de qualquer host dentro da intranet    
#    app.run(host='0.0.0.0',port=5000,debug=True)  roda asim => python manage.py







