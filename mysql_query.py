# -*- coding: utf-8 -*-

from mysql_base import Base,A
from sqlalchemy import create_engine

#mysqlTssBR = "mysql://root:123456@localhost/tssfixo_br"
mysqlTssBR = "mysql://root:123456@localhost/tis_oi_br"

def respQuery(mes,ano,pais,report):
   
    paisMySql = {
	"tss-ch" : "mysql://tss_chile:HmverJABzyPy2bEh@201.20.34.19/tss_chile",
	"tss-ar" : "mysql://tss_argentina:jEd:bhDAFtGzZ5Ky@201.20.34.19/tss_argentina",
	"tss-mx" : "mysql://tss_mexico:wpcLLMyQYd:HDae6@201.20.34.19/tss_mexico",
	"tss-br" : "mysql://tss_brasil:pnTfcsZ8GLFfHL3e@201.20.34.19/tss_brasil",
	"tss-rd" : "mysql://tss_rdominicana:xNY559s8L8AL2UsU@201.20.34.19/tss_rdominicana",
	"tss-gt" : "mysql://tss_guatemala:5jWNpMYmuqLRehzX@201.20.34.19/tss_guatemala",
	"tss-co" : "mysql://tss_colombia:Csm5xXKGXQE3NHYJ@201.20.34.19/tss_colombia",
	"tss-pe" : "mysql://tss_peru:MzpDs9aQZJDrc5sB@201.20.34.19/tss_peru",
	"tfx-ch" : "mysql://tssfixo_ch:tssfixo_ch#123@201.20.34.19/tssfixo_ch",
	"tfx-gt" : "mysql://tssfixo_gt:6#ZUYrLuOD8@201.20.34.19/tssfixo_gt",
	"tfx-eq" : "mysql://tssfixo_ec:3DbGKTgAxxUOognF@201.20.34.19/tssfixo_ec",
	"tfx-rd" : "mysql://tssfixo_do:7sjbjS8czd@201.20.34.19/tssfixo_do",
	"tfx-br" : "mysql://net_brasil:9ryDSmHP7ZGs26qR@201.20.34.19/tssfixo_br",
	"tmb-br" : "mysql://tssmobile_br:u7MALK7qBtTHm95U@201.20.34.19/mobile_br",
	"tmb-ar" : "mysql://integradora:titans#123@201.20.34.19/mobile_ar",
	"tnt-mx" : "mysql://tnt-security:3K55qh9yBoxUsX@db7b.security.aws1a.prod.titansgroup.net/tnt-security",
	"tis-oi" : "mysql://tis_app:5P1Q3vCYj59sbbx@db1a.security.aws1.prod.titansgroup.net/tis_oi_br",
	"nas-br" : "mysql://tss_helpdesk:dHNzaGVscC1kZXNrJQ==@201.20.34.19/tss_helpdesk"
    }
    engine = create_engine(paisMySql[pais])
    #engine = create_engine(mysqlTssBR)
    connection = engine.connect()

    queryTFX = """
	SELECT			'853' 			 as PartnerID, #valor recuperado da application.ini
				pa.idPackageAcquisitions as CCID,
				l.login 		 as EmailDaLicensa,
				p.keyTypes 		 as Pacote,
				l.sku 			 as SKU,
				l.insertDate 		 as DataDeAtivacao,
				l.ds_licenses 		 as Licensa

	FROM 			licenses                 as l
	INNER JOIN 		packageacquisitions 	 as pa ON pa.idPackageAcquisitions= l.packageAcquisitions_idPackageAcquisitions
	INNER JOIN 		package 		 as p  ON p.idPackage 		  = pa.package_idPackage
	INNER JOIN 		typelicenses 		 as tl ON tl.idTypeLicenses 	  = l.typeLiceses_idTypeLiceses
	INNER JOIN 		partners 		 as pt ON pt.idPartners           = tl.partners_idPartners

	WHERE      		(l.insertDate between '%s-%s-01 00:00:00' and '%s-%s-31 00:00:00' ) 
	AND        		l.licenses_st = 1 
	AND        		pt.idPartners = 2;
        """ % (ano,mes,ano,mes)

    queryTSS = """
        SELECT                  '712' 			as PartnerID, #valor recuperado da application.ini
                                pa.idPacoteAquisicao 	as CCID,
                                l.ds_login 		as EmailDaLicensa,
                                p.ds_pacote 		as Pacote,
                                l.cod_sku 		as SKU,
                                l.dt_inicio 		as DataDeAtivacao,
                                l.ds_licenca 		as Licensa

        FROM 			licenca 	        as l
        INNER JOIN 		pacoteaquisicao 	as pa ON pa.idPacoteAquisicao 	= l.idPacoteAquisicao
        INNER JOIN 		pacote 			as p ON p.idPacote 		= pa.idPacoteConfigura
        INNER JOIN 		licencatipo 		as lt ON lt.idLicencaTipo 	= l.idLicencaTipo
        INNER JOIN 		parceiro 		as pt ON pt.idParceiro 		= lt.idParceiro

        WHERE			(l.dt_inicio between '%s-%s-01 00:00:00' and '%s-%s-31 00:00:00' )
        AND 			l.st_licenca  = 1 
        AND 			pt.idParceiro = 1;
        """ % (ano,mes,ano,mes)

    #queryTMB = """

    #    """ % (ano,mes,ano,mes)

    queryTNT = """

	SELECT			pea2.value 		 as partnerId, #valor recuperado da application.ini
				lea.value 		 as ccid,
				lea3.value 		 as email,
				pac.name 		 as pacote,
				pea.value 		 as sku,
				l.created 		 as data,
				lea2.value 		 as licenca

	FROM 			license 		 as l
	INNER JOIN 		license_extra_attributes as lea ON lea.license_id   = l.id AND lea.key       = "ccid"
	INNER JOIN 		license_extra_attributes as lea2 ON lea2.license_id = l.id AND lea2.key      = "license"
	INNER JOIN 		license_extra_attributes as lea3 ON lea3.license_id = l.id AND lea3.key      = "email"
	INNER JOIN 		plan_extra_attributes    as pea ON pea.plan_id      = l.plan_id AND pea.key  = "sku"
	INNER JOIN 		plan_extra_attributes    as pea2 ON pea2.plan_id    = l.plan_id AND pea2.key = "partner_id"
	INNER JOIN 		acquisition              as acq ON acq.id           = l.acquisition_id
	INNER JOIN 		package                  as pac ON pac.id           = acq.package_id

	WHERE 			l.vendor_integration_status = "PROVISIONED"
	AND 			l.created > date("%s-%s");
        """ % (ano,mes)

    queryTISAtivos = """
        /* usuários ativos na base */
	select 			cp.ds_phone 		as msisdn, 
				p.ds_email              as email,
				pr.ds_product 		as produto,
				pa.`name` 		as pacote,
				p.dt_acquisition 	as dt_compra,
				p.`value` 		as valor,
				c.ds_channelsale 	as 'canal de venda',
                                c.ds_channelsale 

	from 			product_acquisition     as p
	inner join 		customerphone           as cp on p.customerphone_id = cp.id
	inner join 		product                 as pr on p.product_id       = pr.id
	inner join 		package                 as pa on pa.id              = pr.package_id
	inner join 		acquisition             as a on a.id                = p.acquisition_id
	inner join 		channelsale             as c on c.id                = a.channelsale_id

	where 			p.`status` in (-1,1,2,3,8); 
    """
    queryNetAssist = """
	select   		c.email						as email,
   				c.CpfCnpj					as cpfcnpj,
   				cast(concat('00', c.codigoPlano) as char (40)) 	as pacote,
   				l.dt_insercao 					as data,
   				case 	l.st_licenca
       				    WHEN '1' 
					THEN 'ATIVO'
   				    ELSE  'CANCELADO'
			   	END 
										as status

	from   			cliente 					as c
       	inner join   		licenca 				  	as l ON l.idCliente = c.id_cliente
	order by 		1 desc;
    """
    queryTISCancelados = """
	/* usuários cancelados na base */
	select 			cp.ds_phone 		as msisdn, 
				p.ds_email              as email, 
				pr.ds_product 		as produto,
				pa.`name` 		as pacote,
				p.dt_acquisition 	as dt_compra,
				p.dt_cancel 		as 'data cancelamento',
                                p.dt_cancel,
				p.`value` 		as valor,
				c.ds_channelsale 	as 'canal de venda', 
                                c.ds_channelsale,
				pro.ds_profile 		as 'usuario cancelamento',
                                pro.ds_profile

	from 			product_acquisition     as p	
	inner join 		customerphone           as cp on p.customerphone_id = cp.id
	inner join 		product                 as pr on p.product_id       = pr.id
	inner join 		package                 as pa on pa.id              = pr.package_id
	inner join 		acquisition             as a on a.id                = p.acquisition_id
	inner join 		channelsale             as c on c.id                = a.channelsale_id
	inner join 		user                    as u on u.id                = p.user_idcancel
	inner join 		profile                 as pro on pro.id            = u.profile_id

	where 			p.`status` in (0,6,9);
    """

    if pais[0:1+2]=="tss":
        result = connection.execute(queryTSS)
    elif pais[0:1+2]=="tfx":
	result = connection.execute(queryTFX)
    elif pais[0:1+2]=="tmb":
	result = connection.execute(queryTMB)
    elif pais[0:1+2]=="tnt":
	result = connection.execute(queryTNT)
    elif pais[0:1+2]=="nas":
        result = connection.execute(queryNetAssist)
    elif pais[0:1+2]=="tis" and report==1:
        result = connection.execute(queryTISAtivos)
    elif pais[0:1+2]=="tis" and report==2:
        result = connection.execute(queryTISCancelados)

    return result.fetchall();




